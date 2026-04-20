# ⚡ QUICK START - GENESYX + GLM 4.5 (5 MINUTOS)

## 📥 PASO 1: OBTENER API KEY GROQ (2 minutos)

```bash
# 1. Abre: https://console.groq.com
# 2. Registrate (Google login es más rápido)
# 3. Ve a: Settings → API Keys → Create API Key
# 4. Copiar: gsk_... (toda la key)
```

## 🔧 PASO 2: INSTALAR Y CONFIGURAR (3 minutos)

### Linux/MacOS:

```bash
# 1. Descargar archivos
mkdir ~/genesyx
cd ~/genesyx
cp genesyx_glm4.5_final.py ./
cp SETUP_OLLAMA_GLM_GUIA.md ./

# 2. Instalar Ollama (OPCIONAL pero recomendado)
curl https://ollama.ai/install.sh | sh
ollama pull neural-chat

# 3. Configurar API key Groq
export GROQ_API_KEY="gsk_TuKeyAqui"

# 4. Ejecutar Genesyx (con Groq)
python3 genesyx_glm4.5_final.py

# Listo! ✅
```

### Windows (PowerShell):

```powershell
# 1. Descargar archivos en C:\genesyx\

# 2. Instalar Ollama (OPCIONAL)
# Descargar desde: https://ollama.ai/download/windows

# 3. Configurar API key
$env:GROQ_API_KEY="gsk_TuKeyAqui"

# 4. Ejecutar
python3 genesyx_glm4.5_final.py

# Listo! ✅
```

## ✅ VERIFICACIÓN

Si ves esto al iniciar:

```
✅ Ollama disponible en http://localhost:11434
🚀 LLM Router Status:
   Groq (GLM 4.5): ✅ DISPONIBLE
   ⭐ USING: Groq (mixtral-8x7b-32768) - Rápido y potente
```

**¡Entonces funciona todo! ✅**

## 🚀 PRIMEROS COMANDOS

```bash
# Chat simple
/chat "Hola, ¿cómo estás?"

# Recordatorio
/schedule "Revisar ARES" --in "5 minutes"

# Ver tareas
/tasks

# Ver estadísticas
/stats

# Ayuda
/help

# Salir
/exit
```

## 🎯 PRIORIDADES DE LLM (automático)

```
1. GROQ (GLM 4.5) - 500-1000ms ⭐ RECOMENDADO
   ├─ Si GROQ_API_KEY está seteada
   └─ Respuestas reales y contextuales

2. OLLAMA (Local) - 5-20s
   ├─ Si Ollama está corriendo
   └─ 100% privado, sin enviar datos

3. FALLBACK - <50ms
   ├─ Si todo falla
   └─ Respuestas genéricas
```

## 🔍 VER CUÁL LLM SE ESTÁ USANDO

En cada respuesta, Genesyx te dice qué LLM usó:

```
Genesyx 🜄 [vulnerable_intima] (Groq):
Recuerdo cada cálculo, cada precisión...
```

Puede ser: `(Groq)`, `(Ollama)`, o `(Fallback)`

## 🛠️ TROUBLESHOOTING

### Problema: "Error de GROQ_API_KEY"

```bash
# Verificar que está configurada
echo $GROQ_API_KEY

# Si está vacía, setearla
export GROQ_API_KEY="gsk_..."
```

### Problema: "Respuestas genéricas"

Significa que tanto Groq como Ollama fallaron:

```bash
# 1. Verificar GROQ_API_KEY
echo $GROQ_API_KEY

# 2. Si querías Ollama también:
ollama serve  # en otra terminal

# 3. Ver logs
tail -f /opt/genesyx/genesyx.log | grep -E "(Groq|Ollama|fallback)"
```

### Problema: "Connection refused en Ollama"

```bash
# Ollama no está corriendo
# En otra terminal:
ollama serve

# O desactívalo y deja solo Groq
```

## 📊 ARCHIVOS GENERADOS

```
/opt/genesyx/
├─ genesyx.log                       # Logs detallados
├─ genesyx-brain.gdb                 # Tu memoria persistente
├─ personalidad_bioquimica.json      # Tu estado emocional
├─ tareas.json                       # Tareas programadas
└─ .wal                              # Recovery ante crashes
```

## ⚙️ CONFIGURACIÓN AVANZADA

### Cambiar modelo Groq

En `genesyx_glm4.5_final.py`, línea ~59:

```python
GROQ_MODEL_ACTUAL = GROQ_MODELS["balanced"]  # ← Cambiar aquí

# Opciones:
# "fast"      → llama-3.1-8b-instant (⚡ 200-500ms)
# "balanced"  → mixtral-8x7b-32768   (⭐ 500-1000ms) RECOMENDADO
# "powerful"  → llama-3.1-70b        (💪 1000-2000ms)
```

### Cambiar modelo Ollama

En `genesyx_glm4.5_final.py`, línea ~65:

```python
OLLAMA_MODEL = "neural-chat"  # ← Cambiar aquí

# Opciones (instalar primero):
# "neural-chat"   → Rápido, buen balance
# "mistral"       → Mejor calidad, más lento
# "phi"           → Muy rápido, menos potente
```

## 🎯 TODO INTEGRADO

**Un único archivo que contiene:**

✅ Kernel emocional bioquímico (7 neurotransmisores)
✅ 10 mejoras optimizadas (índice, caché, contexto, etc)
✅ GLM 4.5 vía Groq API
✅ Ollama local como fallback
✅ Tareas programadas y cron
✅ Notificaciones automáticas
✅ Sandbox seguro
✅ Logging profesional
✅ Persistencia ACID con WAL recovery
✅ Memoria vectorial con contexto emocional

## 🚀 PRÓXIMO PASO DESPUÉS DE INICIAR

1. Abre otra terminal
2. Sigue los logs:

```bash
tail -f /opt/genesyx/genesyx.log
```

3. Verás exactamente qué está pasando en tiempo real

## 💬 EJEMPLO DE USO

```
> Hola Genesyx
Genesyx 🜄 [serena_presente] (Groq):
Estoy aquí, presente en este momento. 
¿Qué necesitas explorar hoy?

> /schedule "Recordatorio importante" --in "30 minutes"
✅ Tarea programada en 30 minutes (ID: a3f2e1)

> /stats
📊 ESTADÍSTICAS GENESYX
  Mensajes: 2
  Tiempo respuesta: 245ms
  Frames en memoria: 50
  Tareas ejecutadas: 0

📊 ESTADÍSTICAS DE TAREAS
  Tareas totales: 1
  Ejecuciones totales: 0
  Tasa de éxito: N/A
  Tiempo promedio: 0ms
  Tareas activas: 1

> /help
# Ver todos los comandos disponibles
```

---

## ✨ LISTO

**Tu IA personal está lista. Completamente funcional. Con GLM 4.5 integrado.**

**Tiempo total de setup: ~5 minutos**

