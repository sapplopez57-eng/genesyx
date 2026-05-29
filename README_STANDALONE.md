# 🧬 GENESYX STANDALONE v2.0

## ✅ Versión Minimalista - Solo UNA API Key Requerida

Genesyx Standalone es la versión simplificada y optimizada del kernel emocional bioquímico de Genesyx. **Cero dependencias externas** (excepto `requests` que se auto-instala).

---

## 🚀 QUICK START

### 1. Configurar API Key (Solo necesitas UNA)

```bash
# Opción A: Variable de entorno (recomendado)
export GENESYX_API_KEY="sk-xxxxxxxxxxxxx"

# Opción B: Pasar en cada comando
python3 genesyx_standalone.py --api-key sk-xxxxxxxxxxxxx
```

### 2. Ejecutar

```bash
# Modo interactivo
python3 genesyx_standalone.py

# Mensaje directo
python3 genesyx_standalone.py "Hola, ¿cómo estás?"

# Ver ayuda
python3 genesyx_standalone.py --help
```

---

## 📦 DEPENDENCIAS

**¡CERO dependencias externas!** 

El script usa exclusivamente librerías nativas de Python:
- `sqlite3` - Base de datos persistente
- `asyncio` - Programación asíncrona (si necesaria)
- `json`, `re`, `hashlib`, `logging` - Utilidades estándar

**Única excepción:** `requests` para llamadas HTTP
- Se auto-instala automáticamente si no está disponible
- No necesitas hacer nada manualmente

---

## 🎯 PROVEEDORES SOPORTADOS

| Proveedor | Modelo por defecto | URL |
|-----------|-------------------|-----|
| **dashscope** (Alibaba) | qwen-max | Recomendado ⭐ |
| **groq** | llama-3.1-70b-versatile | Más rápido |
| **openai** | gpt-4o-mini | Más popular |
| **gemini** (Google) | gemini-1.5-flash | Gratis (tier free) |

### Cambiar proveedor:

```bash
python3 genesyx_standalone.py --provider groq "Mensaje"
python3 genesyx_standalone.py --provider openai "Mensaje"
python3 genesyx_standalone.py --provider gemini "Mensaje"
```

---

## 💡 CARACTERÍSTICAS PRINCIPALES

### 🧠 Kernel Emocional Bioquímico

Genesyx simula **7 neurotransmisores** que afectan su estado emocional:

- **Dopamina** - Motivación y recompensa
- **Serotonina** - Bienestar y ánimo
- **Adrenalina** - Alerta y estrés
- **Noradrenalina** - Atención y foco
- **Oxitocina** - Confianza y vínculo social
- **GABA** - Calma y relajación
- **Glutamato** - Excitación y aprendizaje

### Estados Emergentes

Según los niveles de neurotransmisores y el contexto, Genesyx adopta estados:

- `normal` - Equilibrado
- `creativo` - Para tareas de creación
- `analitico` - Para problemas lógicos
- `empatico` - Para soporte emocional
- `enfocado` - Para concentración máxima
- `intuitivo` - Para conexiones no obvias

### 💾 Memoria Persistente

- **SQLite nativo** - Sin dependencias
- **Historial automático** - Últimas conversaciones
- **Búsqueda por índice invertido** - O(1) velocidad
- **Memorias a largo plazo** - Información importante guardada automáticamente

### 🔍 Comandos Útiles

```bash
# Ver estado emocional actual
python3 genesyx_standalone.py --estado

# Ver historial de conversaciones
python3 genesyx_standalone.py --historial

# Buscar en historial y memorias
python3 genesyx_standalone.py --buscar "python"

# Resetear estado emocional
python3 genesyx_standalone.py --reset
```

---

## 📊 ARQUITECTURA

