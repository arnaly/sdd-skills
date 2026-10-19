---
name: sdd-plan
description: "Planifica técnicamente un cambio SDD ya aclarado, definiendo módulos, datos, contratos, algoritmos y verificación sin comenzar la implementación."
---

# Planificación técnica

## Entrada

Identifica el expediente y lee instrucciones aplicables, constitución acordada,
spec, clarificación y capacidades vigentes afectadas. Comprueba que la clarificación
está resuelta y corresponde a la revisión actual de spec. Si faltan documentos,
quedan decisiones de comportamiento o hay contradicciones, explica el bloqueo;
no rellenes respuestas para poder planificar.

## Procedimiento

1. Inspecciona los módulos y herramientas existentes que afectan al cambio. Separa
   datos verificados de propuestas; conserva convenciones compatibles y contrasta
   la solución con los seis principios.
2. Escribe `plan.md` siguiendo la [plantilla](assets/plan.md). Define módulos y
   responsabilidades, datos, interfaces/contratos, flujos y algoritmos solo donde
   sean pertinentes. El contrato puede ser API, CLI, UI u otro; no impongas una CLI
   ni un algoritmo de rachas por los ejemplos usados para explicar el método.
3. Registra decisiones técnicas con motivo y alternativas relevantes. Resuelve con
   el usuario las que cambien alcance, restricciones o compromisos importantes.
   Un cambio de comportamiento vuelve a spec y clarificación.
4. Define estrategia de verificación por RF: tipos de test, casos positivos,
   negativos y límites relevantes; controles de principios, regresión y contratos.
   Si faltan herramientas de test, incluye cómo prepararlas o plantea el bloqueo;
   no sustituyas los tests requeridos por una futura comprobación manual vaga.
5. Incluye migraciones, compatibilidad y recuperación cuando el cambio las necesite.
   No añadas despliegues ni acciones remotas por defecto. Referencia las revisiones
   de constitución, spec y clarificación; incrementa la del plan al cambiarlo
   sustancialmente e invalida tareas y aprobación afectadas.

## Salida y límite

Entrega plan, decisiones y correspondencia con los RF. Deja explícitos los bloqueos;
solo un plan listo permite desglosar tareas. Esta fase no implementa, no marca tests
como ejecutados ni solicita otra vez decisiones de producto ya resueltas. La
aprobación del conjunto se solicita tras preparar las tareas.
