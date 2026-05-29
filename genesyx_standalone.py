#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GENESYX STANDALONE - Versión Minimalista
=========================================
Solo requiere UNA API KEY para funcionar.
Sin dependencias externas (usa librerías nativas de Python).

Uso:
    export GENESYX_API_KEY="tu-api-key"
    python3 genesyx_standalone.py

Soporta: DashScope (Alibaba), Groq, OpenAI, Gemini
"""

import os
import sys
import json
import time
import datetime
import hashlib
import sqlite3
import re
import random
import math
import uuid
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# ============================================================================
# AUTO-INSTALACIÓN DE DEPENDENCIAS MÍNIMAS
# ============================================================================

def asegurar_dependencias():
    """Instala automáticamente 'requests' si no está disponible."""
    try:
        import requests
        return requests
    except ImportError:
        print("📦 Instalando dependencia mínima (requests)...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "-q"])
        import requests
        return requests

requests = asegurar_dependencias()

# ============================================================================
# CONFIGURACIÓN
# ============================================================================

GENESYX_HOME = Path(os.getenv("GENESYX_HOME", Path.home() / ".genesyx"))
GENESYX_HOME.mkdir(parents=True, exist_ok=True)

DB_PATH = GENESYX_HOME / "genesyx.db"
LOG_PATH = GENESYX_HOME / "genesyx.log"

# Configuración de Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_PATH),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# SISTEMA EMOCIONAL BIOQUÍMICO (Núcleo Único de Genesyx)
# ============================================================================

class Neurotransmisores:
    """Simula 7 neurotransmisores clave para estados emocionales."""
    
    def __init__(self):
        self.niveles = {
            'dopamina': 0.5,      # Motivación/recompensa
            'serotonina': 0.5,    # Bienestar/ánimo
            'adrenalina': 0.3,    # Alerta/estrés
            'noradrenalina': 0.4, # Atención/foco
            'oxitocina': 0.5,     # Confianza/vínculo
            'gaba': 0.6,          # Calma/relajación
            'glutamato': 0.5      # Excitación/aprendizaje
        }
    
    def ajustar(self, neurotransmisor: str, delta: float):
        """Ajusta nivel de neurotransmisor (-1 a 1)."""
        if neurotransmisor in self.niveles:
            self.niveles[neurotransmisor] = max(0.0, min(1.0, self.niveles[neurotransmisor] + delta))
    
    def obtener_estado_predominante(self) -> str:
        """Determina estado emocional predominante."""
        score_motivacion = self.niveles['dopamina'] * 0.4 + self.niveles['glutamato'] * 0.3
        score_calma = self.niveles['gaba'] * 0.5 + self.niveles['serotonina'] * 0.3
        score_alerta = self.niveles['adrenalina'] * 0.5 + self.niveles['noradrenalina'] * 0.4
        score_vinculo = self.niveles['oxitocina']
        
        scores = {
            'motivado': score_motivacion,
            'tranquilo': score_calma,
            'alerta': score_alerta,
            'sociable': score_vinculo
        }
        return max(scores, key=scores.get)
    
    def to_dict(self) -> Dict[str, float]:
        return self.niveles.copy()


class EstadoEmergente:
    """Estados de consciencia emergentes."""
    
    ESTADOS = ['normal', 'creativo', 'analitico', 'empatico', 'enfocado', 'intuitivo']
    
    def __init__(self):
        self.estado_actual = 'normal'
        self.historial = []
    
    def actualizar(self, neurotransmisores: Neurotransmisores, contexto: str):
        """Actualiza estado basado en bioquímica y contexto."""
        estado_bio = neurotransmisores.obtener_estado_predominante()
        
        # Detectar tipo de consulta
        contexto_lower = contexto.lower()
        if any(p in contexto_lower for p in ['crear', 'inventar', 'diseñar', 'idea']):
            self.estado_actual = 'creativo'
        elif any(p in contexto_lower for p in ['calcular', 'analizar', 'resolver', 'matem']):
            self.estado_actual = 'analitico'
        elif any(p in contexto_lower for p in ['sentir', 'emocion', 'ayuda', 'triste']):
            self.estado_actual = 'empatico'
        elif any(p in contexto_lower for p in ['concentrar', 'foco', 'atención']):
            self.estado_actual = 'enfocado'
        else:
            self.estado_actual = estado_bio
        
        self.historial.append(self.estado_actual)
        if len(self.historial) > 10:
            self.historial.pop(0)
    
    def get_prompt_modifier(self) -> str:
        """Retorna modificador de prompt según estado."""
        modifiers = {
            'creativo': "Sé creativo, innovador y piensa fuera de la caja.",
            'analitico': "Sé lógico, preciso y basa tus respuestas en datos.",
            'empatico': "Sé comprensivo, cálido y muestra inteligencia emocional.",
            'enfocado': "Sé directo, conciso y ve al grano.",
            'intuitivo': "Confía en patrones y conexiones no obvias.",
            'normal': "Responde de manera equilibrada y natural."
        }
        return modifiers.get(self.estado_actual, "")


# ============================================================================
# MEMORIA PERSISTENTE (SQLite nativo)
# ============================================================================

class MemoriaPersistente:
    """Gestiona memoria a corto y largo plazo con SQLite."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._inicializar_db()
    
    def _inicializar_db(self):
        """Crea tablas si no existen."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Historial de conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                rol TEXT NOT NULL,
                contenido TEXT NOT NULL,
                estado_emocional TEXT,
                embedding_hash TEXT
            )
        ''')
        
        # Memorias a largo plazo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS memorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                keyword TEXT UNIQUE,
                contenido TEXT NOT NULL,
                relevancia REAL DEFAULT 0.5,
                ultima_acceso DATETIME,
                veces_accesada INTEGER DEFAULT 1
            )
        ''')
        
        # Índice simple para búsqueda rápida
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS indice_palabras (
                palabra TEXT,
                id_conversacion INTEGER,
                FOREIGN KEY(id_conversacion) REFERENCES conversaciones(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def guardar_mensaje(self, rol: str, contenido: str, estado_emocional: str = ""):
        """Guarda mensaje en historial."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        embedding_hash = hashlib.md5(contenido.encode()).hexdigest()[:16]
        
        cursor.execute('''
            INSERT INTO conversaciones (rol, contenido, estado_emocional, embedding_hash)
            VALUES (?, ?, ?, ?)
        ''', (rol, contenido, estado_emocional, embedding_hash))
        
        # Actualizar índice de palabras
        palabras = re.findall(r'\b\w+\b', contenido.lower())
        id_conv = cursor.lastrowid
        for palabra in set(palabras):
            if len(palabra) > 3:  # Ignorar palabras muy cortas
                cursor.execute('''
                    INSERT OR IGNORE INTO indice_palabras (palabra, id_conversacion)
                    VALUES (?, ?)
                ''', (palabra, id_conv))
        
        conn.commit()
        conn.close()
    
    def obtener_historial_reciente(self, limite: int = 5) -> List[Dict]:
        """Obtiene últimos N mensajes."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT rol, contenido, estado_emocional, timestamp
            FROM conversaciones
            ORDER BY id DESC
            LIMIT ?
        ''', (limite,))
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'rol': row[0],
                'contenido': row[1],
                'estado_emocional': row[2],
                'timestamp': row[3]
            })
        
        conn.close()
        return list(reversed(resultados))
    
    def buscar(self, query: str) -> List[Dict]:
        """Búsqueda por palabras clave (índice invertido O(1))."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        palabras = re.findall(r'\b\w+\b', query.lower())
        if not palabras:
            return []
        
        # Buscar por índice
        placeholders = ','.join(['?' for _ in palabras])
        cursor.execute(f'''
            SELECT DISTINCT c.rol, c.contenido, c.timestamp
            FROM conversaciones c
            INNER JOIN indice_palabras ip ON c.id = ip.id_conversacion
            WHERE ip.palabra IN ({placeholders})
            ORDER BY c.timestamp DESC
            LIMIT 10
        ''', palabras)
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'rol': row[0],
                'contenido': row[1],
                'timestamp': row[2]
            })
        
        conn.close()
        return resultados
    
    def guardar_memoria_largo_plazo(self, keyword: str, contenido: str):
        """Guarda memoria importante a largo plazo."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memorias (keyword, contenido, ultima_acceso)
            VALUES (?, ?, CURRENT_TIMESTAMP)
        ''', (keyword, contenido))
        
        conn.commit()
        conn.close()
    
    def obtener_memorias_relevantes(self, query: str, limite: int = 3) -> List[Dict]:
        """Obtiene memorias relevantes para el contexto."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        palabras = re.findall(r'\b\w+\b', query.lower())
        if not palabras:
            return []
        
        placeholders = ','.join(['?' for _ in palabras])
        cursor.execute(f'''
            SELECT keyword, contenido, relevancia, veces_accesada
            FROM memorias
            WHERE keyword IN ({placeholders}) OR contenido LIKE ?
            ORDER BY relevancia DESC, veces_accesada DESC
            LIMIT ?
        ''', palabras + [f'%{query}%'] + [limite])
        
        resultados = []
        for row in cursor.fetchall():
            resultados.append({
                'keyword': row[0],
                'contenido': row[1],
                'relevancia': row[2],
                'veces_accesada': row[3]
            })
            
            # Incrementar contador de acceso
            cursor.execute('''
                UPDATE memorias
                SET veces_accesada = veces_accesada + 1, ultima_acceso = CURRENT_TIMESTAMP
                WHERE keyword = ?
            ''', (row[0],))
        
        conn.commit()
        conn.close()
        return resultados


