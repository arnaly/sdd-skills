# Reglas de la metodología

## Unidad de trabajo

La constitución y el contexto son del proyecto. El resto de documentos pertenece
a un expediente `specs/NNN-descripcion/`. Las capacidades vigentes se mantienen
en `specs/current/<capacidad>.md`. Los expedientes cerrados conservan su ubicación.

Usa el siguiente número libre, con al menos tres dígitos, sin renumerar cambios
existentes. Si hay varios expedientes activos y la petición no identifica uno,
pregunta cuál usar. No elijas por fecha ni mezcles sus tareas.

Las skills se invocan por fase. Pueden seleccionarse automáticamente ante una
petición de esa fase, pero la disponibilidad de las skills no activa el método
en todos los repositorios. `sdd-context` establece la adopción en el proyecto.

## Preparación y contexto existente

La constitución contiene exactamente seis principios acordados con el usuario,
cada uno con una regla y una comprobación observable. Su contenido depende del
proyecto; no hay seis principios universales impuestos por estas skills.
Modificar un principio requiere un acuerdo explícito, su motivo y nueva revisión.

`AGENTS.md` aporta referencias, contexto y comandos concretos. Distingue lo
inspeccionado de lo ejecutado y verificado. Conserva las instrucciones existentes
y las de otros ámbitos aplicables. Si contradicen la constitución, consulta el
conflicto: no establezcas una prioridad nueva ni elimines la instrucción.

En proyectos con código se registra únicamente lo inspeccionado. El código
observado no se convierte automáticamente en un requisito aprobado, y no se
afirma conocer toda la aplicación. En proyectos vacíos, los comandos y decisiones
todavía inexistentes permanecen como pendientes, sin inventar comprobaciones.

## Secuencia, revisiones y aprobación

1. Especificar comportamiento y criterios de aceptación, usando los
   [patrones EARS](../skills/sdd-specify/references/ears.md).
2. Revisar como QA, resolver con el usuario las dudas que afecten al comportamiento
   y actualizar la spec. Una respuesta propuesta por la IA no es una decisión.
3. Planificar sobre la revisión aclarada: solución y estrategia de comprobación.
4. Desglosar tareas trazables y presentar el conjunto para aprobación.
5. Implementar solo el conjunto autorizado, comprobando las condiciones de cada tarea.
6. Validar cada requisito y consolidar únicamente si se puede cerrar el cambio completo.

Cada documento de preparación tiene una revisión entera, empezando por 1.
Registra las revisiones de sus antecedentes. Incrementa la revisión ante cambios
de significado; una corrección ortográfica no necesita nueva aprobación. Cambiar
un RF mantiene su ID y registra el motivo; un ID retirado se conserva como tal y
no se reutiliza. Eliminar un RF para ocultar un fallo requiere revisar el alcance
con el usuario, aclarar, replanificar y volver a aprobar.

La aprobación vive en `tasks.md`: estado, revisiones de constitución, spec,
clarificación, plan y definición de tareas, junto a evidencia de la autorización
real del usuario (mensaje y fecha o referencia de sesión si están disponibles).
El agente puede registrar una autorización recibida; no puede inventarla ni
convertir una casilla o una sugerencia propia en aprobación. Una instrucción
explícita de implementar después de presentar el conjunto puede ser la aprobación;
no se solicita de nuevo una autorización que ya cubre ese mismo conjunto.

Los checkboxes, resultados de tests y notas de avance no cambian por sí solos la
revisión de la definición de tareas. Un cambio sustancial de comportamiento,
contratos, solución, tareas, restricciones o principios invalida los antecedentes
afectados y la aprobación. Antes de seguir, actualiza los documentos dependientes,
repite la clarificación si corresponde y solicita la aprobación del nuevo conjunto.
Las instrucciones superiores y permisos de ejecución siguen siendo aplicables.

Cada fase comprueba sus entradas. Si falta alguna, hay revisiones desfasadas o una
contradicción relevante, explica el bloqueo y conserva el trabajo válido. No
fabrica un documento de una fase anterior ni ejecuta silenciosamente fases extra.

## Trazabilidad y cierre

Cada tarea referencia los RF que ayuda a satisfacer o justifica su carácter de
soporte. Cada RF activo debe tener tareas y verificaciones. El plan identifica
qué tipos de test y escenarios se necesitan; las tareas los concretan y la
validación comprueba las aserciones efectivas y su ejecución.

Las tareas de implementación/tests se completan antes del cierre. Si una tarea
tiene como resultado la propia validación o consolidación, se identifica con
`Fase: validación/cierre` y se completa durante esa fase. No se exige que esté
cerrada antes de ejecutar su propio resultado; sus dependencias sí deben cumplir.

`validation.md` registra por RF sus criterios, tareas, ruta y nombre de los tests,
qué comprueban, comando ejecutado, resultado y huecos. Puede haber varios tests
por RF y un test puede cubrir varios RF. Ni mencionar un ID en un test ni un
resultado global correcto prueban que cubra el requisito completo.

Los estados por RF son `cumple`, `falla`, `sin cobertura` y `no ejecutado`.
Solo `cumple` para todos los RF activos, tareas terminadas con evidencia
(incluidas las de cierre realizadas en esa fase), principios respetados y ausencia
de bloqueos permite declarar `validado` después de terminar la consolidación.
Un chequeo manual puede complementar la evidencia, pero no reemplaza la cobertura
de tests acordada para un RF. Si no puede ejecutarse una comprobación, se informa
el motivo y se deja el cambio abierto. No se rebaja el criterio para cerrar.

Al cerrar, actualiza las capacidades afectadas en `specs/current/` preservando
comportamiento previo compatible y enlazando el expediente de origen. Los RF se
citan con su expediente (`001-nombre/RF-1`), porque los IDs son locales al cambio.
Las capacidades nuevas se crean; las modificaciones y retiradas aprobadas se
integran sin borrar requisitos ajenos. Si una spec vigente contradice el código
o el alcance aprobado, resuelve el conflicto antes de consolidar.

Conserva los expedientes cerrados y sus evidencias. Si una validación posterior
descubre una regresión de un cambio cerrado, registra el hallazgo y abre un nuevo
expediente de corrección; no reescribas el pasado como si no hubiese ocurrido.