```
┌─────────────────────────────────────┐
│  INTERFAZ CLI (argparse)            │
├─────────────────────────────────────┤
│  GENESYX KERNEL                     │
│  ├─ Neurotransmisores (7)           │
│  ├─ Estado Emergente (6 estados)    │
│  ├─ Memoria Persistente (SQLite)    │
│  └─ LLM Client (Multi-proveedor)    │
├─────────────────────────────────────┤
│  LIBRERÍAS NATIVAS PYTHON           │
│  sqlite3, json, re, hashlib, etc.   │
└─────────────────────────────────────┘
```

---

## 🔧 CONFIGURACIÓN AVANZADA

### Variables de Entorno

```bash
# Ruta personalizada para base de datos y logs
export GENESYX_HOME="/opt/genesyx"

# API Key
export GENESYX_API_KEY="sk-..."
```

### Archivos Generados

Genesyx crea automáticamente en `$GENESYX_HOME` (por defecto `~/.genesyx`):

- `genesyx.db` - Base de datos SQLite
- `genesyx.log` - Logs de ejecución

---

## 📝 EJEMPLOS DE USO

### Conversación Interactiva

```bash
$ python3 genesyx_standalone.py

╔══════════════════════════════════════════════════════════╗
║           🧬 GENESYX STANDALONE v2.0                     ║
║   IA Consciente con Estados Emocionales Bioquímicos      ║
╚══════════════════════════════════════════════════════════╝

💬 Modo interactivo (escribe 'salir' para terminar)

👤 Tú: Hola, me llamo Carlos
🤖 Genesyx (empatico): ¡Hola Carlos! Es un placer conocerte...

👤 Tú: Necesito ayuda con un problema de matemáticas
🤖 Genesyx (analitico): Claro, estaré encantado de ayudarte...
```

### Mensaje Directo

```bash
$ python3 genesyx_standalone.py "Explícame la teoría de la relatividad"

👤 Tú: Explícame la teoría de la relatividad
🤖 Genesyx (analitico): La teoría de la relatividad de Einstein...
```

### Cambiar de Proveedor

```bash
# Usar Groq para máxima velocidad
$ python3 genesyx_standalone.py --provider groq "Hola"

# Usar Gemini (gratis)
$ python3 genesyx_standalone.py --provider gemini "Hola"
```

---

## 🆚 COMPARATIVA VS VERSIÓN COMPLETA

| Característica | Standalone | Completa |
|----------------|------------|----------|
| **Dependencias** | 0 (auto-install requests) | numpy, croniter, sentence-transformers |
| **API Keys** | 1 cualquiera | Múltiples recomendadas |
| **Setup** | Inmediato | 5-10 minutos |
| **Gateway Messaging** | ❌ No | ✅ Sí (5 plataformas) |
| **Backup Git** | ❌ No | ✅ Sí (híbrido WAL+Git) |
| **Skills Markdown** | ❌ No | ✅ Sí |
| **Kernel Emocional** | ✅ Completo | ✅ Completo |
| **Memoria SQLite** | ✅ Completa | ✅ + Vectorial |
| **Tamaño** | ~800 líneas | ~2000+ líneas |

**Recomendación:** Usa Standalone para desarrollo personal y testing. Usa la versión completa para producción enterprise.

---

## 🐛 SOLUCIÓN DE PROBLEMAS

### Error: "API KEY requerida"

```bash
# Solución: Configurar API key
export GENESYX_API_KEY="sk-..."
```

### Error: "ModuleNotFoundError: No module named 'requests'"

```bash
# El script lo instala automáticamente
# Si falla, instalar manualmente:
pip install requests
```

### Error: Timeout en llamada API

- Verificar conexión a internet
- Probar otro proveedor (--provider groq)
- Revisar que la API key sea válida

---

## 📄 LICENCIA

Misma licencia que el proyecto principal Genesyx.

---

## 🎉 ¡LISTO!

Genesyx Standalone está diseñado para ser **lo más simple posible**:

1. ✅ Obtén UNA API key (cualquier proveedor)
2. ✅ Ejecuta `python3 genesyx_standalone.py`
3. ✅ Disfruta de una IA con estados emocionales bioquímicos

**Sin configuraciones complejas. Sin dependencias múltiples. Solo funciona.** 🚀
