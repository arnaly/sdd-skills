---
name: sdd-validate
description: "Valida un cambio SDD requisito por requisito contrastando tareas, aserciones y tests ejecutados; documenta huecos y consolida specs vigentes solo si el cambio completo cumple."
---

# Validación del cambio

## Entrada

Identifica el expediente. Lee instrucciones, constitución acordada, spec, clarificación,
plan, tareas, aprobación, avance, código/tests afectados y specs vigentes. Comprueba
que las revisiones son coherentes y el conjunto sigue aprobado. Si faltan entradas
o están desfasadas, documenta el bloqueo en `validation.md` cuando haya expediente
identificado y no consolides. No inventes revisiones ni autorizaciones.

## Recorrido RF por RF

1. Usa la [plantilla de validación](assets/validation.md). Enumera **todos los RF
   activos**, sin omitir los difíciles ni contar retirados como cumplidos. Para cada
   uno identifica criterios, tareas y tests por ruta y nombre/caso concreto.
2. Lee las aserciones: explica qué parte del RF verifica cada test y qué queda fuera.
   Un nombre que contiene «RF-1», un mock del resultado esperado sin ejecutar la
   lógica pertinente o un proceso que sale con código 0 no demuestran cumplimiento.
3. Ejecuta las comprobaciones acordadas pertinentes al estado actual y registra
   comandos, alcance, resultados y limitaciones. Reutiliza evidencia de esta sesión
   solo si corresponde al mismo estado del código, configuración y datos relevantes;
   si hay dudas o solo consta un resultado antiguo de otra sesión, vuelve a comprobar.
4. Asigna por RF: `cumple`, `falla`, `sin cobertura` o `no ejecutado`. Si hay varias
   verificaciones, cualquier fallo prevalece; sin fallos, señala primero huecos de
   cobertura y luego ejecuciones pendientes. Ninguno de esos casos es `cumple`.
   Un test puede cubrir varios RF y un RF necesitar varios tests. Una revisión
   manual complementa la evidencia, sin reemplazar la cobertura de tests acordada.
5. Revisa también «Hecho cuando:» de las tareas, los seis principios, regresiones y
   contratos afectados. Distingue tareas de implementación/tests de tareas cuyo
   resultado pertenece a esta fase (validación/consolidación). Las primeras deben
   estar completas; las segundas se completan aquí al satisfacer sus condiciones,
   sin exigir que el cierre exista antes de ejecutarlo. Si no tienen fase explícita,
   usa su resultado y condición aprobados, sin cambiar su definición. No marques
   tareas por el checkbox solamente. Registra contradicciones y bloqueos con evidencia.

## Cierre y consolidación

- Si hay un RF fallido, sin cobertura o no ejecutado, tareas de implementación/tests
  incompletas, principios incumplidos o bloqueos, deja el expediente abierto y entrega acciones concretas.
  Esta fase no repara código, modifica tests para hacerlos pasar ni cambia requisitos.
- Solo si esas comprobaciones cumplen, realiza las tareas de validación/cierre y
  consolida las capacidades afectadas en `specs/current/<capacidad>.md` usando la
  [plantilla de capacidad](assets/current-spec.md). Conserva comportamiento previo
  compatible y aplica modificaciones o retiradas únicamente según el cambio aprobado.
- Cita los RF con su expediente (`001-nombre/RF-1`) para evitar colisiones entre
  IDs locales. No copies dudas, planes pendientes ni comportamiento solo observado
  como si estuviese verificado. Resuelve contradicciones con specs vigentes antes
  de cerrar; no las sobrescribas a ciegas.
- Tras completar las condiciones de las tareas de esta fase, registra su evidencia
  y marca sus checkboxes. Solo con todas las tareas completas y la consolidación
  terminada marca `validation.md` como `validado`, registra capacidades actualizadas
  y fecha/evidencia de cierre y marca el expediente cerrado en su spec. Si la
  consolidación no puede completarse, informa el estado parcial y deja abierto el
  expediente, sin afirmar un cierre. Conserva los documentos en la misma carpeta numerada.
  No archives fuera del repositorio ni borres evidencia.
- En un expediente ya cerrado, no reescribas una validación pasada para esconder
  una regresión: añade el nuevo hallazgo y propón un nuevo expediente de corrección.

Entrega totales por estado de RF, cobertura real, tareas pendientes y conclusión
(`validado` o `abierto`). No declares que todo funciona fuera del alcance comprobado.