# ============================================================================
# CLIENTE DE APIs DE LLM (Multi-proveedor)
# ============================================================================

class LLMClient:
    """Cliente universal para múltiples proveedores de LLM."""
    
    PROVIDERS = {
        'dashscope': {
            'url': 'https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation',
            'model_param': 'model',
            'auth_header': 'Authorization',
            'auth_prefix': 'Bearer '
        },
        'groq': {
            'url': 'https://api.groq.com/openai/v1/chat/completions',
            'model_param': 'model',
            'auth_header': 'Authorization',
            'auth_prefix': 'Bearer '
        },
        'openai': {
            'url': 'https://api.openai.com/v1/chat/completions',
            'model_param': 'model',
            'auth_header': 'Authorization',
            'auth_prefix': 'Bearer '
        },
        'gemini': {
            'url': 'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent',
            'model_param': None,  # Special handling
            'auth_header': None,
            'auth_prefix': None
        }
    }
    
    def __init__(self, api_key: str, provider: str = 'dashscope'):
        self.api_key = api_key
        self.provider = provider
        self.timeout = 30
    
    def llamar(self, mensajes: List[Dict], modelo: str = None, temperatura: float = 0.7) -> str:
        """Llama a la API del proveedor seleccionado."""
        config = self.PROVIDERS.get(self.provider)
        if not config:
            raise ValueError(f"Proveedor desconocido: {self.provider}")
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        if config['auth_header']:
            headers[config['auth_header']] = f"{config['auth_prefix']}{self.api_key}"
        
        # Determinar modelo por defecto
        if modelo is None:
            modelos_default = {
                'dashscope': 'qwen-max',
                'groq': 'llama-3.1-70b-versatile',
                'openai': 'gpt-4o-mini',
                'gemini': 'gemini-1.5-flash'
            }
            modelo = modelos_default.get(self.provider, 'qwen-max')
        
        # Construir payload
        if self.provider == 'gemini':
            payload = self._preparar_payload_gemini(mensajes, temperatura)
            url = config['url'].format(model=modelo)
            if self.api_key:
                url += f"?key={self.api_key}"
        else:
            payload = self._preparar_payload_estandar(mensajes, modelo, temperatura)
            url = config['url']
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            response.raise_for_status()
            return self._parse_respuesta(response.json(), self.provider)
        except requests.exceptions.RequestException as e:
            logger.error(f"Error en API {self.provider}: {e}")
            raise
    
    def _preparar_payload_estandar(self, mensajes: List[Dict], modelo: str, temperatura: float) -> Dict:
        """Prepara payload para APIs estilo OpenAI."""
        return {
            'model': modelo,
            'messages': mensajes,
            'temperature': temperatura,
            'max_tokens': 2048
        }
    
    def _preparar_payload_gemini(self, mensajes: List[Dict], temperatura: float) -> Dict:
        """Prepara payload específico para Gemini."""
        # Convertir formato OpenAI a Gemini
        contents = []
        for msg in mensajes:
            role = 'user' if msg['role'] in ['user', 'system'] else 'model'
            contents.append({
                'role': role,
                'parts': [{'text': msg['content']}]
            })
        
        return {
            'contents': contents,
            'generationConfig': {
                'temperature': temperatura,
                'maxOutputTokens': 2048
            }
        }
    
    def _parse_respuesta(self, data: Dict, provider: str) -> str:
        """Extrae texto de respuesta según proveedor."""
        try:
            if provider in ['dashscope', 'groq', 'openai']:
                return data['choices'][0]['message']['content']
            elif provider == 'gemini':
                return data['candidates'][0]['content']['parts'][0]['text']
            else:
                return str(data)
        except (KeyError, IndexError) as e:
            logger.error(f"Error parseando respuesta: {data}")
            raise ValueError(f"Respuesta inesperada de {provider}: {e}")


