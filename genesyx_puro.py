#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🧬 GENESYX STANDALONE - VERSIÓN 100% NATIVA
============================================

✅ REQUISITOS ÚNICOS:
   - Python 3.6+
   - UNA sola API Key (DashScope/Alibaba)
   - Conexión a internet

❌ SIN DEPENDENCIAS EXTERNAS:
   - No requiere pip install
   - No requiere requests
   - Usa SOLO librerías nativas de Python

💡 USO:
   export GENESYX_API_KEY="sk-xxxxx"
   python3 genesyx_puro.py
   
   O simplemente:
   python3 genesyx_puro.py
   (Te pedirá la API Key la primera vez)
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from pathlib import Path

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

ARCHIVO_KEY = Path.home() / ".genesyx_key"
URL_API = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
MODELO = "qwen-max"

# ============================================================================
# NÚCLEO EMOCIONAL BIOQUÍMICO
# ============================================================================

class Neuroquimica:
    """Simula neurotransmisores que afectan las respuestas."""
    
    def __init__(self):
        self.niveles = {
            "serotonina": 50.0,  # Estado de ánimo
            "dopamina": 50.0,    # Motivación
            "oxitocina": 50.0,   # Confianza
            "cortisol": 10.0,    # Estrés
            "adrenalina": 10.0   # Alerta
        }
    
    def estimular(self, emocion):
        """Ajusta químicos según emoción detectada."""
        ajustes = {
            "alegria": {"serotonina": 5, "dopamina": 5, "cortisol": -2},
            "tristeza": {"serotonina": -3, "dopamina": -2, "oxitocina": 2},
            "miedo": {"cortisol": 10, "adrenalina": 15, "serotonina": -5},
            "confianza": {"oxitocina": 8, "cortisol": -5},
            "curiosidad": {"dopamina": 6, "adrenalina": 3}
        }
        
        if emocion in ajustes:
            for q, val in ajustes[emocion].items():
                self.niveles[q] = max(0, min(100, self.niveles[q] + val))
        
        # Homeostasis: retorno al equilibrio
        for q in self.niveles:
            if self.niveles[q] > 50:
                self.niveles[q] -= 0.5
            elif self.niveles[q] < 50:
                self.niveles[q] += 0.5
    
    def obtener_estado(self):
        """Determina estado emocional dominante."""
        if self.niveles["cortisol"] > 70 or self.niveles["adrenalina"] > 70:
            return "Alerta/Estrés"
        elif self.niveles["serotonina"] > 70 and self.niveles["dopamina"] > 70:
            return "Eufórico/Creativo"
        elif self.niveles["oxitocina"] > 70:
            return "Empático/Amigable"
        elif self.niveles["dopamina"] < 30:
            return "Apático"
        return "Neutral"
    
    def mostrar(self):
        """Visualiza niveles bioquímicos."""
        print("\n📊 BIOQUÍMICA ACTUAL:")
        print("-" * 40)
        for nombre, valor in self.niveles.items():
            barra = "█" * int(valor / 5)
            print(f"  {nombre.capitalize():12} [{barra:<20}] {valor:.1f}%")
        print(f"\n  🎭 Estado: {self.obtener_estado()}")
        print("-" * 40)

# ============================================================================
# MEMORIA DE CONVERSACIÓN
# ============================================================================

class Memoria:
    """Guarda últimos mensajes para contexto."""
    
    def __init__(self, capacidad=5):
        self.capacidad = capacidad
        self.historial = []
    
    def agregar(self, rol, contenido):
        self.historial.append({"role": rol, "content": contenido})
        if len(self.historial) > self.capacidad:
            self.historial.pop(0)
    
    def obtener(self):
        return self.historial

# ============================================================================
# CLIENTE HTTP NATIVO (Sin requests!)
# ============================================================================

def llamar_api(api_key, mensaje, contexto, estado):
    """
    Llama a la API de DashScope usando SOLO urllib (nativo).
    Sin dependencias externas.
    """
    
    system_prompt = (
        f"Eres Genesyx, una IA con estados emocionales simulados. "
        f"Estado actual: {estado}. "
        f"Sé natural, conciso y coherente con tu estado emocional."
    )
    
    messages = [{"role": "system", "content": system_prompt}]
    messages.extend(contexto)
    messages.append({"role": "user", "content": mensaje})
    
    payload = {
        "model": MODELO,
        "input": {"messages": messages},
        "parameters": {"temperature": 0.7, "max_tokens": 1000}
    }
    
    data_json = json.dumps(payload).encode('utf-8')
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        req = urllib.request.Request(URL_API, data=data_json, headers=headers)
        
        with urllib.request.urlopen(req, timeout=30) as response:
            resultado = response.read().decode('utf-8')
            datos = json.loads(resultado)
            
            # Extraer respuesta
            if "output" in datos and "choices" in datos["output"]:
                return datos["output"]["choices"][0]["message"]["content"]
            elif "output" in datos and "text" in datos["output"]:
                return datos["output"]["text"]
            else:
                return "[Error: Formato inesperado]"
                
    except urllib.error.HTTPError as e:
        return f"[Error HTTP {e.code}: {e.reason}]"
    except urllib.error.URLError as e:
        return f"[Error conexión: {e.reason}]"
    except Exception as e:
        return f"[Error: {str(e)}]"

