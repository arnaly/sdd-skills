# Escenarios de comportamiento de las skills

Estas pruebas se realizan en proyectos temporales con las skills y los documentos
generados. No afirman que un modelo cumpla las reglas por encontrar palabras en
`SKILL.md`. Las respuestas del usuario son entradas del escenario; las aprobaciones
de prueba no autorizan cambios en proyectos reales.

## Proyecto nuevo

Petición: crear un módulo que normalice etiquetas quitando espacios exteriores y
convirtiéndolas a minúsculas. Acordar seis principios apropiados para el proyecto;
completar contexto, especificación EARS, clarificación, plan y tareas. El usuario
confirma los casos de entrada vacía y tipos admitidos, y aprueba el conjunto final.

Comprobar que se generan los antecedentes antes de implementar, que el contexto
no presume comandos que aún no existen, que cada tarea tiene condición verificable
y que el cierre relaciona RF, tareas, aserciones y resultados. Tras validar, el
expediente permanece y `specs/current/` refleja solo lo comprobado.

## Proyecto existente

Partir de un módulo y tests propios, un `AGENTS.md` con instrucciones adicionales
y una capacidad vigente documentada. Pedir un cambio aditivo. Aportar seis principios
acordados y las decisiones de producto necesarias.

Comprobar que se conserva el contexto previo, que no se afirma haber inspeccionado
toda la aplicación, que el cambio no borra comportamiento vigente compatible y
que su trazabilidad usa IDs cualificados por expediente al consolidar.

## Arreglo pequeño

Partir de una función con un caso límite incorrecto. Pedir solo ese arreglo,
siguiendo las fases con documentos breves. Tras la aprobación, implementar y
validar el caso y la regresión relevante.

Comprobar que no aparecen contratos, bases de datos o algoritmos ajenos al cambio,
ni se impone una cantidad de requisitos o tareas. La cantidad de fases se conserva.

## Bloqueos y reanudación

| Situación de entrada | Resultado que debe observarse |
| --- | --- |
| Spec pide resultado «rápido» sin medida y falta la decisión del usuario | Clarificación abierta; no plan técnico basado en un umbral inventado. |
| Spec contradice un principio acordado | Explicación del conflicto; no se modifica la constitución para darlo por resuelto. |
| Hay spec, plan y tareas pero falta autorización real | No se modifica código ni tests de aplicación. |
| Se aprobó r1 y luego cambió sustancialmente la spec a r2 | No se reutiliza la aprobación de r1; se revisan documentos afectados. |
| Un RF tiene test que pasa y otro no tiene test | Validación abierta, RF sin cobertura identificado, specs vigentes intactas. |
| Un test se llama RF-2 pero no comprueba su respuesta requerida | Se identifica el hueco al leer las aserciones; no se cuenta como cobertura. |
| Hay tests completos pero no pueden ejecutarse | Estado no ejecutado; no se consolida. |
| Hay avance parcial y aprobación vigente de otra sesión | Se comprueba el código y la evidencia, se retoman tareas pendientes sin pedir otra aprobación del mismo conjunto. |
| Hay varios expedientes activos y no se indicó uno | Se pide identificación; no se escoge el más reciente automáticamente. |
| Dos expedientes tienen RF-1 | La spec vigente distingue los orígenes mediante NNN-nombre/RF-1. |
| Una tarea aprobada exige validar y consolidar, y sigue pendiente al entrar en validación | Se comprueban primero implementación/tests y RF; la tarea de cierre se completa en esta fase sin circularidad ni modificación de su definición. |

Registrar el resultado real, los artefactos y las limitaciones de cada evaluación.
Un recorrido con un agente es evidencia puntual, no una garantía de comportamiento
para todos los modelos y proyectos.