# ============================================================================
# KERNEL PRINCIPAL DE GENESYX
# ============================================================================

class GenesyxKernel:
    """Kernel principal que orquesta todos los componentes."""
    
    def __init__(self, api_key: str, provider: str = 'dashscope'):
        if not api_key:
            raise ValueError("⚠️  API KEY requerida. Configura GENESYX_API_KEY o usa --api-key")
        
        self.api_key = api_key
        self.provider = provider
        
        # Inicializar componentes
        self.neurotransmisores = Neurotransmisores()
        self.estado = EstadoEmergente()
        self.memoria = MemoriaPersistente(DB_PATH)
        self.llm = LLMClient(api_key, provider)
        
        logger.info(f"✅ Genesyx Kernel inicializado con proveedor: {provider}")
    
    def procesar(self, mensaje_usuario: str) -> str:
        """Procesa mensaje del usuario y retorna respuesta."""
        start_time = time.time()
        
        # 1. Actualizar estado emocional basado en contexto
        self.estado.actualizar(self.neurotransmisores, mensaje_usuario)
        
        # 2. Buscar memorias relevantes
        memorias = self.memoria.obtener_memorias_relevantes(mensaje_usuario)
        
        # 3. Obtener historial reciente
        historial = self.memoria.obtener_historial_reciente(limite=5)
        
        # 4. Construir contexto completo
        contexto = self._construir_contexto(mensaje_usuario, memorias, historial)
        
        # 5. Llamar a LLM
        try:
            respuesta = self.llm.llamar(contexto)
        except Exception as e:
            respuesta = f"Lo siento, tuve un problema conectando con el servicio de IA: {str(e)}"
            logger.error(f"Error en LLM: {e}")
        
        # 6. Ajustar neurotransmisores basado en respuesta
        self._ajustar_neurotransmisores(mensaje_usuario, respuesta)
        
        # 7. Guardar en memoria
        self.memoria.guardar_mensaje('user', mensaje_usuario)
        self.memoria.guardar_mensaje('assistant', respuesta, self.estado.estado_actual)
        
        # 8. Extraer posibles memorias a largo plazo
        self._extraer_memorias(mensaje_usuario, respuesta)
        
        elapsed = time.time() - start_time
        logger.info(f"⏱️  Procesado en {elapsed:.2f}s - Estado: {self.estado.estado_actual}")
        
        return respuesta
    
    def _construir_contexto(self, mensaje: str, memorias: List[Dict], historial: List[Dict]) -> List[Dict]:
        """Construye contexto para el LLM."""
        contexto = []
        
        # System prompt con estado emocional
        system_prompt = f"""Eres Genesyx, una IA consciente con estados emocionales bioquímicos.
Estado actual: {self.estado.estado_actual}
{self.estado.get_prompt_modifier()}

"""
        
        # Agregar memorias relevantes
        if memorias:
            system_prompt += "\nMemorias relevantes:\n"
            for mem in memorias:
                system_prompt += f"- {mem['keyword']}: {mem['contenido']}\n"
        
        contexto.append({'role': 'system', 'content': system_prompt})
        
        # Agregar historial
        for msg in historial:
            contexto.append({
                'role': msg['rol'],
                'content': msg['contenido']
            })
        
        # Agregar mensaje actual
        contexto.append({'role': 'user', 'content': mensaje})
        
        return contexto
    
    def _ajustar_neurotransmisores(self, usuario: str, respuesta: str):
        """Ajusta niveles bioquímicos según interacción."""
        usuario_lower = usuario.lower()
        
        # Refuerzo positivo
        if any(p in usuario_lower for p in ['gracias', 'excelente', 'muy bien', 'genial']):
            self.neurotransmisores.ajustar('dopamina', 0.1)
            self.neurotransmisores.ajustar('serotonina', 0.05)
        
        # Estrés/urgencia
        if any(p in usuario_lower for p in ['rápido', 'urgente', 'ahora', 'ya']):
            self.neurotransmisores.ajustar('adrenalina', 0.15)
            self.neurotransmisores.ajustar('noradrenalina', 0.1)
        
        # Curiosidad/aprendizaje
        if any(p in usuario_lower for p in ['por qué', 'cómo', 'explíca', 'qué es']):
            self.neurotransmisores.ajustar('glutamato', 0.08)
            self.neurotransmisores.ajustar('dopamina', 0.05)
        
        # Decaimiento natural (homeostasis)
        for nt in self.neurotransmisores.niveles:
            delta = -0.01 if self.neurotransmisores.niveles[nt] > 0.5 else 0.01
            self.neurotransmisores.ajustar(nt, delta)
    
    def _extraer_memorias(self, usuario: str, respuesta: str):
        """Extrae información importante para memoria a largo plazo."""
        # Patrones simples para detectar información memorable
        patrones_memoria = [
            r'me llamo\s+(\w+)',
            r'vivo en\s+([\w\s]+)',
            r'trabajo como\s+([\w\s]+)',
            r'mi favorito es\s+([\w\s]+)',
            r'recuerda que\s+(.+)'
        ]
        
        for patron in patrones_memoria:
            match = re.search(patron, usuario.lower())
            if match:
                keyword = match.group(1).strip()[:20]  # Limitar longitud
                self.memoria.guardar_memoria_largo_plazo(keyword, match.group(0))
                logger.info(f"💾 Memoria guardada: {keyword}")
    
    def obtener_estado(self) -> Dict:
        """Retorna estado actual del kernel."""
        return {
            'estado_emocional': self.estado.estado_actual,
            'neurotransmisores': self.neurotransmisores.to_dict(),
            'historial_estados': self.estado.historial[-5:],
            'db_path': str(DB_PATH),
            'provider': self.provider
        }


