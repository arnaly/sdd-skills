#!/usr/bin/env node

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { installSkills } from '../scripts/install.mjs';

const root = fileURLToPath(new URL('../', import.meta.url));
const help = `Uso: sdd-skills [install|update] [--dest DIRECTORIO]

  install       Instalar las ocho skills (opción por defecto).
  update        Actualizar las instalaciones propias, con copia de respaldo.
  --dest RUTA   Destino de skills; por defecto ./skills en el repositorio actual.
  --help        Mostrar esta ayuda.
  --version     Mostrar la versión.

Instala las skills en el proyecto desde el que lo ejecutas.`;

try {
  if (Number(process.versions.node.split('.')[0]) < 20) {
    throw new Error('Se necesita Node.js 20 o posterior.');
  }
  const args = process.argv.slice(2);
  let destination = resolve('skills');
  let command;
  let mode;
  for (let index = 0; index < args.length; index += 1) {
    const argument = args[index];
    if (argument === '--help' || argument === '-h') {
      mode = 'help';
    } else if (argument === '--version' || argument === '-v') {
      mode = 'version';
    } else if (argument === '--dest') {
      const value = args[++index];
      if (!value || value.startsWith('--')) throw new Error('Falta la ruta de --dest.');
      destination = resolve(value);
    } else if (argument.startsWith('--dest=')) {
      const value = argument.slice('--dest='.length);
      if (!value) throw new Error('Falta la ruta de --dest.');
      destination = resolve(value);
    } else if ((argument === 'install' || argument === 'update') && !command) {
      command = argument;
    } else {
      throw new Error(`Argumento desconocido: ${argument}. Usa --help.`);
    }
  }
  if (mode === 'help') {
    console.log(help);
  } else if (mode === 'version') {
    console.log(readFileSync(resolve(root, 'VERSION'), 'utf8').trim());
  } else {
    const result = installSkills(root, destination, { update: command === 'update' });
    console.log(`Destino: ${result.destination}`);
    console.log(`Instaladas/actualizadas: ${result.installed.length}; sin cambios: ${result.unchanged.length}`);
    if (result.backup) console.log(`Copia anterior: ${result.backup}`);
    console.log('Si Codex no muestra las skills, reinicia su sesión.');
  }
} catch (error) {
  console.error(`Error: ${error.message}`);
  process.exitCode = 1;
}
