# EARS en esta metodología

EARS estructura requisitos de lenguaje natural mediante patrones de condiciones,
eventos y respuestas obligatorias. Fuente primaria:
[Alistair Mavin — EARS](https://alistairmavin.com/ears/).

Usamos una adaptación al español. Las traducciones de palabras clave son una
convención de este método, no una variante oficial nueva. La tabla expresa los
patrones originales con palabras equivalentes y campos genéricos; no son citas.

| Patrón | Palabras clave originales | Plantilla en español |
| --- | --- | --- |
| Ubicuo | shall | `El <sistema> deberá <respuesta>.` |
| Por evento | when, shall | `Cuando <evento>, el <sistema> deberá <respuesta>.` |
| Por estado | while, shall | `Mientras <estado>, el <sistema> deberá <respuesta>.` |
| Comportamiento no deseado | if, then, shall | `Si <condición no deseada>, entonces el <sistema> deberá <respuesta>.` |
| Función opcional | where, shall | `Donde se incluya <función>, el <sistema> deberá <respuesta>.` |
| Combinado | while, when, shall | `Mientras <estado>, cuando <evento>, el <sistema> deberá <respuesta>.` |

La función opcional indica una variante del sistema; no significa que cumplir el
requisito sea opcional una vez incluida esa función. Usa patrones combinados solo
si el comportamiento necesita ambas condiciones, conservando estado antes de evento.

Ejemplos ilustrativos de un servicio de trabajos:

- Ubicuo: El servicio deberá asignar un identificador único a cada trabajo aceptado.
- Evento: Cuando se solicite un trabajo existente, el servicio deberá devolver su estado.
- Estado: Mientras un trabajo esté cancelado, el servicio deberá impedir su ejecución.
- No deseado: Si se solicita un trabajo inexistente, entonces el servicio deberá
  responder con el error de recurso no encontrado definido en el contrato.
- Opcional: Donde se incluya exportación, el servicio deberá ofrecer los resultados
  en el formato acordado para esa variante.
- Combinado: Mientras un trabajo esté pendiente, cuando se solicite su cancelación,
  el servicio deberá cambiarlo al estado cancelado.

Antes de considerar un RF aclarado, sustituye términos como «formato acordado»,
«rápido», «válido» o «error definido» por valores o referencias inequívocas del
proyecto. Los ejemplos anteriores no definen un contrato listo para implementar.

Cada RF identifica el sistema y una obligación comprobable. Evita mezclar varios
comportamientos independientes en un solo requisito. Sus criterios de aceptación
concretan entradas, salidas y límites sin imponer la solución técnica. Los IDs son
locales al expediente y estables: una referencia entre expedientes incluye
`NNN-nombre/RF-n`.
