---
name: sdd-constitution
description: "Acuerda y documenta seis principios innegociables para iniciar o revisar la constitución SDD de un proyecto. Úsala para definir sus reglas, no para especificar una funcionalidad."
---

# Constitución del proyecto

## Entrada

Petición de preparar o revisar la constitución. Lee las instrucciones de agente
aplicables, la documentación y una muestra relevante del código y configuración.
Si existe `docs/constitution.md`, léela antes de proponer cambios. Inspeccionar un
comando no equivale a haberlo ejecutado.

## Procedimiento

1. Resume propósito, usuarios y restricciones conocidos. Separa lo observado,
   lo deseado y lo desconocido; en un repositorio vacío no inventes decisiones.
2. Propón **exactamente seis** principios propios del proyecto. Cada uno debe
   expresar una regla concreta y una forma observable de comprobarla. Usa la
   [plantilla](assets/constitution.md); sus campos no son principios predeterminados.
3. Acuérdalos con el usuario. Si faltan decisiones que cambian los principios,
   pregúntalas. Puedes guardar una propuesta como borrador, pero no declararla
   acordada por el silencio del usuario.
4. Guarda `docs/constitution.md` con revisión, evidencia del acuerdo y seis
   principios. Conserva contexto y contenido válido existente; si hay otro número
   de principios o instrucciones contradictorias, presenta la adaptación y resuelve
   el conflicto antes de fijar la constitución.
5. Ante una revisión, registra motivo e impacto en expedientes activos. Cambiar
   sustancialmente un principio invalida la revisión de los planes y aprobaciones
   afectados; no cambies las reglas para justificar código ya escrito.

## Salida y límite

Informa ruta, revisión y estado (`borrador` o `acordada`), qué se inspeccionó y qué
queda pendiente. Para avanzar a contexto debe estar acordada. Esta fase no crea
requisitos de cambios ni implementa código, y no activa SDD por sí sola en otros
proyectos. Una constitución ya acordada no necesita regenerarse en cada cambio.
