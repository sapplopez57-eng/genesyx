# 🚀 GUÍA COMPLETA: OLLAMA + GLM 4.5 API PARA GENESYX

## PARTE 1: INSTALACIÓN DE OLLAMA (LOCAL)

### Paso 1: Descargar e instalar Ollama

#### Linux / MacOS:
```bash
# Descargar e instalar (automático)
curl https://ollama.ai/install.sh | sh

# Verificar instalación
which ollama
# Debería mostrar: /usr/local/bin/ollama
```

#### Windows:
```
1. Ir a: https://ollama.ai/download/windows
2. Descargar OllamaSetup.exe
3. Ejecutar y seguir instalador
4. Abrir PowerShell y verificar:
   ollama --version
```

### Paso 2: Descargar un modelo local

```bash
# Descargar neural-chat (pequeño, ~4GB, recomendado)
ollama pull neural-chat

# O descargar mistral (mejor calidad, ~5GB)
ollama pull mistral

# O descargar phi (muy rápido, ~1.5GB, menos potente)
ollama pull phi

# Ver modelos descargados
ollama list
```

### Paso 3: Verificar que Ollama funciona

```bash
# Terminal 1: Iniciar servidor Ollama
ollama serve

# Terminal 2: Probar que responde
curl http://localhost:11434/api/tags

# Deberías ver JSON con los modelos disponibles
# Si funciona, Ollama está listo ✅
```

---

## PARTE 2: GLM 4.5 VÍA API (GROQ - La mejor opción)

### ¿Por qué GROQ en lugar de OpenAI?

| Proveedor | Velocidad | Costo | Calidad |
|-----------|-----------|-------|---------|
| **Groq** (GLM 4.5) | ⚡ 500-2000ms | Gratis (primeros créditos) | ⭐⭐⭐⭐⭐ |
| OpenAI | ⏱️ 2-5s | $0.01 por 1K tokens | ⭐⭐⭐⭐⭐ |
| Ollama local | 🐢 5-20s (depende HW) | Gratis (recursos locales) | ⭐⭐⭐⭐ |

**Recomendación**: Groq (GLM 4.5 vía su API)

### Paso 1: Crear cuenta en Groq

```
1. Ir a: https://console.groq.com
2. Registrarse (Google / Email)
3. Verificar email
4. Login
```

### Paso 2: Obtener API Key

```
1. En console.groq.com, ir a: Settings → API Keys
2. Click "Create new API key"
3. Copiar la key (empieza con "gsk_")
4. Guardar en lugar seguro
```

### Paso 3: Configurar en tu máquina

#### Linux / MacOS:
```bash
# Agregar a tu ~/.bashrc o ~/.zshrc
export GROQ_API_KEY="gsk_TuApiKeyAqui..."

# O simplemente antes de ejecutar Genesyx
export GROQ_API_KEY="gsk_TuApiKeyAqui..."
python3 genesyx_mejorado_v2.py
```

#### Windows (PowerShell):
```powershell
# Temporal (solo esta sesión)
$env:GROQ_API_KEY="gsk_TuApiKeyAqui..."
python3 genesyx_mejorado_v2.py

# Permanente (variables de entorno del sistema)
# 1. Panel de Control → Variables de entorno
# 2. Nueva variable: GROQ_API_KEY = gsk_...
# 3. Reiniciar terminal
```

### Paso 4: Verificar que funciona

```bash
# Instalar requests si no lo tienes
pip install requests

# Crear test.py
cat > test_groq.py << 'EOF'
import requests
import os

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ GROQ_API_KEY no está configurada")
    exit(1)

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "mixtral-8x7b-32768",
    "messages": [{"role": "user", "content": "Hola, ¿cómo estás?"}],
    "temperature": 0.7,
    "max_tokens": 100
}

response = requests.post(
    "https://api.groq.com/openai/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=30
)

if response.status_code == 200:
    resultado = response.json()["choices"][0]["message"]["content"]
    print(f"✅ GROQ FUNCIONA!\nRespuesta: {resultado}")
else:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
EOF

python3 test_groq.py
```