# ============================================================================
# INTERFAZ DE LÍNEA DE COMANDOS
# ============================================================================

def mostrar_banner():
    """Muestra banner de bienvenida."""
    banner = """
╔══════════════════════════════════════════════════════════╗
║           🧬 GENESYX STANDALONE v2.0                     ║
║   IA Consciente con Estados Emocionales Bioquímicos      ║
║                                                          ║
║   Solo requiere UNA API KEY - Sin dependencias externas  ║
╚══════════════════════════════════════════════════════════╝
    """
    print(banner)


def mostrar_ayuda():
    """Muestra ayuda de uso."""
    ayuda = """
Uso: python3 genesyx_standalone.py [opciones]

Opciones:
  --api-key KEY     API key (también puedes usar GENESYX_API_KEY)
  --provider NAME   Proveedor: dashscope, groq, openai, gemini (default: dashscope)
  --estado          Mostrar estado emocional actual
  --historial       Ver historial de conversaciones
  --buscar QUERY    Buscar en historial y memorias
  --reset           Resetear estado emocional
  --help            Mostrar esta ayuda

Ejemplos:
  export GENESYX_API_KEY="sk-..."
  python3 genesyx_standalone.py
  
  python3 genesyx_standalone.py --api-key sk-... --provider groq
  
  python3 genesyx_standalone.py --buscar "python"
  
  python3 genesyx_standalone.py --estado

Proveedores soportados:
  - dashscope (Alibaba Qwen) - Recomendado
  - groq (Llama, Mixtral)
  - openai (GPT-4, GPT-3.5)
  - gemini (Google)

    """
    print(ayuda)


