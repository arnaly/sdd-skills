<!-- sdd:context:start -->
## Desarrollo con SDD

Metodología: SDD Skills <versión instalada si se conoce>
Constitución: `docs/constitution.md`, revisión <n>, acordada.

### Contexto del proyecto

- Propósito: <descripción>
- Implementado y observado: <hechos con rutas>
- Deseado: <objetivos>
- Desconocido o pendiente: <lagunas>
- Mapa relevante: <directorios y responsabilidades>
- Convenciones: <las observadas o acordadas>

### Comandos

| Objetivo | Comando y directorio | Evidencia | Resultado o pendiente |
| --- | --- | --- | --- |
| <preparar/ejecutar/verificar> | <comando encontrado> | <inspeccionado/verificado/pendiente> | <resultado y limitaciones> |

### Flujo de cambios

Usar las fases `sdd-specify` → `sdd-clarify` → `sdd-plan` → `sdd-tasks` → aprobación
explícita → `sdd-implement` → `sdd-validate`. La constitución se prepara con
`sdd-constitution`; este contexto se mantiene con `sdd-context`.
Las consultas y trabajos ajenos a desarrollo no requieren abrir un cambio.

- Expedientes: `specs/NNN-descripcion/`, cada uno con `spec.md`,
  `clarifications.md`, `plan.md`, `tasks.md` y, al verificar, `validation.md`.
- Comportamiento vigente verificado: `specs/current/`, por capacidad.
- Resolver dudas de comportamiento antes de planificar. Consultar contradicciones
  con instrucciones existentes o principios, sin reemplazarlos unilateralmente.
- Guardar en `tasks.md` la aprobación real del usuario y las revisiones cubiertas.
  Un cambio sustancial del conjunto requiere actualizarlo y volver a aprobarlo.
- Registrar avance, comandos y resultados para poder retomar en otra sesión.
  Al retomar, identificar el expediente y comprobar antecedentes, aprobación y
  estado real. No escoger arbitrariamente entre varios cambios activos.
- Cerrar solo con todos los RF cubiertos por tests ejecutados con éxito,
  tareas comprobadas y principios respetados. Conservar el expediente al consolidar.

### Pendientes del contexto

<Hechos por verificar o decisiones que todavía no existen; no inventar comandos.>
<!-- sdd:context:end -->