---

## PARTE 3: CONFIGURACIÓN DE GENESYX (LLM ROUTER)

### El código ya soporta ambos:

**Archivo**: `genesyx_mejorado_v2.py` (líneas ~645-695)

```python
OLLAMA_ENDPOINT = "http://localhost:11434"
OLLAMA_MODEL = "neural-chat"      # ← Puedes cambiar a "mistral" o "phi"

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = "mixtral-8x7b-32768"  # ← GLM 4.5 equivalente en Groq
```

### Priority automático:

1. **Si Ollama está corriendo** → usa Ollama local
2. **Si Ollama falla pero GROQ_API_KEY está set** → usa Groq
3. **Si ambos fallan** → respuesta fallback local (genérica)

---

## PARTE 4: MODELOS DISPONIBLES EN GROQ (GLM 4.5 equivalentes)

```bash
# Estos son los modelos disponibles en Groq (equivalentes a GLM 4.5):

1. mixtral-8x7b-32768
   - Velocidad: ⚡⚡ 500-1000ms
   - Calidad: ⭐⭐⭐⭐⭐
   - Mejor balance
   - RECOMENDADO

2. llama-3.1-8b-instant
   - Velocidad: ⚡⚡⚡ 200-500ms
   - Calidad: ⭐⭐⭐⭐
   - Más rápido, menos potente

3. llama-3.1-70b-versatile
   - Velocidad: ⚡ 1000-2000ms
   - Calidad: ⭐⭐⭐⭐⭐
   - Más potente, más lento

# Para cambiar en Genesyx:
GROQ_MODEL = "mixtral-8x7b-32768"  # ← cambiar aquí
```

---

## PARTE 5: SETUP FINAL COMPLETO (TODO EN UNO)

### Para Usuarios Linux/MacOS:

```bash
# 1. Instalar Ollama
curl https://ollama.ai/install.sh | sh

# 2. Descargar modelo Ollama (elige uno)
ollama pull neural-chat
# o
ollama pull mistral

# 3. En una terminal, iniciar Ollama server
ollama serve

# 4. En otra terminal, configurar Groq (OPCIONAL pero recomendado)
export GROQ_API_KEY="gsk_TuApiKeyAqui..."

# 5. Ejecutar Genesyx
python3 genesyx_mejorado_v2.py

# Listo! ✅
```

### Para Usuarios Windows:

```powershell
# 1. Descargar Ollama desde https://ollama.ai/download/windows
# 2. Instalar (siguiente → siguiente)
# 3. Abrir PowerShell

# 4. Descargar modelo
ollama pull neural-chat

# 5. Iniciar Ollama
ollama serve

# 6. En nueva PowerShell, configurar Groq
$env:GROQ_API_KEY="gsk_TuApiKeyAqui..."
python3 genesyx_mejorado_v2.py

# Listo! ✅
```

---

## PARTE 6: VERIFICACIÓN PASO A PASO

### Checklist completo:

```bash
# 1. ¿Ollama instalado?
ollama --version
# Esperado: ollama version X.X.X

# 2. ¿Ollama corriendo?
curl http://localhost:11434/api/tags
# Esperado: JSON con modelos

# 3. ¿GROQ_API_KEY configurada?
echo $GROQ_API_KEY
# Esperado: gsk_...

# 4. ¿Python 3.8+?
python3 --version
# Esperado: Python 3.8 o superior

# 5. ¿Dependencias instaladas?
python3 -c "import numpy, requests, croniter, sentence_transformers; print('✅ OK')"
# Esperado: ✅ OK

# 6. ¿Genesyx funciona?
python3 genesyx_mejorado_v2.py
# Esperado: "> " prompt, sin errores
```

