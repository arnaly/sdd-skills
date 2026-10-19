---
name: sdd-context
description: "Prepara o actualiza AGENTS.md para adoptar SDD en un proyecto, con contexto y comandos basados en evidencia y conservando las instrucciones existentes."
---

# Contexto del agente

## Entrada

Lee las instrucciones de agente aplicables y `docs/constitution.md`. La
constitución debe estar acordada y contener seis principios verificables. Si
falta, está en borrador o contradice instrucciones existentes, explica el bloqueo.
No inventes ni apruebes los principios para continuar.

## Procedimiento

1. Inspecciona estructura, manifiestos, configuración, documentación y puntos de
   entrada relevantes. Distingue implementación observada, objetivos y lagunas.
2. Localiza `AGENTS.md` raíz y los de ámbitos afectados. Conserva sus instrucciones,
   anotaciones y organización. Integra el contexto en la sección SDD existente o
   añade una sola sección delimitada siguiendo la [plantilla](assets/context.md).
   Si no existe el archivo raíz, créalo. No cambies instrucciones de subdirectorios
   sin que lo requiera la petición.
3. Documenta propósito, mapa breve, convenciones y comandos de preparación,
   ejecución y verificación encontrados. Para cada comando indica `inspeccionado`,
   `verificado` (con resultado) o `pendiente`. Ejecuta únicamente comprobaciones
   pertinentes permitidas; no declares que un build pasa solo porque existe el script.
4. Añade referencias a la constitución, `specs/current/`, los expedientes
   `specs/NNN-descripcion/` y las ocho fases. Activa el flujo para cambios de código:
   especificar → aclarar → planificar → tareas → aprobación → implementar → validar.
   Las consultas y tareas ajenas a desarrollo no necesitan un expediente.
5. Incluye cómo retomar indicando expediente, cómo conservar aprobación y evidencias
   en `tasks.md`, y que modificar sustancialmente el conjunto exige revisión y nueva
   aprobación. La aprobación se refiere al conjunto presentado, no a futuros cambios.
6. Si aparecen contradicciones, consúltalas en lugar de eliminar instrucciones o
   asignarles una prioridad nueva. No rebajes principios ni permisos de ejecución.

## Salida y límite

Informa qué sección se integró, evidencia inspeccionada/verificada y pendientes.
La activación solo afecta a este proyecto. No cambia su código ni instala skills,
no fuerza un stack y no duplica el contenido completo de la constitución en
`AGENTS.md`. Una segunda ejecución actualiza la misma sección.
