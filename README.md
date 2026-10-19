# SDD Skills

Tu metodología de Spec Driven Development para Codex: ocho skills, documentos
versionados con el código y aprobación antes de implementar. Independiente del
lenguaje y del framework, para proyectos nuevos y existentes.

## Instalar una vez

Requiere Node.js 20 o posterior con npm y Git. El repositorio es privado, así que
necesitas una clave SSH autorizada en GitHub con acceso a `arnaly/sdd-skills`.
Ejecuta desde cualquier carpeta:

Desde este repositorio:

```bash
npx --yes --allow-git=all git+ssh://git@github.com/arnaly/sdd-skills.git install
```

npm obtiene el paquete desde GitHub mediante tu acceso SSH, lo guarda en su caché
y ejecuta el instalador. `--allow-git=all` autoriza esta descarga de Git en npm 12;
no cambia su configuración global. No necesitas clonar este repositorio ni
instalar Python. Las ocho skills y sus
plantillas se copian a `~/.agents/skills` y quedan disponibles para tu usuario
en Codex desde todos tus proyectos.

El comando no crea una constitución ni modifica `AGENTS.md`, `package.json` o
archivos del proyecto desde el que lo ejecutas. La adopción del método se hace
después con las skills.

También puedes elegir un destino de skills reconocido por tu entorno:

```bash
npx --yes --allow-git=all git+ssh://git@github.com/arnaly/sdd-skills.git install --dest /ruta/a/skills
```

Una instalación idéntica no cambia nada. Si hay diferencias, aborta antes de
instalar ninguna skill. No reemplaza archivos, enlaces ni carpetas ajenas.

Para actualizar una instalación gestionada por este instalador:

```bash
npx --yes --allow-git=all git+ssh://git@github.com/arnaly/sdd-skills.git update
```

La actualización es explícita y conserva las carpetas reemplazadas, incluidos tus
cambios locales, en una carpeta hermana del destino: `~/.agents/.skills-sdd-backups/`
para la instalación por defecto. Imprime la ubicación exacta de la copia. Las copias
y la preparación temporal quedan fuera del directorio de skills para evitar que
el asistente descubra versiones antiguas o incompletas.
Para restaurarla, aparta la skill nueva y devuelve la carpeta de la copia a su
ubicación original. Si elegiste otro destino, pasa el mismo `--dest` al actualizar.
No hay actualizaciones automáticas. Las instalaciones son copias; la actualización
reemplaza el contenido gestionado y conserva tus cambios anteriores en el respaldo.
También reconoce instalaciones realizadas con el instalador Python anterior.

El paquete se ejecuta directamente desde GitHub. No hace falta una publicación en
el registro npm para usar estas órdenes. El funcionamiento de `npx` está descrito
en la [documentación de npm](https://docs.npmjs.com/cli/commands/npm-exec/).
Si SSH devuelve `Permission denied (publickey)`, configura el acceso de tu terminal
a GitHub antes de repetir la instalación. No se cambia la visibilidad del repositorio.

Si las skills no aparecen en Codex, reinicia la sesión. Consulta las ubicaciones
admitidas en la [documentación de skills de Codex](https://learn.chatgpt.com/docs/build-skills).

## Activar en un proyecto

Abre el repositorio del proyecto en Codex y pide, en orden:

```text
Usa $sdd-constitution para acordar los seis principios de este proyecto.
Usa $sdd-context para preparar el contexto del agente y activar SDD aquí.
```

La primera skill inspecciona lo disponible y acuerda los principios contigo.
La segunda integra el contexto en `AGENTS.md`, conservando instrucciones previas.
Instalar las skills no aplica SDD automáticamente a otros proyectos. La invocación
explícita de una fase también permite empezar a usarla; si faltan antecedentes,
esa fase explica cuáles hay que preparar.

## Trabajar en un cambio

```text
Usa $sdd-specify para especificar <lo que quiero conseguir>.
Usa $sdd-clarify para revisar specs/001-nombre-del-cambio/ como QA.
Usa $sdd-plan para planificar ese cambio.
Usa $sdd-tasks para desglosarlo y presentarme el conjunto para aprobación.
```

Tras revisar spec, clarificación, plan y tareas, puedes responder:

```text
Apruebo este conjunto. Usa $sdd-implement para implementarlo.
Usa $sdd-validate para comprobar cada RF y cerrar el cambio si cumple todo.
```

| Fase | Entregable principal |
| --- | --- |
| Constitución | `docs/constitution.md`, exactamente seis principios acordados |
| Contexto | `AGENTS.md`, comandos y contexto apoyados en evidencia |
| Especificación | `spec.md`, requisitos EARS `RF-1…RF-N` |
| Clarificación | `clarifications.md`, hallazgos QA y decisiones; spec corregida |
| Planificación | `plan.md`, diseño técnico y verificación prevista |
| Tareas | `tasks.md`, tareas `T1…TN` y «Hecho cuando:» |
| Implementación | Código, tests y progreso en `tasks.md` |
| Validación | `validation.md`, trazabilidad RF → tareas → tests → resultado |

```text
docs/constitution.md
AGENTS.md
specs/
  current/                         # comportamiento vigente verificado por capacidad
  001-nombre-del-cambio/           # expediente, conservado también tras el cierre
    spec.md
    clarifications.md
    plan.md
    tasks.md
    validation.md
```

El número identifica el cambio; no fija la cantidad de requisitos o tareas.
Un arreglo pequeño usa documentos breves y las mismas fases. No se generan de
antemano documentos de fases todavía no realizadas.

## Retomar, adaptar y comprobar

Para retomar en otro chat, indica el expediente y la fase:

```text
Usa $sdd-implement para retomar specs/001-nombre-del-cambio/.
Lee sus documentos y comprueba la aprobación y los avances antes de continuar.
```

Las decisiones, revisiones, aprobación y evidencias se guardan en el expediente.
Una aprobación anterior solo vale para el conjunto al que se refiere. La falta
de tests ejecutados o de cobertura de un RF deja el cambio abierto. Ninguna fase
hace commits, push, despliegues ni publica resultados por el hecho de usar SDD.

Lee las [reglas del método](docs/methodology.md) para entender las transiciones y
la consolidación de specs. Las plantillas están en `skills/*/assets/`; las
instrucciones, en `skills/*/SKILL.md`. Puedes adaptarlas aquí y actualizar después
tu instalación. Cada skill lleva sus recursos sin depender de la ruta del clon.

Para desarrollar o comprobar el instalador, desde un clon del repositorio:

```bash
npm test
```

El instalador Python original se conserva para instalaciones locales desde un
clon (`python3 scripts/install.py`). Sus pruebas se ejecutan con
`python3 -m unittest discover -s tests -v`. La instalación con `npx` solo usa Node.js.

Los tests comprueban instalación, conflictos, recuperación y recursos empaquetados.
Los [escenarios de comportamiento](tests/scenarios.md) describen además los
recorridos que se deben revisar con un agente. Los
[resultados de la validación inicial](tests/validation.md) separan las comprobaciones
automatizadas de las evaluaciones realizadas con agentes. Un chequeo estructural no demuestra
que un asistente siga correctamente las instrucciones. Son una guía de trabajo,
no un motor que imponga técnicamente las transiciones.
