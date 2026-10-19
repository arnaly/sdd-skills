import {
  cpSync, existsSync, lstatSync, mkdirSync, mkdtempSync, readFileSync,
  readdirSync, realpathSync, renameSync, rmSync, rmdirSync, writeFileSync,
} from 'node:fs';
import { createHash, randomUUID } from 'node:crypto';
import { basename, dirname, isAbsolute, join, relative, resolve } from 'node:path';

export const SKILLS = Object.freeze([
  'sdd-constitution', 'sdd-context', 'sdd-specify', 'sdd-clarify',
  'sdd-plan', 'sdd-tasks', 'sdd-implement', 'sdd-validate',
]);
const MARKER = '.sdd-install.json';

function statIfPresent(path) {
  try {
    return lstatSync(path);
  } catch (error) {
    if (error.code === 'ENOENT') return undefined;
    throw error;
  }
}

function canonicalDestination(path) {
  const missing = [];
  let ancestor = resolve(path);
  while (!statIfPresent(ancestor)) {
    missing.unshift(basename(ancestor));
    ancestor = dirname(ancestor);
  }
  return join(realpathSync(ancestor), ...missing);
}

function contains(parent, child) {
  const path = relative(parent, child);
  return path === '' || (!isAbsolute(path) && path !== '..' && !path.startsWith(`..${process.platform === 'win32' ? '\\' : '/'}`));
}

function manifest(folder) {
  const result = [];
  function visit(directory) {
    for (const name of readdirSync(directory).sort()) {
      const path = join(directory, name);
      const stat = lstatSync(path);
      if (stat.isSymbolicLink()) throw new Error(`Enlace dentro de la skill: ${path}`);
      if (stat.isDirectory()) visit(path);
      else if (stat.isFile()) {
        if (path !== join(folder, MARKER)) {
          result.push([relative(folder, path).split('\\').join('/'), createHash('sha256').update(readFileSync(path)).digest('hex')]);
        }
      } else throw new Error(`Archivo no regular dentro de la skill: ${path}`);
    }
  }
  visit(folder);
  return JSON.stringify(result.sort(([left], [right]) => left.localeCompare(right)));
}

function readOwner(folder) {
  const path = join(folder, MARKER);
  const stat = statIfPresent(path);
  if (!stat?.isFile() || stat.isSymbolicLink()) return {};
  try {
    const value = JSON.parse(readFileSync(path, 'utf8'));
    return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  } catch (error) {
    if (error instanceof SyntaxError) return {};
    throw error;
  }
}

export function installSkills(sourceRoot, requestedDestination, { update = false } = {}) {
  const source = realpathSync(sourceRoot);
  const payload = join(source, 'skills');
  const destination = canonicalDestination(requestedDestination);
  if (contains(payload, destination) || contains(destination, payload)) {
    throw new Error('El destino no puede solaparse con las skills de origen.');
  }
  const version = readFileSync(join(source, 'VERSION'), 'utf8').trim();
  if (!version) throw new Error('VERSION está vacía.');
  if (statIfPresent(destination) && !lstatSync(destination).isDirectory()) {
    throw new Error(`El destino no es una carpeta: ${destination}`);
  }

  const expected = new Map();
  const owners = new Map();
  for (const name of SKILLS) {
    const folder = join(payload, name);
    const stat = statIfPresent(folder);
    const entrypoint = statIfPresent(join(folder, 'SKILL.md'));
    if (!stat?.isDirectory() || stat.isSymbolicLink() || !entrypoint?.isFile() || entrypoint.isSymbolicLink()) {
      throw new Error(`Skill de origen incompleta: ${folder}`);
    }
    expected.set(name, manifest(folder));
    owners.set(name, { managed_by: 'sdd-skills', skill: name, version });
  }

  const changed = [], unchanged = [], previous = [], conflicts = [];
  for (const name of SKILLS) {
    const target = join(destination, name);
    const stat = statIfPresent(target);
    if (!stat) {
      changed.push(name);
      continue;
    }
    if (stat.isSymbolicLink() || !stat.isDirectory()) {
      conflicts.push(`${name}: el destino es un archivo o enlace`);
      continue;
    }
    const owner = readOwner(target);
    if (owner.managed_by !== 'sdd-skills' || owner.skill !== name) {
      conflicts.push(`${name}: carpeta ajena o sin marca de este instalador`);
      continue;
    }
    let same = false;
    try {
      same = manifest(target) === expected.get(name) && owner.version === version;
    } catch {
      // No leer enlaces locales; la carpeta completa se conserva en el respaldo.
    }
    if (same) unchanged.push(name);
    else if (update) {
      changed.push(name);
      previous.push(name);
    } else conflicts.push(`${name}: contenido o versión diferente; revisa y usa update`);
  }
  if (conflicts.length) throw new Error(`No se ha instalado ninguna skill:\n- ${conflicts.join('\n- ')}`);
  if (!changed.length) return { destination, installed: [], unchanged, backup: null };

  const backupRoot = join(dirname(destination), `.${basename(destination)}-sdd-backups`);
  const backupStat = statIfPresent(backupRoot);
  if (previous.length && backupStat && (!backupStat.isDirectory() || backupStat.isSymbolicLink())) {
    throw new Error(`La carpeta de copias no es un directorio seguro: ${backupRoot}`);
  }
  mkdirSync(destination, { recursive: true });
  const backup = previous.length ? join(backupRoot, randomUUID()) : null;
  const staging = mkdtempSync(join(dirname(destination), '.sdd-install-'));
  const deployed = [], moved = [];
  try {
    for (const name of changed) {
      cpSync(join(payload, name), join(staging, name), { recursive: true, dereference: false });
      writeFileSync(join(staging, name, MARKER), `${JSON.stringify(owners.get(name), null, 2)}\n`);
    }
    try {
      if (backup) mkdirSync(backup, { recursive: true });
      for (const name of changed) {
        const target = join(destination, name);
        if (previous.includes(name)) {
          renameSync(target, join(backup, name));
          moved.push(name);
        } else if (statIfPresent(target)) {
          throw new Error(`El destino ha cambiado durante la instalación: ${target}`);
        }
        renameSync(join(staging, name), target);
        deployed.push(name);
      }
    } catch (error) {
      const recoveryErrors = [];
      for (const name of deployed.reverse()) {
        try { rmSync(join(destination, name), { recursive: true }); }
        catch (recoveryError) { recoveryErrors.push(recoveryError.message); }
      }
      for (const name of moved.reverse()) {
        try { renameSync(join(backup, name), join(destination, name)); }
        catch (recoveryError) { recoveryErrors.push(recoveryError.message); }
      }
      if (recoveryErrors.length) {
        throw new Error(`Falló parte de la recuperación. Revisa ${backup}: ${recoveryErrors.join('; ')}`, { cause: error });
      }
      if (backup && existsSync(backup)) rmdirSync(backup);
      throw error;
    }
  } finally {
    rmSync(staging, { recursive: true, force: true });
  }
  return { destination, installed: changed, unchanged, backup };
}