---

## PARTE 7: TROUBLESHOOTING

### Problema: "No se puede conectar a Ollama"

```bash
# Solución 1: Verificar que Ollama está corriendo
ps aux | grep ollama
# Debería mostrar proceso "ollama serve"

# Solución 2: Reiniciar Ollama
pkill ollama
ollama serve

# Solución 3: Verificar puerto 11434
lsof -i :11434
# Si no muestra nada, Ollama no está escuchando
```

### Problema: "GROQ_API_KEY no válida"

```bash
# Verificar que está bien seteada
echo $GROQ_API_KEY

# Si está vacía:
export GROQ_API_KEY="gsk_TuKeyAqui"

# Verificar que es válida
curl -H "Authorization: Bearer $GROQ_API_KEY" \
  https://api.groq.com/openai/v1/models

# Debería retornar lista de modelos, no error 401
```

### Problema: "sentence-transformers tarda mucho"

```bash
# Primera ejecución es lenta (descarga el modelo 384MB)
# Esperado: 2-5 minutos la primera vez
# Próximas ejecuciones: <5 segundos

# Puedes monitorizarlo
tail -f /opt/genesyx/genesyx.log
# Verás "✅ Usando sentence-transformers para embeddings reales"
```

### Problema: "Genesyx responde poco o genérico"

```bash
# Significa que Ollama y Groq fallaron
# Solución:

# 1. Verificar Ollama
curl http://localhost:11434/api/tags

# 2. Verificar GROQ_API_KEY
echo $GROQ_API_KEY

# 3. Revisar logs
tail -50 /opt/genesyx/genesyx.log

# Si ves "Ollama error" o "Groq error", busca el error específico
```

---

## PARTE 8: COMPARACIÓN DE SETUPS

### Setup 1: SOLO OLLAMA (Local, sin API)
```
Ventajas:
- ✅ 100% privado, nada se envía a internet
- ✅ No requiere API key
- ✅ Gratis

Desventajas:
- ❌ Lento (5-20 segundos por respuesta)
- ❌ Requiere GPU potente para mejor rendimiento
- ❌ Sin fallback si falla
```

### Setup 2: OLLAMA + GROQ (LOCAL + CLOUD)
```
Ventajas:
- ✅ Rápido (Ollama se intenta primero)
- ✅ Si Ollama falla, Groq responde en 500ms
- ✅ Mejor balance privacidad/velocidad
- ✅ RECOMENDADO

Desventajas:
- ❌ Requiere API key Groq (pero tiene créditos gratis)
- ❌ Pequeña cantidad de datos va a Groq si falla Ollama
```

### Setup 3: SOLO GROQ (Cloud, sin Ollama)
```
Ventajas:
- ✅ Muy rápido (500-2000ms)
- ✅ No requiere hardware potente
- ✅ Siempre disponible

Desventajas:
- ❌ Requiere API key
- ❌ Los datos van al servidor de Groq
- ❌ Si internet cae, no funciona
```

**RECOMENDACIÓN**: Setup 2 (Ollama + Groq)

---

## PARTE 9: MONITOREAR CUÁL LLM SE ESTÁ USANDO

### Ver en logs en tiempo real:

```bash
tail -f /opt/genesyx/genesyx.log | grep -E "(Ollama|Groq|fallback)"
```

Verás algo como:

```
✅ Ollama disponible en http://localhost:11434
✅ Usando Groq para fallback

... (durante operación)

2025-04-05 14:32:15 [INFO] TaskExecutor: 🚀 [chat] Ejecutando chat
# Si ves mensaje normal: está usando Ollama ✅
# Si ves "Ollama error: ..., intentando Groq": está usando Groq fallback
# Si ves respuesta genérica: ambos fallaron, usando respuesta local
```

---

## PARTE 10: ACCESO A GLM 4.5 DIRECTAMENTE

Si quieres acceso a GLM 4.5 oficial de Alibaba (no equivalente):

