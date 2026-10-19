---
name: sdd-clarify
description: "Revisa una spec SDD como QA antes de planificar, detecta ambigüedades y escenarios omitidos, registra respuestas del usuario y corrige los requisitos afectados."
---

# Clarificación de requisitos

## Entrada

Identifica el expediente sin elegir arbitrariamente entre varios. Lee las
instrucciones aplicables, la constitución acordada, `spec.md`, la clarificación
previa si existe, las specs vigentes y el código relevante. Si faltan antecedentes
o hay un conflicto con principios, explica el bloqueo antes de planificar.

## Revisión QA

1. Revisa cada RF y sus criterios como alguien que tiene que construir un test:
   ¿se pueden determinar entradas, condiciones y respuesta sin inventar reglas?
2. Busca ambigüedad de términos, actores y permisos, contradicciones entre RF,
   estados inicial/final, entradas vacías o inválidas, errores y escenarios límite
   pertinentes. Revisa fechas, persistencia, concurrencia o compatibilidad solo
   cuando el cambio las implique. No amplíes el alcance con una lista genérica.
3. Registra hallazgos `CL-1…CL-N` en `clarifications.md` usando la
   [plantilla](assets/clarifications.md): RF afectado, pregunta, impacto, carácter
   bloqueante, respuesta real y resolución. Conserva el historial de preguntas
   existentes. Si no hay hallazgos, registra qué se revisó y ese resultado.
4. Resuelve hechos mediante inspección y cita su evidencia. Las decisiones sobre
   comportamiento se consultan al usuario. Una recomendación o un supuesto del
   agente no cuenta como respuesta; no cierres una pregunta por falta de respuesta.
5. Actualiza `spec.md` con las decisiones, conservando IDs y aumentando su revisión
   cuando corresponda. Registra la revisión final revisada en la clarificación.
   Invalida plan, tareas y aprobación si estaban basados en otra interpretación.
6. Solo marca la revisión `resuelta` y la spec `aclarada` si no quedan ambigüedades
   que afecten a comportamiento, alcance o aceptación. Una sugerencia editorial
   puede quedar anotada como no bloqueante con su justificación.

## Salida y límite

Informa hallazgos abiertos/resueltos y la revisión de spec cubierta. Con bloqueos,
solicita las respuestas pendientes y detente antes de planificar. Esta fase no
elige la solución técnica ni implementa; tampoco aprueba automáticamente el cambio.
