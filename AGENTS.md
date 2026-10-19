# Instrucciones para agentes

## Proyecto

Este repositorio distribuye ocho skills de Spec Driven Development para Codex.
Las instrucciones, plantillas y documentación se mantienen en español.

- `skills/sdd-*/SKILL.md`: instrucciones de cada fase.
- `skills/sdd-*/assets/`: plantillas que utiliza cada skill.
- `skills/sdd-*/references/`: material de consulta, cuando corresponde.
- `skills/sdd-*/agents/openai.yaml`: metadatos de las skills.
- `docs/methodology.md`: reglas y transiciones del método.
- `bin/sdd-skills.mjs`: entrada de la CLI.
- `scripts/install.mjs`: instalador principal en Node.js.
- `scripts/install.py`: instalador Python anterior, conservado por compatibilidad.
- `tests/`: pruebas del instalador y escenarios de comportamiento de las skills.

## Desarrollo

- Prefiere soluciones simples y mantenibles y respeta el estilo existente.
- El paquete usa módulos ES y requiere Node.js 20 o posterior. Evita añadir
  dependencias sin una necesidad concreta.
- Mantén coherentes las instrucciones de las skills, sus plantillas, el README
  y la metodología cuando cambies el comportamiento del método.
- Cada skill debe funcionar después de copiarla fuera de este clon. Sus recursos
  deben usar rutas relativas a su propia carpeta.
- Conserva las garantías del instalador: instalación idéntica sin cambios,
  detección de conflictos antes de instalar, actualización explícita con respaldo
  y recuperación ante fallos. Instala por defecto en `./skills` del proyecto
  desde el que se ejecuta, conservando sus demás archivos.
- Usa destinos temporales para comprobar instalaciones; no actualices las skills
  globales del usuario como parte de una prueba.
- Mantén sincronizados `VERSION` y la versión de `package.json` cuando se autorice
  un cambio de versión.
- Este archivo aporta contexto para desarrollar el repositorio. No activa por sí
  solo el flujo SDD ni implica aprobación de especificaciones, tareas o entregas.

## Verificación

- Para cambios en la CLI o el instalador Node.js: `npm test`.
- Para cambios en el instalador Python: `python3 -m unittest discover -s tests -v`.
- Para cambios en recursos compartidos por ambos instaladores, ejecuta ambas suites.
- Para cambios en las skills o documentación, revisa la coherencia y las rutas
  locales; consulta `tests/scenarios.md` para elegir los escenarios pertinentes.
- Los tests estructurales no demuestran que un agente siga las instrucciones.
  Distingue las comprobaciones automatizadas de las evaluaciones de comportamiento.
- Verifica los cambios antes de informar de su finalización e indica qué se ha
  comprobado y qué queda sin verificar.

## Git y GitHub

- Usa Git CLI para operaciones locales y el MCP oficial de GitHub para operaciones
  específicas de GitHub, como issues, pull requests y GitHub Actions.
- No crees commits, hagas push, fusiones pull requests, publiques paquetes ni
  realices operaciones destructivas sin autorización explícita del usuario.
- Ejecuta las pruebas pertinentes antes de crear commits.
- Conserva los cambios ajenos a la tarea y revisa el diff antes de darla por terminada.