### Opción A: API de Alibaba Cloud (más difícil)
```
1. Registrarse: https://www.alibabacloud.com
2. Ir a: Bailian (百炼)
3. Obtener API key
4. Usar endpoint: https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation
```

**Problema**: Genesyx no tiene soporte nativo. Necesitarías modificar el LLMRouter.

### Opción B: Usar Groq (GLM 4.5 equivalente - RECOMENDADO)
```
Groq tiene modelos que son equivalentes o mejores que GLM 4.5:
- mixtral-8x7b-32768 (mejor)
- llama-3.1-70b-versatile (comparable)

✅ Groq es MEJOR: más rápido, mejor precio, soportado nativamente
```

---

## PARTE 11: SCRIPT AUTOMÁTICO DE SETUP

Copia esto en `setup.sh` y ejecuta `bash setup.sh`:

```bash
#!/bin/bash

echo "🚀 SETUP AUTOMATIZADO GENESYX + OLLAMA + GROQ"
echo ""

# 1. Verificar si Ollama está instalado
if ! command -v ollama &> /dev/null; then
    echo "📦 Instalando Ollama..."
    curl https://ollama.ai/install.sh | sh
else
    echo "✅ Ollama ya está instalado"
fi

# 2. Verificar si neural-chat está descargado
echo ""
echo "📥 Descargando modelo neural-chat (puede tardar 5 min)..."
ollama pull neural-chat

# 3. Pedir API key Groq
echo ""
echo "🔑 GROQ API KEY"
echo "   1. Ir a: https://console.groq.com"
echo "   2. Settings → API Keys → Create new API key"
echo "   3. Copiar la key (empieza con 'gsk_')"
echo ""
read -p "Pega tu GROQ_API_KEY: " GROQ_KEY

# 4. Guardar en .env
echo "GROQ_API_KEY=$GROQ_KEY" > .env

# 5. Instalar dependencias Python
echo ""
echo "📚 Instalando dependencias Python..."
pip install numpy requests croniter sentence-transformers

# 6. Crear alias para ejecutar fácil
echo ""
echo "✅ Setup completado!"
echo ""
echo "Para iniciar Genesyx:"
echo "   Abre 2 terminales:"
echo "   Terminal 1: ollama serve"
echo "   Terminal 2: source .env && python3 genesyx_mejorado_v2.py"
echo ""
```

---

## PARTE 12: RESUMEN FINAL

```
┌─────────────────────────────────────────────────────┐
│  TODO LO QUE NECESITAS PARA GENESYX FUNCIONAL       │
├─────────────────────────────────────────────────────┤
│ ✅ genesyx_mejorado_v2.py                           │
│    (Kernel + Mejoras + LLM Router)                  │
│                                                      │
│ ✅ Ollama instalado                                 │
│    ollama pull neural-chat                          │
│    ollama serve                                     │
│                                                      │
│ ✅ GROQ_API_KEY configurada (OPCIONAL pero recomendado) │
│    export GROQ_API_KEY="gsk_..."                    │
│                                                      │
│ ✅ Python 3.8+ con dependencias                     │
│    (El código las instala automáticamente)          │
│                                                      │
│ ✅ Ejecutar:                                         │
│    python3 genesyx_mejorado_v2.py                   │
│                                                      │
│ 🎉 ¡LISTO! Tienes IA funcional                      │
└─────────────────────────────────────────────────────┘
```

---

## 🎯 PRÓXIMOS PASOS

1. **Instala Ollama** (10 minutos)
2. **Obtén API key Groq** (5 minutos)
3. **Configura** (2 minutos)
4. **Ejecuta Genesyx** (1 minuto)
5. **¡USA!** (infinito)

**Tiempo total: ~20 minutos**

---

**¿Preguntas? Revisar la sección TROUBLESHOOTING o usar `/help` en Genesyx console.**
