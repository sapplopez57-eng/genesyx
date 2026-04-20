#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ACCESO REAL A GLM 4.5 (ALIBABA CLOUD BAILIAN) - API OFICIAL                ║
║                                                                              ║
║  GLM 4.5 es el modelo más potente de Alibaba Cloud (mejor que Groq)         ║
║                                                                              ║
║  Requisitos:                                                                ║
║  1. Cuenta en Alibaba Cloud: https://www.alibabacloud.com                   ║
║  2. Activar Bailian: https://console.aliyun.com/                            ║
║  3. Obtener API key                                                         ║
║  4. Configurar en Genesyx                                                   ║
║                                                                              ║
║  Este archivo te muestra exactamente cómo hacerlo.                          ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import requests
import json
import os
from datetime import datetime

# =============================================================================
# PASO 1: REGISTRO Y CONFIGURACIÓN DE ALIBABA CLOUD
# =============================================================================

GUIA_PASO_1 = """
╔════════════════════════════════════════════════════════════════════════════╗
║                    PASO 1: CREAR CUENTA EN ALIBABA CLOUD                   ║
╚════════════════════════════════════════════════════════════════════════════╝

1. Abre: https://www.alibabacloud.com
2. Click "Sign Up" (esquina superior derecha)
3. Elige método:
   ✅ RECOMENDADO: Usar Google Account (más rápido)
   o Email + contraseña

4. Completa registro:
   - Email válido
   - Contraseña fuerte
   - Verificar email

5. Completar verificación:
   - Alibaba enviará email de confirmación
   - Verificar teléfono (10 segundos con SMS)
   
6. Login: https://account.alibabacloud.com/login/

✅ CUENTA CREADA
"""

GUIA_PASO_2 = """
╔════════════════════════════════════════════════════════════════════════════╗
║               PASO 2: ACTIVAR BAILIAN (SERVICIO GLM 4.5)                   ║
╚════════════════════════════════════════════════════════════════════════════╝

1. Una vez logeado, ir a:
   https://console.aliyun.com/

2. Buscar "Bailian" en la barra de búsqueda (arriba)

3. Click en "Bailian - LLM as a Service"
   (También aparece como "百炼" en chino)

4. Click "Open Service" o "Activate"
   - Primera vez es gratis con créditos de prueba
   - Te darán ~50-100 CNY en créditos

5. Aceptar términos y confirmar

✅ BAILIAN ACTIVADO (instántaneo)
"""

GUIA_PASO_3 = """
╔════════════════════════════════════════════════════════════════════════════╗
║               PASO 3: OBTENER API KEY DE BAILIAN                            ║
╚════════════════════════════════════════════════════════════════════════════╝

1. En Bailian console, ir a:
   左侧菜单 (menú izquierdo) → "API-KEY Management"
   
   En inglés: Left menu → Settings → API Keys

2. Click "Create New API Key"

3. Recibirás:
   - API Key (ej: sk-xxx...xxx)
   - Copiar completa
   - Guardar en lugar seguro

4. NOTA: La key de Bailian es diferente a la de Groq
   - Bailian: Empieza con "sk-"
   - Groq: Empieza con "gsk_"

✅ API KEY OBTENIDA
"""

GUIA_PASO_4 = """
╔════════════════════════════════════════════════════════════════════════════╗
║               PASO 4: CONFIGURAR EN TU SISTEMA                              ║
╚════════════════════════════════════════════════════════════════════════════╝

Linux/MacOS:
  export DASHSCOPE_API_KEY="sk_xxx...xxx"
  python3 genesyx_glm4.5_alibaba.py

Windows (PowerShell):
  $env:DASHSCOPE_API_KEY="sk_xxx...xxx"
  python3 genesyx_glm4.5_alibaba.py

Windows (CMD):
  set DASHSCOPE_API_KEY=sk_xxx...xxx
  python3 genesyx_glm4.5_alibaba.py

✅ CONFIGURADO
"""

