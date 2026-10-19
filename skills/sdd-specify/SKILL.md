---
name: sdd-specify
description: "Especifica un cambio SDD con requisitos RF en notación EARS y criterios de aceptación, creando o revisando su expediente numerado antes de la clarificación QA."
---

# Especificación del cambio

## Entrada

Lee `AGENTS.md` y otras instrucciones aplicables, la constitución acordada con seis
principios en `docs/constitution.md`, las capacidades relevantes de `specs/current/`
y el código/documentación afectados. Si falta la constitución o el contexto SDD,
explica qué fase preparar. No conviertas comportamiento observado en requisito aprobado.

## Procedimiento

1. Identifica objetivo, usuarios, alcance, exclusiones, entradas/salidas y restricciones.
   Pregunta las decisiones de producto que no puedas obtener inspeccionando. No
   diseñes módulos ni escojas tecnologías en lugar del usuario en esta fase.
2. Si se revisa un expediente, usa el indicado. Si hay varios candidatos y falta
   identificación, pregunta. Para uno nuevo, crea `specs/NNN-descripcion/` con el
   siguiente número libre (al menos tres dígitos); no renumeres ni sobrescribas otros.
3. Usa la [plantilla](assets/spec.md) y la [guía EARS](references/ears.md). Escribe
   requisitos atómicos `RF-1…RF-N`, con condiciones y respuestas observables; usa el
   patrón adecuado, sin forzar todos a «Cuando». Incluye fallos y límites relevantes.
4. Añade criterios de aceptación por RF, restricciones no funcionales pertinentes,
   impacto en capacidades vigentes y compatibilidad. Identifica el comportamiento
   observado, el deseado y las incógnitas. No inventes cantidades de RF ni ejemplos
   de negocio como requisitos obligatorios.
5. Registra dudas sin resolver y mantén el estado en borrador o pendiente de
   clarificación. La revisión QA corresponde a la siguiente fase, aunque no hayas
   encontrado dudas durante la escritura.
6. Si cambia una spec existente, conserva IDs, registra los retirados y el motivo,
   incrementa su revisión cuando cambie el significado y señala como desfasados
   clarificación, plan, tareas y aprobación afectados. No borres RF para ocultar fallos.

## Salida y límite

Entrega ruta, revisión, número de RF activos y dudas. La salida es `spec.md` y no
autoriza implementación. No generes anticipadamente plan, tareas, tests ni specs
vigentes. Una corrección pequeña usa los mismos campos con contenido breve.
