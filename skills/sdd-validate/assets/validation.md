# Validación — <cambio>

Estado: abierto
Revisiones comprobadas: constitución <n>; spec <n>; clarificación <n>; plan <n>;
definición de tareas <n>.
Aprobación vigente: <referencia en tasks.md, o bloqueo>
Estado del código comprobado: <commit si existe y cambios locales relevantes;
si no hay commits, describir archivos/estado y momento de comprobación>

## Trazabilidad RF → tareas → tests → resultado

| RF | Criterios cubiertos | Tareas | Test: ruta y nombre/caso | Aserciones y huecos | Ejecución | Estado |
| --- | --- | --- | --- | --- | --- | --- |
| RF-1 | <criterios> | <Tn> | <test concreto, o ninguno> | <qué demuestra y qué falta> | <comando y resultado, o pendiente> | <cumple/falla/sin cobertura/no ejecutado> |

Incluir todos los RF activos. Varios tests pueden cubrir un RF; un test puede
cubrir varios RF. Si no se cumple todo el RF, su estado no es `cumple`.

## Comprobaciones ejecutadas

| Comando y directorio | Momento/estado comprobado | Resultado y alcance |
| --- | --- | --- |
| <comando> | <estado> | <pasados/fallidos/no ejecutado y limitaciones> |

## Tareas, principios y regresión

- Condiciones «Hecho cuando:» comprobadas: <por tarea y evidencia; distinguir
  implementación/tests de validación/cierre completadas en esta fase>
- Seis principios: <comprobación de P1…P6 y resultado>
- Regresión y contratos: <resultado según plan>
- Bloqueos: <detalle o ninguno>

## Conclusión y consolidación

- RF activos: <n>; cumplen: <n>; fallan: <n>; sin cobertura: <n>; no ejecutados: <n>.
- Tareas comprobadas completas/pendientes: <n/n>.
- Conclusión: abierto
- Acciones pendientes: <detalle>
- Capacidades consolidadas: ninguna mientras el cambio no esté validado.
- Fecha y evidencia de cierre: pendiente

Consolidar cuando todos los RF cumplan, las tareas de implementación/tests estén
comprobadas y no existan principios incumplidos ni bloqueos. Completar las tareas
de validación/cierre durante esta fase. Solo marcar `validado` tras satisfacer
todas las tareas y terminar la consolidación. Conservar el expediente.