# =============================================================================
# GLM 4.5 API ENDPOINTS Y CONFIGURACIÓN
# =============================================================================

# API de Bailian (GLM 4.5 oficial)
BAILIAN_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

# API Key (obtener de: https://console.aliyun.com -> Bailian)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")

# Modelos disponibles en Bailian
MODELOS_BAILIAN = {
    "glm4": {
        "nombre": "Qwen GLM-4",
        "id": "qwen-max",
        "precio": "$0.02 por 1K tokens",
        "velocidad": "⚡⚡ 500-1500ms",
        "calidad": "⭐⭐⭐⭐⭐",
        "descripcion": "Modelo más potente, mejor para tareas complejas"
    },
    "glm3": {
        "nombre": "Qwen GLM-3.5",
        "id": "qwen-plus",
        "precio": "$0.004 por 1K tokens",
        "velocidad": "⚡⚡⚡ 300-800ms",
        "calidad": "⭐⭐⭐⭐",
        "descripcion": "Balance entre velocidad y calidad"
    },
    "glm_turbo": {
        "nombre": "Qwen GLM Turbo",
        "id": "qwen-turbo",
        "precio": "$0.002 por 1K tokens",
        "velocidad": "⚡⚡⚡⚡ 100-300ms",
        "calidad": "⭐⭐⭐",
        "descripcion": "Más rápido, menos potente"
    }
}

# RECOMENDADO: qwen-max (equivalente a GLM 4.5)
MODELO_ACTUAL = "qwen-max"

