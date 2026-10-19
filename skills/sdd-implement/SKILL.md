---
name: sdd-implement
description: "Implementa o retoma un cambio SDD con spec, plan y tareas aprobados, ejecuta sus comprobaciones y registra progreso y evidencias sin consolidar aún la spec vigente."
---

# Implementación del cambio

## Antes de tocar código

1. Identifica el expediente; si hay varios y no está claro cuál, pregunta. Lee
   instrucciones aplicables, constitución acordada con seis principios, spec,
   clarificación resuelta, plan y tareas. Contrasta las revisiones encadenadas y
   cualquier diferencia sustancial posterior a la aprobación.
2. Exige autorización explícita para ese conjunto. Si el usuario acaba de darla
   después de presentarlo, regístrala en `tasks.md` con sus revisiones y evidencia;
   también sirve el registro real de una sesión anterior mientras siga vigente.
   Una casilla, un texto sin evidencia o la invocación de esta skill sin un conjunto
   presentado no son aprobación. Si falta, presenta lo pendiente y espera antes
   de modificar código o tests de aplicación.
3. Si faltan antecedentes, hay bloqueos QA, contradicciones con la constitución o
   aprobación desfasada, explica el motivo y la fase a revisar. No los resuelvas
   silenciosamente cambiando requisitos ni generando el plan sobre la marcha.

## Ejecución

1. Inspecciona estado real del trabajo y evidencia existente. Respeta ediciones
   ajenas. No asumas que un checkbox refleja el estado actual del código.
2. Ejecuta tareas de implementación pendientes en orden de dependencias. Las tareas
   cuyo resultado es validar o consolidar quedan para `sdd-validate`; no marques
   su cierre anticipadamente ni las trates como bloqueos de implementación.
   Implementa y añade/adapta
   tests que comprueben los criterios de los RF y los casos negativos relevantes.
   La verificación debe inspeccionar respuestas observables, no solo nombres de RF.
3. Ejecuta las comprobaciones acordadas y pertinentes. Registra en `tasks.md`
   archivos afectados, comandos, resultados y RF relacionados. Usa el
   [formato de avance](assets/progress.md) sin sustituir el contenido existente.
4. Marca `[x]` únicamente si se cumple «Hecho cuando:» con evidencia. Si no puedes
   ejecutar un test, registra el bloqueo y deja sin marcar las tareas que lo exijan.
   Una tarea parcial sigue pendiente; conserva el detalle suficiente para retomarla.
5. Si surge un cambio sustancial de comportamiento, contrato, solución, restricciones
   o tareas, pausa el trabajo afectado, registra el hallazgo e invalida aprobación.
   Vuelve a las fases necesarias y solicita aprobación del nuevo conjunto. Los
   ajustes internos compatibles y las notas de progreso no necesitan otra aprobación.

## Salida y límite

Informa tareas terminadas/pendientes, tests realmente ejecutados y bloqueos. No
conviertas una implementación en validación final: no modifiques `specs/current/`
ni cierres el expediente en esta fase. No hagas commits, push ni despliegues por
el hecho de implementar un cambio SDD.
