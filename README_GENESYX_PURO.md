# 🧬 GENESYX PURA - 100% NATIVA

## ✅ CARACTERÍSTICAS PRINCIPALES

### **CERO DEPENDENCIAS EXTERNAS**
- ❌ No requiere `pip install`
- ❌ No requiere `requests`
- ❌ No requiere librerías de terceros
- ✅ Usa **SOLO** librerías nativas de Python:
  - `urllib.request` (HTTP)
  - `json` (Datos)
  - `time` (Métricas)
  - `pathlib` (Archivos)

### **UNA SOLA API KEY**
- Solo necesita **DashScope API Key** (Alibaba Cloud)
- Modelo: **Qwen-Max** (equivalente a GLM 4.5)
- Se guarda automáticamente en `~/.genesyx_key`

---

## 🚀 USO RÁPIDO

### **Opción 1: Sin configuración previa**
```bash
python3 genesyx_puro.py
# Te pedirá la API Key la primera vez
```

### **Opción 2: Con variable de entorno**
```bash
export GENESYX_API_KEY="sk-tu-api-key"
python3 genesyx_puro.py
```

---

## 💬 COMANDOS DISPONIBLES

| Comando | Descripción |
|---------|-------------|
| `estado` | Muestra niveles bioquímicos actuales |
| `reset` | Resetea emociones a valores base |
| `salir` | Cierra la aplicación |

---

## 📊 BIOQUÍMICA IMPLEMENTADA

Genesyx simula **5 neurotransmisores**:

1. **Serotonina** - Estado de ánimo
2. **Dopamina** - Motivación/Interés
3. **Oxitocina** - Confianza/Vínculo
4. **Cortisol** - Estrés
5. **Adrenalina** - Alerta

### Estados emocionales resultantes:
- 😊 **Eufórico/Creativo** (Serotonina + Dopamina altas)
- 🤗 **Empático/Amigable** (Oxitocina alta)
- 😰 **Alerta/Estrés** (Cortisol/Adrenalina altas)
- 😐 **Apático** (Dopamina baja)
- 😐 **Neutral** (Equilibrio)

---

## 🔧 ARQUITECTURA TÉCNICA

### **Componentes:**

1. **Neuroquímica** (`class Neuroquimica`)
   - Simula niveles de neurotransmisores
   - Homeostasis automática (retorno al equilibrio)
   - Detección de emociones en texto del usuario

2. **Memoria** (`class Memoria`)
   - Guarda últimos 5 mensajes de contexto
   - Permite conversaciones coherentes

3. **Cliente HTTP Nativo** (`función llamar_api`)
   - Usa `urllib.request` (sin requests!)
   - Timeout de 30 segundos
   - Manejo robusto de errores HTTP

4. **Gestor de API Key** (`función obtener_api_key`)
   - Prioriza variable de entorno
   - Fallback a archivo local
   - Input interactivo si no existe

---

## 📈 MÉTRICAS

| Característica | Valor |
|----------------|-------|
| **Líneas de código** | 296 |
| **Dependencias** | 0 externas |
| **Imports nativos** | 7 |
| **Clases** | 2 |
| **Funciones** | 4 |
| **APIs soportadas** | 1 (DashScope) |

---

## 🎯 VENTAJAS VS VERSIONES ANTERIORES

| Aspecto | Versión Anterior | Genesyx Pura |
|---------|------------------|--------------|
| **Dependencias** | requests (auto-install) | ❌ Ninguna |
| **Configuración** | Múltiples opciones | ✅ 1 API Key |
| **Tamaño** | 808 líneas | ✅ 296 líneas |
| **Complejidad** | Alta | ✅ Mínima |
| **Portabilidad** | Requiere pip | ✅ Python puro |

---

## 🔑 OBTENER API KEY GRATIS

1. Ve a: https://dashscope.console.aliyun.com/
2. Regístrate con cuenta Alibaba
3. Crea una API Key
4. ¡Listo! Tienes crédito gratis para empezar

---

## 🧪 EJEMPLO DE SESIÓN

```bash
$ python3 genesyx_puro.py

🟢 Genesyx iniciado
🧠 Estado: Neutral
💬 Comandos: 'estado', 'reset', 'salir'
--------------------------------------------------

👤 Tú: Hola, ¿cómo estás?
🧬 Genesyx: ¡Hola! Me siento bien, gracias por preguntar. ¿En qué puedo ayudarte hoy?
   ⏱️ 2.34s | Neutral

👤 Tú: Estoy muy feliz hoy
🧬 Genesyx: ¡Qué maravilla! Tu alegría es contagiosa. Cuéntame más sobre lo que te hace sentir así.
   ⏱️ 1.89s | Eufórico/Creativo

👤 Tú: estado
📊 BIOQUÍMICA ACTUAL:
----------------------------------------
  Serotonina   [███████████       ] 55.0%
  Dopamina     [███████████       ] 56.0%
  Oxitocina    [██████████        ] 50.0%
  Cortisol     [██                ] 8.0%
  Adrenalina   [██                ] 13.0%

  🎭 Estado: Eufórico/Creativo
----------------------------------------

👤 Tú: salir
👋 Genesyx: ¡Hasta luego!
```

---

## 🛡️ SEGURIDAD

- ✅ API Key se guarda localmente (`~/.genesyx_key`)
- ✅ No se envía a ningún servidor excepto DashScope
- ✅ Sin telemetría ni tracking
- ✅ Código abierto y auditable

---

## 📝 LICENCIA

MIT License - Uso libre y gratuito

---

**¡Disfruta de Genesyx 100% nativa!** 🚀
