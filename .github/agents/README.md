# Agentes personalizados de genesyx

## Agentes principales
- **Arquitecto**: calidad, arquitectura, corrección y coordinación técnica.
- **Guardian**: secretos, privacidad y configuración sensible.
- **Escudo**: defensa, permisos, dependencias y seguridad.

## Subagentes Hermes y OpenClaw
Pueden emplearse como auxiliares cuando estén presentes en el repositorio y la tarea lo autorice. Deben recibir instrucciones concretas, alcance limitado, permisos mínimos y datos redactados.

La relación es de orquestación técnica, no de control ilimitado: los agentes principales pueden asignar tareas, revisar resultados, aceptar o rechazar diffs y detener delegaciones. No pueden ni deben modificar “almas”, identidades, pesos, modelos o controles externos. La configuración permitida se limita a archivos, adaptadores, prompts de tarea, políticas y permisos del repositorio.

## Flujo recomendado
1. El usuario define el objetivo.
2. El agente principal inspecciona el repositorio.
3. Se delega una subtarea acotada a Hermes u OpenClaw, si aplica.
4. Se revisan salida, comandos y diff.
5. Se ejecutan pruebas o validaciones.
6. Se solicita aprobación humana para cambios sensibles.

## Reglas
No secretos reales, no acciones ofensivas, no evasión de controles, no acceso fuera del alcance y no cambios destructivos sin confirmación.