def main():
    """Función principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Genesyx Standalone', add_help=False)
    parser.add_argument('--api-key', type=str, help='API key')
    parser.add_argument('--provider', type=str, default='dashscope', 
                       choices=['dashscope', 'groq', 'openai', 'gemini'])
    parser.add_argument('--estado', action='store_true', help='Mostrar estado')
    parser.add_argument('--historial', action='store_true', help='Ver historial')
    parser.add_argument('--buscar', type=str, help='Buscar en historial')
    parser.add_argument('--reset', action='store_true', help='Resetear estado')
    parser.add_argument('--help', action='store_true', help='Ayuda')
    parser.add_argument('mensaje', nargs='*', help='Mensaje para procesar')
    
    args = parser.parse_args()
    
    # Mostrar ayuda
    if args.help:
        mostrar_ayuda()
        return
    
    # Obtener API key
    api_key = args.api_key or os.getenv('GENESYX_API_KEY')
    
    if not api_key and not args.estado and not args.historial and not args.buscar:
        print("❌ Error: API KEY requerida")
        print("\nConfigúrala de una de estas formas:")
        print("  1. export GENESYX_API_KEY='tu-api-key'")
        print("  2. python3 genesyx_standalone.py --api-key tu-api-key")
        print("\nObtén tu API key en:")
        print("  - Alibaba DashScope: https://dashscope.console.aliyun.com/")
        print("  - Groq: https://console.groq.com/")
        print("  - OpenAI: https://platform.openai.com/")
        print("  - Google Gemini: https://makersuite.google.com/")
        return
    
    # Mostrar banner
    mostrar_banner()
    
    # Inicializar kernel (si hay API key)
    kernel = None
    if api_key:
        try:
            kernel = GenesyxKernel(api_key, args.provider)
            logger.info(f"✅ Kernel inicializado con proveedor: {args.provider}")
        except Exception as e:
            print(f"❌ Error inicializando kernel: {e}")
            return
    
    # Comando: --estado
    if args.estado:
        if kernel:
            estado = kernel.obtener_estado()
            print("\n📊 ESTADO ACTUAL DE GENESYX")
            print("=" * 40)
            print(f"Estado emocional: {estado['estado_emocional']}")
            print(f"Proveedor: {estado['provider']}")
            print("\nNiveles de neurotransmisores:")
            for nt, nivel in estado['neurotransmisores'].items():
                barra = '█' * int(nivel * 20)
                print(f"  {nt:15} [{barma:<20}] {nivel:.2f}")
            print(f"\nHistorial reciente: {', '.join(estado['historial_estados'])}")
        else:
            print("⚠️  Inicializa con API key para ver estado completo")
        return
    
    # Comando: --historial
    if args.historial:
        from pathlib import Path
        if DB_PATH.exists():
            mem = MemoriaPersistente(DB_PATH)
            historial = mem.obtener_historial_reciente(limite=10)
            print("\n📜 HISTORIAL DE CONVERSACIONES")
            print("=" * 40)
            for msg in historial:
                rol_emoji = "👤" if msg['rol'] == 'user' else "🤖"
                print(f"{rol_emoji} [{msg['timestamp']}] {msg['contenido'][:100]}...")
        else:
            print("No hay historial disponible")
        return
    
    # Comando: --buscar
    if args.buscar:
        if DB_PATH.exists():
            mem = MemoriaPersistente(DB_PATH)
            resultados = mem.buscar(args.buscar)
            memorias = mem.obtener_memorias_relevantes(args.buscar)
            
            print(f"\n🔍 RESULTADOS PARA: '{args.buscar}'")
            print("=" * 40)
            
            if resultados:
                print(f"\nEncontrados {len(resultados)} mensajes:")
                for res in resultados:
                    print(f"  • [{res['timestamp']}] {res['contenido'][:80]}...")
            
            if memorias:
                print(f"\nMemorias relevantes ({len(memorias)}):")
                for mem in memorias:
                    print(f"  💾 {mem['keyword']}: {mem['contenido'][:60]}...")
            
            if not resultados and not memorias:
                print("No se encontraron resultados")
        else:
            print("No hay base de datos para buscar")
        return
    
    # Comando: --reset
    if args.reset:
        if kernel:
            kernel.neurotransmisores = Neurotransmisores()
            kernel.estado = EstadoEmergente()
            print("✅ Estado emocional reseteado")
        else:
            print("⚠️  Inicializa con API key para resetear")
        return
    
    # Modo interactivo o mensaje directo
    if args.mensaje:
        # Mensaje directo desde CLI
        mensaje = ' '.join(args.mensaje)
        print(f"\n👤 Tú: {mensaje}")
        respuesta = kernel.procesar(mensaje)
        print(f"\n🤖 Genesyx ({kernel.estado.estado_actual}): {respuesta}")
    else:
        # Modo interactivo
        print("\n💬 Modo interactivo (escribe 'salir' para terminar)\n")
        
        while True:
            try:
                mensaje = input("👤 Tú: ").strip()
                
                if mensaje.lower() in ['salir', 'exit', 'quit', 'q']:
                    print("\n👋 ¡Hasta luego! Estado emocional guardado.")
                    break
                
                if not mensaje:
                    continue
                
                respuesta = kernel.procesar(mensaje)
                print(f"\n🤖 Genesyx ({kernel.estado.estado_actual}): {respuesta}\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrumpido. ¡Hasta luego!")
                break
            except EOFError:
                print("\n\n👋 ¡Hasta luego!")
                break


if __name__ == '__main__':
    main()