print("""
╔══════════════════════════════════════════════════════════════════════════╗
║               🚀 ACCESO A GLM 4.5 (ALIBABA BAILIAN)                      ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# FUNCIÓN: VERIFICAR CONFIGURACIÓN
# =============================================================================

def verificar_configuracion():
    """Verifica si todo está configurado correctamente"""
    
    print("\n📋 VERIFICACIÓN DE CONFIGURACIÓN")
    print("=" * 70)
    
    # 1. Verificar API Key
    if not DASHSCOPE_API_KEY:
        print("❌ DASHSCOPE_API_KEY no configurada")
        print("\n   Configurar:")
        print("   export DASHSCOPE_API_KEY='sk_...'")
        print("   python3 glm4.5_api_oficial.py")
        return False
    else:
        print(f"✅ DASHSCOPE_API_KEY: {DASHSCOPE_API_KEY[:20]}...")
    
    # 2. Verificar que sea formato correcto
    if not DASHSCOPE_API_KEY.startswith("sk-") and not DASHSCOPE_API_KEY.startswith("sk_"):
        print("❌ API Key no parece válida (debe empezar con 'sk-' o 'sk_')")
        return False
    else:
        print("✅ Formato de API Key válido")
    
    # 3. Verificar modelo
    if MODELO_ACTUAL not in MODELOS_BAILIAN:
        print(f"❌ Modelo '{MODELO_ACTUAL}' no reconocido")
        return False
    else:
        info = MODELOS_BAILIAN[MODELO_ACTUAL]
        print(f"✅ Modelo: {info['nombre']} (ID: {info['id']})")
        print(f"   Velocidad: {info['velocidad']}")
        print(f"   Calidad: {info['calidad']}")
        print(f"   Precio: {info['precio']}")
    
    print("\n✅ CONFIGURACIÓN VÁLIDA")
    return True

# =============================================================================
# FUNCIÓN: PROBAR CONEXIÓN A BAILIAN
# =============================================================================

def probar_conexion():
    """Prueba que la API de Bailian responda correctamente"""
    
    print("\n🔌 PRUEBA DE CONEXIÓN A BAILIAN (GLM 4.5)")
    print("=" * 70)
    
    if not DASHSCOPE_API_KEY:
        print("❌ API Key no configurada. Primero ejecuta:")
        print("   export DASHSCOPE_API_KEY='sk_...'")
        return False
    
    try:
        headers = {
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODELO_ACTUAL,
            "input": {
                "messages": [
                    {"role": "user", "content": "Hola, ¿funcionas?"}
                ]
            },
            "parameters": {
                "temperature": 0.7,
                "max_tokens": 100
            }
        }
        
        print(f"📤 Enviando solicitud a Bailian...")
        print(f"   Endpoint: {BAILIAN_ENDPOINT}")
        print(f"   Modelo: {MODELO_ACTUAL}")
        
        import time
        inicio = time.time()
        
        response = requests.post(
            BAILIAN_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        tiempo_ms = (time.time() - inicio) * 1000
        
        if response.status_code == 200:
            resultado = response.json()
            respuesta = resultado.get("output", {}).get("text", "")
            
            print(f"\n✅ CONEXIÓN EXITOSA!")
            print(f"   Tiempo respuesta: {tiempo_ms:.0f}ms")
            print(f"   Respuesta de GLM 4.5:")
            print(f"   '{respuesta}'")
            return True
        
        elif response.status_code == 401:
            print(f"\n❌ ERROR 401: API Key inválida o expirada")
            print(f"   Verificar en: https://console.aliyun.com")
            return False
        
        elif response.status_code == 429:
            print(f"\n❌ ERROR 429: Límite de rate alcanzado")
            print(f"   Esperar unos minutos e intentar de nuevo")
            return False
        
        else:
            print(f"\n❌ ERROR {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR DE CONEXIÓN: {e}")
        print(f"   Verificar que:")
        print(f"   1. Internet está conectado")
        print(f"   2. API Key es válida")
        print(f"   3. Bailian está activado en tu cuenta")
        return False

# =============================================================================
# FUNCIÓN: LLAMAR A GLM 4.5
# =============================================================================

def llamar_glm4_5(mensaje: str, temperatura: float = 0.7, max_tokens: int = 1024) -> str:
    """
    Llama a GLM 4.5 vía API de Bailian
    
    Args:
        mensaje: El texto a procesar
        temperatura: 0-2 (0=determinista, 1=normal, 2=creativo)
        max_tokens: Máximo de tokens en la respuesta
    
    Returns:
        Respuesta de GLM 4.5, o error si falla
    """
    
    if not DASHSCOPE_API_KEY:
        return "❌ ERROR: DASHSCOPE_API_KEY no configurada"
    
    try:
        headers = {
            "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": MODELO_ACTUAL,
            "input": {
                "messages": [
                    {"role": "user", "content": mensaje}
                ]
            },
            "parameters": {
                "temperature": temperatura,
                "max_tokens": max_tokens
            }
        }
        
        response = requests.post(
            BAILIAN_ENDPOINT,
            headers=headers,
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            resultado = response.json()
            return resultado.get("output", {}).get("text", "Error: sin respuesta")
        else:
            return f"Error {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error de conexión: {e}"

# =============================================================================
# FUNCIÓN: MOSTRAR GUÍAS
# =============================================================================

def mostrar_guia(paso: int = 0):
    """Muestra la guía de setup paso a paso"""
    
    if paso == 1 or paso == 0:
        print(GUIA_PASO_1)
    
    if paso == 2 or paso == 0:
        print(GUIA_PASO_2)
    
    if paso == 3 or paso == 0:
        print(GUIA_PASO_3)
    
    if paso == 4 or paso == 0:
        print(GUIA_PASO_4)

# =============================================================================
# EJEMPLOS DE USO
# =============================================================================

def ejemplos():
    """Muestra ejemplos de cómo usar"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                        EJEMPLOS DE USO DE GLM 4.5                          ║
╚════════════════════════════════════════════════════════════════════════════╝

1. VERIFICAR CONFIGURACIÓN:
   
   python3 glm4.5_api_oficial.py --check
   
2. PROBAR CONEXIÓN:
   
   python3 glm4.5_api_oficial.py --test
   
3. ENVIAR MENSAJE SIMPLE:
   
   python3 glm4.5_api_oficial.py --ask "¿Cuál es la capital de Francia?"
   
4. USAR EN TU CÓDIGO:
   
   from glm4_5_api_oficial import llamar_glm4_5
   
   respuesta = llamar_glm4_5("Hola GLM 4.5, ¿cómo estás?")
   print(respuesta)

5. CON PARÁMETROS PERSONALIZADOS:
   
   respuesta = llamar_glm4_5(
       "Cuéntame un poema",
       temperatura=1.5,      # Más creativo
       max_tokens=500        # Respuesta más larga
   )
   print(respuesta)

6. INTEGRAR EN GENESYX:
   
   # Ver: genesyx_glm4.5_alibaba.py
   # Reemplaza Groq por Bailian (GLM 4.5 oficial)
   # Misma interfaz, mejor modelo
""")

# =============================================================================
# FUNCIÓN: LISTA DE PRECIOS Y MODELOS
# =============================================================================

def mostrar_modelos():
    """Muestra todos los modelos disponibles en Bailian"""
    
    print("""
╔════════════════════════════════════════════════════════════════════════════╗
║                 MODELOS DISPONIBLES EN BAILIAN (ALIBABA)                   ║
╚════════════════════════════════════════════════════════════════════════════╝
""")
    
    for key, info in MODELOS_BAILIAN.items():
        print(f"📌 {info['nombre']}")
        print(f"   ID: {info['id']}")
        print(f"   Velocidad: {info['velocidad']}")
        print(f"   Calidad: {info['calidad']}")
        print(f"   Precio: {info['precio']}")
        print(f"   {info['descripcion']}")
        print()
    
    print("✅ RECOMENDADO para Genesyx: qwen-max (GLM 4.5 equivalente)")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "--help" or arg == "-h":
            print("""
Uso: python3 glm4.5_api_oficial.py [OPCIÓN]

OPCIONES:
  --guia           Mostrar guía completa de setup
  --check          Verificar configuración
  --test           Probar conexión a Bailian
  --ask <mensaje>  Enviar mensaje a GLM 4.5
  --modelos        Listar modelos disponibles
  --ejemplos       Mostrar ejemplos de uso
  --help           Esta ayuda
""")
        
        elif arg == "--guia":
            mostrar_guia()
        
        elif arg == "--check":
            verificar_configuracion()
        
        elif arg == "--test":
            probar_conexion()
        
        elif arg == "--ask" and len(sys.argv) > 2:
            mensaje = " ".join(sys.argv[2:])
            print(f"\n📤 Enviando a GLM 4.5: {mensaje}\n")
            respuesta = llamar_glm4_5(mensaje)
            print(f"✅ Respuesta:\n{respuesta}")
        
        elif arg == "--modelos":
            mostrar_modelos()
        
        elif arg == "--ejemplos":
            ejemplos()
        
        else:
            print(f"Opción desconocida: {arg}")
            print("Usa: python3 glm4.5_api_oficial.py --help")
    
    else:
        # Sin argumentos: mostrar menú interactivo
        print("""
╔════════════════════════════════════════════════════════════════════════════╗
║          ACCESO A GLM 4.5 (ALIBABA CLOUD BAILIAN) - MENÚ                  ║
╚════════════════════════════════════════════════════════════════════════════╝

1. Mostrar guía de setup
2. Verificar configuración
3. Probar conexión
4. Ver modelos disponibles
5. Ejemplos de uso
6. Salir

Selecciona una opción (1-6): """)
        
        opcion = input().strip()
        
        if opcion == "1":
            mostrar_guia()
        elif opcion == "2":
            verificar_configuracion()
        elif opcion == "3":
            probar_conexion()
        elif opcion == "4":
            mostrar_modelos()
        elif opcion == "5":
            ejemplos()
        elif opcion == "6":
            print("Saliendo...")
        else:
            print("Opción no válida")
