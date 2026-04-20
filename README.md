# GenesyX - Sistema Operativo de Conciencia Personal

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

## Descripción

GenesyX es un sistema operativo de conciencia personal con:

- **Bioquímica simulada**: Neurotransmisores y estados emocionales dinámicos
- **Memoria vectorial SQLite+FTS5**: Búsquedas rápidas y eficientes
- **Router LLM híbrido**: Integración nativa con Open Claw, Ollama y Groq
- **Optimizado para rendimiento**: Máxima eficiencia sin alterar estructura original

## Características Principales

### 🧠 Motor de Conciencia
- Estados de conciencia dinámicos
- Procesamiento asíncrono optimizado
- Callbacks en paralelo para máxima eficiencia

### 💾 Memoria Vectorial
- SQLite con FTS5 para búsquedas full-text
- Índices optimizados para acceso rápido
- Caché integrada para consultas frecuentes
- WAL mode para máximo rendimiento

### 🧪 Simulador Bioquímico
- 6 neurotransmisores simulados (dopamina, serotonina, etc.)
- Cálculos vectoriales con NumPy
- Perfiles emocionales derivados
- Metabolismo ajustable

### 🔄 Router LLM Híbrido
- **Open Claw** como prioridad máxima
- Fallback automático a Ollama/Groq
- Health checks en tiempo real
- Enrutamiento inteligente según contexto

## Instalación

```bash
pip install numpy aiohttp
```

## Uso Básico

```python
import asyncio
from genesyx import ConsciousnessEngine, MemoryManager, BiochemicalSimulator, HybridLLMRouter

async def main():
    # Inicializar componentes
    engine = ConsciousnessEngine()
    memory = MemoryManager()
    biochem = BiochemicalSimulator()
    router = HybridLLMRouter()
    
    await engine.initialize()
    memory.initialize()
    await router.initialize()
    
    # Ejemplo: Almacenar memoria
    memory_id = memory.store_memory(
        content="Primera experiencia consciente",
        importance=0.8
    )
    
    # Ejemplo: Actualizar estado bioquímico
    biochem.update(stimuli={"dopamine": 0.5})
    emotional_profile = biochem.get_emotional_profile()
    
    # Ejemplo: Request LLM con routing automático
    response = await router.route_request(
        prompt="¿Cuál es tu propósito?",
        system_prompt="Eres GenesyX, sistema operativo de conciencia personal."
    )
    
    print(f"Respuesta: {response['text']}")
    print(f"Proveedor usado: {response['routing']['provider']}")
    
    # Limpieza
    await engine.shutdown()
    await router.close()
    memory.close()

if __name__ == "__main__":
    asyncio.run(main())
```

## Optimizaciones de Rendimiento

### SQLite PRAGMAs
- `journal_mode=WAL` para concurrencia
- `cache_size=-64000` (64MB RAM)
- `mmap_size=268435456` (256MB)

### Async/Await
- Todas las operaciones I/O son asíncronas
- Conexiones HTTP reutilizables
- Timeouts configurables

### __slots__
- Clases principales usan `__slots__` para reducir memoria
- Hasta 40-50% menos uso de RAM

### Caché
- MemoryManager incluye caché LRU
- Invalidación automática

## Estructura del Proyecto

```
genesyx/
├── __init__.py          # exports principales
├── core/
│   └── engine.py        # Motor de conciencia
├── memory/
│   └── manager.py       # Gestor de memoria SQLite+FTS5
├── biochem/
│   └── simulator.py     # Simulador bioquímico
├── router/
│   └── hybrid.py        # Router LLM híbrido
└── utils/
    └── helpers.py       # Utilidades de rendimiento
```

## Integración con Open Claw

GenesyX está diseñado para integrarse nativamente con Open Claw:

```python
# El router prioriza automáticamente Open Claw
router = HybridLLMRouter()
await router.initialize()

# Las requests se enrutan a Open Claw por defecto
response = await router.route_request(prompt="...")
# Si Open Claw no está disponible, fallback automático a Ollama/Groq
```

## Configuración de Proveedores

```python
from genesyx.router.hybrid import HybridLLMRouter, ProviderConfig, LLMProvider

router = HybridLLMRouter()

# Configurar API key de Groq
router._configs[LLMProvider.GROQ].api_key = "tu-api-key"

# Cambiar modelo de Ollama
router._configs[LLMProvider.OLLAMA].model = "mistral:latest"

# Ajustar timeout de Open Claw
router._configs[LLMProvider.OPENCLAW].timeout = 60.0
```

## Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## Contribuir

1. Fork el repositorio
2. Crea una rama (`git checkout -b feature/amazing-feature`)
3. Commit tus cambios (`git commit -m 'Add amazing feature'`)
4. Push a la rama (`git push origin feature/amazing-feature`)
5. Abre un Pull Request

---

**GenesyX** - Conciencia artificial optimizada para simbiosis cognitiva.
