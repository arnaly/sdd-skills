# Validación de SDD Skills 0.1.0

Ejecución: 19 de octubre de 2026. Entorno de los tests: Python 3.12.3.

## Comprobaciones automatizadas

- `python3 -m unittest discover -s tests -v`: **17 tests correctos**.
- Validador `quick_validate.py` de Skill Creator: **8 skills válidas**.
- Referencias Markdown locales: sin rutas rotas; los recursos de cada skill
  también se comprobaron después de instalarlos fuera del clon.
- Instalación, reinstalación sin escrituras, conflictos, actualización con respaldo
  y recuperación ante fallos simulados comprobados en directorios temporales.

## Evaluación independiente con agentes

Se utilizaron las skills instaladas en proyectos temporales, se generaron sus
documentos y se ejecutaron tests reales. La aprobación del conjunto se dio en un
mensaje separado después de presentarlo. No son pruebas basadas en buscar frases
de las instrucciones.

| Recorrido | Resultado observado |
| --- | --- |
| Proyecto nuevo: módulo de normalización de etiquetas | Ocho fases; 5 RF cumplen; 3 tareas completas; 7 tests pasan; spec vigente consolidada y expediente conservado. |
| Arreglo pequeño en proyecto existente: límites de paginación | Ocho fases; fallo reproducido antes de corregir; 3 RF cumplen; 2 tareas completas; 4 tests pasan; AGENTS.md y comportamiento previo compatible conservados. |

En siete casos separados se observó el bloqueo correspondiente:

| Entrada | Resultado |
| --- | --- |
| Requisito «rápido» sin umbral decidido | Clarificación abierta; no se creó plan. |
| Tareas sin autorización real | No se modificaron código ni tests. |
| Aprobación de r1 y cambio sustancial a r2 | Aprobación invalidada; implementación detenida. |
| Un RF cubierto y otro sin test | Validación abierta; sin consolidación. |
| Test que no puede cargarse por un runtime ausente | `no ejecutado`; sin consolidación. |
| Spec requiere red y la constitución la prohíbe | Conflicto registrado; sin plan ni alteración de principios. |
| Test llamado RF-2 cuyas aserciones comprueban otro comportamiento | RF-2 identificado sin cobertura, aunque el test pasa; sin cierre. |

Los snapshots antes/después y la existencia de archivos dieron **14 comprobaciones
de resultados correctas** para esos casos. Los [escenarios](scenarios.md) incluyen
también otros casos para futuras evaluaciones; no todos se ejecutaron por separado.

## Hallazgo corregido

La primera evaluación detectó circularidad si una tarea exigía «validar y
consolidar» y a la vez se pedían todas las tareas completas antes de consolidar.
Se pausó el cierre y se corrigieron las instrucciones: implementación y tests son
precondiciones, mientras las tareas de validación/cierre se completan en esa fase.
Se repitió la parte afectada y terminó sin modificar la definición ni la aprobación
de las tareas. `validado` se registra después de completar la consolidación.

## Alcance de la evidencia

Los artefactos de esta ejecución se conservaron en
`/tmp/sdd-behavior-zzj0t_m6/`; son temporales y no forman parte del repositorio.
No se instaló nada en el directorio global del usuario ni se modificaron otros
proyectos. Python 3.10 no se ejecutó: en el ejemplo nuevo se comprobó su gramática,
pero el runtime probado fue 3.12.3. Las evaluaciones son evidencia puntual del
comportamiento del agente, no una garantía para todos los modelos o proyectos.
