import assert from 'node:assert/strict';
import fs from 'node:fs';
import { syncBuiltinESMExports } from 'node:module';
import { tmpdir } from 'node:os';
import { basename, dirname, join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';
import { installSkills, SKILLS } from '../scripts/install.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));

function fixture(t) {
  const base = fs.mkdtempSync(join(tmpdir(), 'sdd-node-test-'));
  t.after(() => fs.rmSync(base, { recursive: true, force: true }));
  const source = join(base, 'source');
  fs.mkdirSync(source);
  fs.cpSync(join(root, 'skills'), join(source, 'skills'), { recursive: true });
  fs.copyFileSync(join(root, 'VERSION'), join(source, 'VERSION'));
  return { base, source, destination: join(base, 'personal skills') };
}

function snapshot(directory) {
  const result = {};
  function visit(path) {
    for (const entry of fs.readdirSync(path, { withFileTypes: true })) {
      const child = join(path, entry.name);
      if (entry.isDirectory()) visit(child);
      else if (entry.isFile()) result[child.slice(directory.length)] = fs.readFileSync(child).toString('base64');
      else result[child.slice(directory.length)] = fs.readlinkSync(child);
    }
  }
  visit(directory);
  return result;
}

test('installs all resources and preserves unrelated skills', (t) => {
  const { source, destination } = fixture(t);
  fs.mkdirSync(join(destination, 'custom'), { recursive: true });
  fs.writeFileSync(join(destination, 'custom', 'keep.txt'), 'keep');
  const result = installSkills(source, destination);
  assert.deepEqual(result.installed, SKILLS);
  assert.equal(fs.readFileSync(join(destination, 'custom', 'keep.txt'), 'utf8'), 'keep');
  assert.ok(fs.existsSync(join(destination, 'sdd-specify', 'references', 'ears.md')));
  assert.ok(fs.existsSync(join(destination, 'sdd-validate', 'assets', 'validation.md')));
  assert.ok(fs.existsSync(join(destination, 'sdd-context', 'agents', 'openai.yaml')));
});

test('identical reinstall performs no writes', (t) => {
  const { source, destination } = fixture(t);
  installSkills(source, destination);
  const sentinel = join(destination, 'sdd-plan', 'SKILL.md');
  fs.utimesSync(sentinel, 1, 1);
  const result = installSkills(source, destination);
  assert.equal(result.installed.length, 0);
  assert.equal(result.unchanged.length, 8);
  assert.equal(fs.statSync(sentinel).mtimeMs, 1000);
});

test('foreign folder prevents any installation, including update', (t) => {
  const { source, destination } = fixture(t);
  fs.mkdirSync(join(destination, 'sdd-validate'), { recursive: true });
  fs.writeFileSync(join(destination, 'sdd-validate', 'SKILL.md'), 'foreign');
  const before = snapshot(destination);
  assert.throws(() => installSkills(source, destination), /carpeta ajena/);
  assert.throws(() => installSkills(source, destination, { update: true }), /carpeta ajena/);
  assert.deepEqual(snapshot(destination), before);
});

test('local edits require update and remain in a backup outside discovery', (t) => {
  const { source, destination } = fixture(t);
  installSkills(source, destination);
  fs.writeFileSync(join(destination, 'sdd-plan', 'assets', 'plan.md'), 'local plan');
  fs.writeFileSync(join(destination, 'sdd-plan', 'extra.txt'), 'local extra');
  const before = snapshot(destination);
  assert.throws(() => installSkills(source, destination), /usa update/);
  assert.deepEqual(snapshot(destination), before);
  const result = installSkills(source, destination, { update: true });
  assert.deepEqual(result.installed, ['sdd-plan']);
  assert.equal(dirname(dirname(result.backup)), dirname(destination));
  assert.equal(fs.readFileSync(join(result.backup, 'sdd-plan', 'assets', 'plan.md'), 'utf8'), 'local plan');
  assert.equal(fs.readFileSync(join(result.backup, 'sdd-plan', 'extra.txt'), 'utf8'), 'local extra');
  assert.ok(!fs.existsSync(join(destination, 'sdd-plan', 'extra.txt')));
});

test('recognizes an installation marker written by the Python installer', (t) => {
  const { source, destination } = fixture(t);
  installSkills(source, destination);
  const version = fs.readFileSync(join(source, 'VERSION'), 'utf8').trim();
  for (const name of SKILLS) {
    fs.writeFileSync(join(destination, name, '.sdd-install.json'), JSON.stringify({ version, skill: name, managed_by: 'sdd-skills' }));
  }
  assert.equal(installSkills(source, destination).unchanged.length, 8);
});

test('files and dangling symlink targets are not replaced', (t) => {
  const { source, destination, base } = fixture(t);
  fs.mkdirSync(destination);
  fs.writeFileSync(join(destination, 'sdd-plan'), 'keep');
  fs.symlinkSync(join(base, 'missing'), join(destination, 'sdd-context'), 'dir');
  assert.throws(() => installSkills(source, destination, { update: true }), /archivo o enlace/);
  assert.equal(fs.readFileSync(join(destination, 'sdd-plan'), 'utf8'), 'keep');
  assert.ok(fs.lstatSync(join(destination, 'sdd-context')).isSymbolicLink());
  assert.equal(fs.readdirSync(destination).length, 2);
});

test('incomplete or linked source fails before creating the destination', (t) => {
  const { source, destination, base } = fixture(t);
  fs.unlinkSync(join(source, 'skills', 'sdd-validate', 'SKILL.md'));
  assert.throws(() => installSkills(source, destination), /incompleta/);
  assert.ok(!fs.existsSync(destination));
  fs.copyFileSync(join(root, 'skills', 'sdd-validate', 'SKILL.md'), join(source, 'skills', 'sdd-validate', 'SKILL.md'));
  fs.symlinkSync(join(base, 'outside'), join(source, 'skills', 'sdd-plan', 'link.txt'));
  assert.throws(() => installSkills(source, destination), /Enlace/);
  assert.ok(!fs.existsSync(destination));
});

test('source overlap is rejected, including through a parent symlink', (t) => {
  const { source, base } = fixture(t);
  const link = join(base, 'linked-source');
  fs.symlinkSync(source, link, 'dir');
  for (const target of [source, join(source, 'skills'), join(link, 'skills', 'nested')]) {
    assert.throws(() => installSkills(source, target), /solaparse/);
  }
});

test('an unsafe backup location is rejected without touching installed files', (t) => {
  const { source, destination, base } = fixture(t);
  installSkills(source, destination);
  fs.writeFileSync(join(destination, 'sdd-plan', 'local.txt'), 'keep');
  const outside = join(base, 'outside');
  fs.mkdirSync(outside);
  fs.symlinkSync(outside, join(dirname(destination), `.${basename(destination)}-sdd-backups`), 'dir');
  const before = snapshot(destination);
  assert.throws(() => installSkills(source, destination, { update: true }), /directorio seguro/);
  assert.deepEqual(snapshot(destination), before);
  assert.deepEqual(fs.readdirSync(outside), []);
});

for (const update of [false, true]) {
  test(`deployment failure rolls back ${update ? 'an update' : 'a fresh install'}`, (t) => {
    const { source, destination } = fixture(t);
    if (update) {
      installSkills(source, destination);
      fs.writeFileSync(join(source, 'VERSION'), '999.0.0\n');
    }
    const before = update ? snapshot(destination) : {};
    const rename = fs.renameSync;
    const mocked = t.mock.method(fs, 'renameSync', (from, to) => {
      if (basename(dirname(from)).startsWith('.sdd-install-') && basename(from) === 'sdd-plan') {
        throw new Error('simulated deployment failure');
      }
      return rename(from, to);
    });
    syncBuiltinESMExports();
    try {
      assert.throws(() => installSkills(source, destination, { update }), /simulated deployment failure/);
    } finally {
      mocked.mock.restore();
      syncBuiltinESMExports();
    }
    assert.deepEqual(snapshot(destination), before);
    assert.ok(fs.readdirSync(dirname(destination)).every((name) => !name.startsWith('.sdd-install-')));
  });
}

test('CLI works from an unrelated project without changing its files', (t) => {
  const { base, destination } = fixture(t);
  const project = join(base, 'another-project');
  fs.mkdirSync(project);
  fs.writeFileSync(join(project, 'package.json'), '{"name":"existing-project","version":"1.0.0"}\n');
  fs.writeFileSync(join(project, 'AGENTS.md'), 'Keep existing instructions.\n');
  const before = snapshot(project);
  const result = spawnSync(process.execPath, [join(root, 'bin', 'sdd-skills.mjs'), 'install', '--dest', destination], { cwd: project, encoding: 'utf8' });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Instaladas\/actualizadas: 8/);
  assert.deepEqual(snapshot(project), before);
});