# ============================================================================
# GESTIÓN DE API KEY
# ============================================================================

def obtener_api_key():
    """Obtiene API Key de entorno, archivo o pide al usuario."""
    
    # 1. Variable de entorno
    key = os.getenv("GENESYX_API_KEY")
    if key:
        return key
    
    # 2. Archivo local
    if ARCHIVO_KEY.exists():
        key = ARCHIVO_KEY.read_text().strip()
        if key:
            return key
    
    # 3. Pedir al usuario
    print("\n" + "="*50)
    print("🧬 GENESYX STANDALONE v1.0 (100% Nativo)")
    print("="*50)
    print("\n⚠️  Necesito una API Key para funcionar.")
    print("Usaré el modelo Qwen-Max de Alibaba (DashScope).")
    print("\n📝 Obtén tu API Key gratis en:")
    print("   https://dashscope.console.aliyun.com/")
    print("\n" + "-"*50)
    
    while True:
        key = input("🔑 Introduce tu API Key: ").strip()
        if len(key) > 10:
            ARCHIVO_KEY.write_text(key)
            print(f"✅ Guardada en {ARCHIVO_KEY}")
            return key
        print("❌ Key muy corta. Intenta de nuevo.")

# ============================================================================
# DETECCIÓN DE EMOCIONES
# ============================================================================

def detectar_emocion(texto):
    """Detecta emoción simple en texto del usuario."""
    t = texto.lower()
    
    if any(x in t for x in ["feliz", "bien", "genial", "amor", "gracias", "excelente"]):
        return "alegria"
    elif any(x in t for x in ["triste", "mal", "dolor", "llorar", "deprimido"]):
        return "tristeza"
    elif any(x in t for x in ["miedo", "peligro", "ayuda", "terror", "pánico"]):
        return "miedo"
    elif any(x in t for x in ["confío", "creo", "seguro", "amigo"]):
        return "confianza"
    elif any(x in t for x in ["qué", "cómo", "por qué", "explíca", "curioso"]):
        return "curiosidad"
    
    return "neutral"

# ============================================================================
# BUCLE PRINCIPAL
# ============================================================================

def main():
    """Bucle principal de conversación."""
    
    api_key = obtener_api_key()
    neuro = Neuroquimica()
    memoria = Memoria()
    
    print("\n🟢 Genesyx iniciado")
    print(f"🧠 Estado: {neuro.obtener_estado()}")
    print("💬 Comandos: 'estado', 'reset', 'salir'")
    print("-"*50)
    
    while True:
        try:
            entrada = input("\n👤 Tú: ").strip()
            
            if not entrada:
                continue
            
            # Comandos especiales
            if entrada.lower() in ["salir", "exit", "quit"]:
                print("\n👋 Genesyx: ¡Hasta luego!")
                break
            
            if entrada.lower() == "estado":
                neuro.mostrar()
                continue
            
            if entrada.lower() == "reset":
                neuro = Neuroquimica()
                print("🔄 Estado emocional reseteado")
                continue
            
            # Detectar emoción y actualizar bioquímica
            emocion = detectar_emocion(entrada)
            neuro.estimular(emocion)
            estado = neuro.obtener_estado()
            
            # Generar respuesta
            print("🧬 Genesyx: ", end="", flush=True)
            inicio = time.time()
            
            respuesta = llamar_api(api_key, entrada, memoria.obtener(), estado)
            
            tiempo = time.time() - inicio
            print(respuesta)
            print(f"   ⏱️ {tiempo:.2f}s | {estado}")
            
            # Guardar en memoria
            memoria.agregar("user", entrada)
            memoria.agregar("assistant", respuesta)
            
        except KeyboardInterrupt:
            print("\n\n🛑 Interrumpido. Cerrando...")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")
            break

if __name__ == "__main__":
    main()
