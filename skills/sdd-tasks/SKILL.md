---
name: sdd-tasks
description: "Desglosa un plan SDD en tareas con checkboxes, dependencias, RF y Hecho cuando verificable, y presenta el conjunto para aprobación antes de implementar."
---

# Tareas del cambio

## Entrada

Identifica el expediente. Lee instrucciones, constitución acordada, spec, clarificación
resuelta para esa spec y plan listo con sus revisiones de entrada vigentes. Lee las
tareas existentes antes de editarlas. Si faltan antecedentes o hay contradicciones,
explica el bloqueo y no inventes el plan.

## Procedimiento

1. Desglosa `tasks.md` usando la [plantilla](assets/tasks.md). Usa `T1…TN` estables,
   checkbox por tarea, dependencias, RF relacionados y **«Hecho cuando:»** con una
   condición observable. Una tarea de soporte sin RF directo requiere justificación.
2. Incluye implementación y tests apropiados para todos los RF. Cada RF activo debe
   tener tareas y verificaciones previstas. Las dependencias deben existir y no
   formar ciclos. Ajusta el tamaño a unidades comprobables, sin fijar ocho tareas.
   Si hay tareas de validación o consolidación final, identifícalas como
   `Fase: validación/cierre`; se completan en `sdd-validate`, no son una precondición
   de sí mismas. Sus dependencias de implementación y tests sí deben estar completas.
3. Conserva IDs y evidencia de tareas previas. No marques trabajo hecho por existir
   código parecido: comprueba su condición. Las nuevas tareas empiezan sin marcar.
4. Registra las revisiones de constitución, spec, clarificación y plan. Presenta
   alcance, decisiones, tareas y comprobaciones al usuario y solicita aprobación
   explícita del conjunto antes de implementar.
5. Mantén `Aprobación: pendiente` hasta recibir autorización real para ese conjunto.
   Puedes registrar una autorización ya recibida que lo cubra, sin volver a pedirla.
   Guarda mensaje exacto relevante, fecha/referencia disponible y las revisiones
   aprobadas, incluida la revisión de la definición de tareas. No fabriques evidencia.
6. Cambiar sustancialmente las tareas o sus entradas invalida la aprobación anterior:
   incrementa la revisión, explica el impacto y presenta el nuevo conjunto. Actualizar
   checkboxes o el registro de avance no cambia por sí solo la definición aprobada.

## Salida y límite

Entrega tareas, cobertura RF → tareas, bloqueos y estado real de aprobación. Esta
fase no implementa aunque el plan sea claro. El registro de aprobación permite
retomar en otro chat; no autoriza acciones fuera del alcance ni sustituye permisos.