test('help, version and invalid arguments do not install anything', (t) => {
  const { destination } = fixture(t);
  for (const [argument, status] of [['--help', 0], ['--version', 0], ['--project', 1], ['--dest', 1]]) {
    const args = argument === '--dest' ? ['--dest'] : [argument, '--dest', destination];
    const result = spawnSync(process.execPath, [join(root, 'bin', 'sdd-skills.mjs'), ...args], { encoding: 'utf8' });
    assert.ifError(result.error);
    assert.equal(result.status, status, result.stderr);
    assert.ok(!fs.existsSync(destination));
  }
});

test('the npm package installs offline outside the clone with all bundled resources', (t) => {
  const base = fs.mkdtempSync(join(tmpdir(), 'sdd-pack-test-'));
  t.after(() => fs.rmSync(base, { recursive: true, force: true }));
  const env = {
    ...process.env,
    npm_config_cache: join(base, 'npm-cache'),
    npm_config_offline: 'true',
    npm_config_audit: 'false',
    npm_config_fund: 'false',
    npm_config_update_notifier: 'false',
  };
  const packed = spawnSync('npm', ['pack', '--ignore-scripts', '--json', '--pack-destination', base], { cwd: root, env, encoding: 'utf8' });
  assert.ifError(packed.error);
  assert.equal(packed.status, 0, packed.stderr);
  const metadata = JSON.parse(packed.stdout);
  const info = Array.isArray(metadata) ? metadata[0] : Object.values(metadata)[0];
  const paths = info.files.map((file) => file.path);
  for (const skill of SKILLS) assert.ok(paths.includes(`skills/${skill}/SKILL.md`));
  assert.ok(paths.includes('bin/sdd-skills.mjs'));
  assert.ok(paths.includes('scripts/install.mjs'));
  assert.ok(paths.every((path) => !/^(tests|docs|\.git|\.aws|\.codex)\//.test(path)));
  const project = join(base, 'another-project');
  fs.mkdirSync(project);
  fs.writeFileSync(join(project, 'package.json'), '{"name":"caller","version":"1.0.0"}\n');
  fs.writeFileSync(join(project, 'AGENTS.md'), 'Keep existing instructions.\n');
  const before = snapshot(project);
  const destination = join(base, 'installed');
  const result = spawnSync('npm', ['exec', '--yes', `--package=${join(base, info.filename)}`, '--', 'sdd-skills', 'install', '--dest', destination], { cwd: project, env, encoding: 'utf8' });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stderr);
  assert.match(result.stdout, /Instaladas\/actualizadas: 8/);
  assert.deepEqual(snapshot(project), before);
  assert.ok(fs.existsSync(join(destination, 'sdd-specify', 'references', 'ears.md')));
  assert.ok(fs.existsSync(join(destination, 'sdd-validate', 'assets', 'validation.md')));
});
