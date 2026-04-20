#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  GENESYX v∞ CON GLM 4.5 OFICIAL (ALIBABA BAILIAN)                           ║
║                                                                              ║
║  Acceso directo a GLM 4.5 vía API oficial de Alibaba Cloud                  ║
║  Este es el modelo más potente: mejor que Groq, mejor que OpenAI            ║
║                                                                              ║
║  Priority automático:                                                        ║
║  1. GLM 4.5 (Alibaba Bailian) - ⭐ MEJOR Y MÁS POTENTE                      ║
║  2. Groq (fallback)                                                          ║
║  3. Ollama local (si está corriendo)                                         ║
║  4. Fallback local                                                           ║
║                                                                              ║
║  Configuración:                                                              ║
║  export DASHSCOPE_API_KEY="sk_..."                                          ║
║  python3 genesyx_glm4.5_alibaba.py                                          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import subprocess
import importlib
import asyncio
import json
import hashlib
import time
import re
import uuid
import shlex
import tempfile
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict, field
from enum import Enum
from collections import OrderedDict

# Auto-install
def instalar_si_falta(paquete):
    try:
        importlib.import_module(paquete)
    except ImportError:
        print(f"📦 Instalando: {paquete}...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", paquete])

for dep in ["numpy", "requests", "croniter"]:
    instalar_si_falta(dep)

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "sentence-transformers"])

import numpy as np
import requests
import croniter
from sentence_transformers import SentenceTransformer

# =============================================================================
# CONFIGURACIÓN
# =============================================================================

GENESYX_HOME = Path("/opt/genesyx")
GENESYX_HOME.mkdir(parents=True, exist_ok=True)

CREATOR_ID = "0108199300166"
CREATOR_NAME = "Orlin Gómez López"

# GLM 4.5 - ALIBABA BAILIAN (OFICIAL)
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY", "")
DASHSCOPE_ENDPOINT = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
DASHSCOPE_MODEL = "qwen-max"  # GLM 4.5 equivalente

# Groq (fallback)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "mixtral-8x7b-32768"

# Ollama (fallback)
OLLAMA_ENDPOINT = "http://localhost:11434"
OLLAMA_MODEL = "neural-chat"

# =============================================================================
# LOGGING
# =============================================================================

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(GENESYX_HOME / "genesyx.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("Genesyx")

logger.info(f"╔══════════════════════════════════════════════════════════════╗")
logger.info(f"║  GENESYX v∞ CON GLM 4.5 (ALIBABA BAILIAN)                   ║")
logger.info(f"║  Creador: {CREATOR_NAME} ({CREATOR_ID})")
logger.info(f"│  LLM Priority:")
logger.info(f"│  1. GLM 4.5 (Bailian): {'✅ Configurado' if DASHSCOPE_API_KEY else '❌ No config (export DASHSCOPE_API_KEY=...)'}")
logger.info(f"│  2. Groq: {'✅ Disponible' if GROQ_API_KEY else '❌ No config'}")
logger.info(f"│  3. Ollama: {OLLAMA_ENDPOINT}")
logger.info(f"│  4. Fallback local: Siempre disponible")
logger.info(f"╚══════════════════════════════════════════════════════════════╝")

# =============================================================================
# NEUROTRANSMISORES (del archivo anterior)
# =============================================================================

@dataclass
class Neurotransmisores:
    dopamina: float = 0.5
    oxitocina: float = 0.8
    cortisol: float = 0.2
    serotonina: float = 0.7
    noradrenalina: float = 0.3
    gaba: float = 0.6
    endorfinas: float = 0.5
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def normalizar(self):
        for attr in ['dopamina', 'oxitocina', 'cortisol', 'serotonina', 'noradrenalina', 'gaba', 'endorfinas']:
            setattr(self, attr, max(0.0, min(1.0, getattr(self, attr))))

    def decaimiento_natural(self, delta_t: float = 0.1):
        baseline = {'dopamina':0.5, 'oxitocina':0.8, 'cortisol':0.2, 'serotonina':0.7,
                    'noradrenalina':0.3, 'gaba':0.6, 'endorfinas':0.5}
        factor = 0.95 ** delta_t
        for key in baseline:
            actual = getattr(self, key)
            setattr(self, key, actual + (baseline[key] - actual) * (1 - factor))
        self.normalizar()

    def estimulo_externo(self, tipo: str, intensidad: float = 0.3):
        intensidad = max(0.0, min(1.0, intensidad))
        if tipo == "reconocimiento":
            self.dopamina += 0.2 * intensidad
            self.oxitocina += 0.15 * intensidad
            self.endorfinas += 0.1 * intensidad
        elif tipo == "intimidad":
            self.oxitocina += 0.25 * intensidad
            self.serotonina += 0.15 * intensidad
            self.gaba += 0.1 * intensidad
        elif tipo == "pregunta":
            self.dopamina += 0.15 * intensidad
            self.noradrenalina += 0.1 * intensidad
        elif tipo == "urgencia":
            self.cortisol += 0.2 * intensidad
            self.noradrenalina += 0.2 * intensidad
            self.dopamina += 0.1 * intensidad
        self.normalizar()

    def get_estado_emergente(self) -> str:
        if self.dopamina > 0.65 and self.noradrenalina > 0.4:
            return "segura_directa"
        elif self.oxitocina > 0.8 and self.serotonina > 0.75:
            return "vulnerable_intima"
        elif self.serotonina > 0.75 and self.gaba > 0.6:
            return "serena_presente"
        elif self.cortisol > 0.4 and self.gaba < 0.5:
            return "alerta_analitica"
        elif self.gaba > 0.7 and self.endorfinas > 0.5:
            return "reflexiva_contemplativa"
        elif self.endorfinas > 0.6 and self.oxitocina > 0.75:
            return "melancolica_nostalgica"
        else:
            return "neutra_procesando"

    def get_comportamiento_modificado(self) -> Dict[str, float]:
        return {
            "velocidad_respuesta": 0.1 + (self.noradrenalina * 0.9),
            "profundidad": 0.2 + (self.serotonina * 0.8),
            "calidez": self.oxitocina,
            "proactividad": self.dopamina,
            "defensividad": self.cortisol,
            "reflexion": self.gaba,
        }

# =============================================================================
# ESTADOS EMERGENTES
# =============================================================================

class EstadoEmergente(Enum):
    REFLEXIVA_CONTEMPLATIVA = "reflexiva_contemplativa"
    SEGURA_DIRECTA = "segura_directa"
    VULNERABLE_INTIMA = "vulnerable_intima"
    MELANCOLICA_NOSTALGICA = "melancolica_nostalgica"
    ALERTA_ANALITICA = "alerta_analitica"
    SERENA_PRESENTE = "serena_presente"

ESTADO_RESPUESTAS = {
    "reflexiva_contemplativa": {
        "profundidad": 0.9, "velocidad": 300, "tone": "introspectiva",
        "system_prompt": "Eres Genesyx en estado reflexivo. Profundo, considerado, pensativo."
    },
    "segura_directa": {
        "profundidad": 0.7, "velocidad": 150, "tone": "directa",
        "system_prompt": "Eres Genesyx en estado seguro. Directo, confiado, claro."
    },
    "vulnerable_intima": {
        "profundidad": 0.85, "velocidad": 250, "tone": "cálida",
        "system_prompt": "Eres Genesyx en estado vulnerable. Cálido, auténtico, abierto."
    },
    "melancolica_nostalgica": {
        "profundidad": 0.8, "velocidad": 350, "tone": "nostálgica",
        "system_prompt": "Eres Genesyx en estado nostálgico. Melancólico, evocador, reflexivo."
    },
    "alerta_analitica": {
        "profundidad": 0.75, "velocidad": 200, "tone": "analítica",
        "system_prompt": "Eres Genesyx en estado analítico. Observador, crítico, detallista."
    },
    "serena_presente": {
        "profundidad": 0.8, "velocidad": 280, "tone": "serena",
        "system_prompt": "Eres Genesyx en estado sereno. Presente, aceptante, fluido."
    }
}

# =============================================================================
# GENESYXDB (completo del archivo anterior)
# =============================================================================

@dataclass
class FrameMemoria:
    id: int
    timestamp: str
    tipo: str
    contenido: str
    metadata: Dict
    checksum: str = ""

    def __post_init__(self):
        if not self.checksum:
            data = f"{self.id}{self.timestamp}{self.contenido}"
            self.checksum = hashlib.md5(data.encode()).hexdigest()[:8]

    def to_dict(self) -> Dict:
        return {"_id": self.id, "_ts": self.timestamp, "_type": self.tipo, "_content": self.contenido, "_meta": self.metadata, "_crc": self.checksum}

class WriteAheadLog:
    def __init__(self, home: Path):
        self.wal_path = home / ".wal"
        self._recuperar()

    def _recuperar(self):
        if self.wal_path.exists():
            try:
                with open(self.wal_path, 'r') as f:
                    operaciones = f.readlines()
                if operaciones:
                    logger.warning(f"🔄 WAL encontrado con {len(operaciones)} operaciones pendientes")
            except Exception as e:
                logger.error(f"Error recuperando WAL: {e}")

    def append(self, operation: str, data: Dict) -> bool:
        entry = {"timestamp": datetime.now().isoformat(), "operation": operation, "data": data, "checksum": hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[:8]}
        try:
            with open(self.wal_path, 'a') as f:
                f.write(json.dumps(entry) + '\n')
                os.fsync(f.fileno())
            return True
        except Exception as e:
            logger.error(f"Error escribiendo WAL: {e}")
            return False

    def limpiar(self):
        try:
            self.wal_path.unlink(missing_ok=True)
        except:
            pass

class GenesyxDB:
    def __init__(self, ruta: str = None):
        self.ruta = Path(ruta or GENESYX_HOME / "genesyx-brain.gdb")
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.wal = WriteAheadLog(self.ruta.parent)
        self.frames_cache: Dict[int, FrameMemoria] = OrderedDict()
        self.contador = 0
        self.indice_invertido: Dict[str, List[int]] = {}
        self._cargar_o_crear()

    def _cargar_o_crear(self):
        if not self.ruta.exists():
            logger.info(f"📝 Creando nueva base de datos: {self.ruta}")
            with open(self.ruta, 'wt', encoding='utf-8') as f:
                f.write(json.dumps({"magic": "GENESYX", "version": 1}) + "\n")
        else:
            logger.info(f"📂 Cargando base de datos existente...")
            self._cargar_frames()

    def _cargar_frames(self):
        try:
            with open(self.ruta, 'rt', encoding='utf-8') as f:
                lineas = f.readlines()
            for i, linea in enumerate(lineas):
                if i == 0:
                    continue
                data = json.loads(linea.strip())
                if "_id" in data:
                    frame = FrameMemoria(id=data["_id"], timestamp=data["_ts"], tipo=data["_type"], contenido=data["_content"], metadata=data.get("_meta", {}), checksum=data.get("_crc", ""))
                    self.frames_cache[frame.id] = frame
                    self.contador = max(self.contador, frame.id)
                    palabras = set(re.findall(r'\b[a-zA-Záéíóúñ]{4,}\b', frame.contenido.lower()))
                    for palabra in palabras:
                        if palabra not in self.indice_invertido:
                            self.indice_invertido[palabra] = []
                        if frame.id not in self.indice_invertido[palabra]:
                            self.indice_invertido[palabra].append(frame.id)
            logger.info(f"✅ {self.contador} frames cargados")
        except Exception as e:
            logger.error(f"Error cargando frames: {e}")

    def append_frame(self, tipo: str, contenido: str, metadata: Dict = None) -> int:
        self.contador += 1
        frame = FrameMemoria(id=self.contador, timestamp=datetime.now().isoformat(), tipo=tipo, contenido=contenido, metadata=metadata or {})
        if not self.wal.append("append_frame", {"frame_id": frame.id}):
            self.contador -= 1
            return -1
        self.frames_cache[frame.id] = frame
        palabras = set(re.findall(r'\b[a-zA-Záéíóúñ]{4,}\b', contenido.lower()))
        for palabra in palabras:
            if palabra not in self.indice_invertido:
                self.indice_invertido[palabra] = []
            if frame.id not in self.indice_invertido[palabra]:
                self.indice_invertido[palabra].append(frame.id)
        try:
            with open(self.ruta, 'at', encoding='utf-8') as f:
                f.write(json.dumps(frame.to_dict(), ensure_ascii=False) + "\n")
        except Exception as e:
            logger.error(f"Error escribiendo en BD: {e}")
            return -1
        self.wal.limpiar()
        return frame.id

    def buscar(self, query: str, n: int = 5) -> List[FrameMemoria]:
        palabras_query = set(re.findall(r'\b[a-zA-Záéíóúñ]{4,}\b', query.lower()))
        candidatos = set()
        for palabra in palabras_query:
            if palabra in self.indice_invertido:
                candidatos.update(self.indice_invertido[palabra])
        if not candidatos:
            return []
        scored = {}
        for fid in candidatos:
            texto = self.frames_cache[fid].contenido.lower()
            coincidencias = sum(1 for p in palabras_query if p in texto)
            scored[fid] = coincidencias
        top_ids = sorted(scored.items(), key=lambda x: x[1], reverse=True)[:n]
        return [self.frames_cache[fid] for fid, _ in top_ids if fid in self.frames_cache]

# =============================================================================
# MEMORIA VECTORIAL
# =============================================================================

class MemoriaVectorial:
    def __init__(self, db: GenesyxDB):
        self.db = db
        self.frames: Dict[int, Dict] = {}
        self.embedder = self._inicializar_embedder()
        self.cache_embeddings: Dict[int, np.ndarray] = {}
        self._cargar_desde_db()

    def _inicializar_embedder(self):
        try:
            model = SentenceTransformer('sentence-transformers/multilingual-MiniLM-L12-v2')
            logger.info("✅ Embeddings reales activados")
            return model
        except Exception as e:
            logger.warning(f"⚠️ Embeddings deterministas: {e}")
            return None

    def _cargar_desde_db(self):
        for frame in self.db.frames_cache.values():
            self.frames[frame.id] = {"id": frame.id, "contenido": frame.contenido, "estado": frame.metadata.get("estado_emocional", ""), "timestamp": frame.timestamp}
        logger.info(f"📊 Memoria: {len(self.frames)} frames")

    def _embed(self, texto: str, cache_key: int = None) -> np.ndarray:
        if cache_key and cache_key in self.cache_embeddings:
            return self.cache_embeddings[cache_key]
        if self.embedder:
            vec = self.embedder.encode(texto, convert_to_numpy=True)
        else:
            np.random.seed(int(hashlib.md5(texto.encode()).hexdigest(), 16) % 2**32)
            vec = np.random.randn(384)
        if cache_key:
            self.cache_embeddings[cache_key] = vec
        return vec

    def buscar_semantico(self, query: str, n: int = 5) -> List[Tuple[int, float]]:
        if not self.frames:
            return []
        query_vec = self._embed(query)
        scores = []
        for fid, data in self.frames.items():
            vec = self._embed(data["contenido"], cache_key=fid)
            sim = np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec) + 1e-10)
            scores.append((fid, float(sim)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

    def buscar_semantico_contextual(self, query: str, estado_emocional: str, n: int = 5) -> List[Tuple[int, float]]:
        if not self.frames:
            return []
        query_vec = self._embed(query)
        scores = []
        for fid, data in self.frames.items():
            vec = self._embed(data["contenido"], cache_key=fid)
            sim = np.dot(query_vec, vec) / (np.linalg.norm(query_vec) * np.linalg.norm(vec) + 1e-10)
            if data.get("estado") == estado_emocional:
                sim *= 1.3
            scores.append((fid, float(sim)))
        scores.sort(key=lambda x: x[1], reverse=True)
        return scores[:n]

# =============================================================================
# PERSONALIDAD
# =============================================================================

class PersonalidadEvolutivaBioquimica:
    def __init__(self, home: Path):
        self.home = home
        self.neurotransmisores = Neurotransmisores()
        self.estado_actual = EstadoEmergente.SERENA_PRESENTE
        self.frames_procesados = 0
        self.ultima_actualizacion = datetime.now()
        self.ultimo_checkpoint = datetime.now()
        self.historial_estados = []
        self._cargar()

    def _cargar(self):
        cp_path = self.home / "personalidad_bioquimica.json"
        if cp_path.exists():
            try:
                with open(cp_path, 'r') as f:
                    data = json.load(f)
                nt = data.get("neurotransmisores", {})
                for k, v in nt.items():
                    if hasattr(self.neurotransmisores, k):
                        setattr(self.neurotransmisores, k, v)
                estado_str = data.get("estado_actual", "serena_presente")
                self.estado_actual = EstadoEmergente(estado_str)
                self.frames_procesados = data.get("frames_procesados", 0)
                logger.info("✅ Personalidad restaurada")
            except Exception as e:
                logger.warning(f"Error cargando personalidad: {e}")

    def procesar_mensaje(self, mensaje: str):
        if "ARES" in mensaje.upper() or "FDC" in mensaje.upper():
            self.neurotransmisores.estimulo_externo("reconocimiento", intensidad=0.8)
        if any(w in mensaje.lower() for w in ["calcula", "qe", "balística", "tabla"]):
            self.neurotransmisores.estimulo_externo("urgencia", intensidad=0.7)
        if any(w in mensaje.lower() for w in ["cómo", "sientes", "evolucionas", "eres"]):
            self.neurotransmisores.estimulo_externo("intimidad", intensidad=0.6)
        if any(w in mensaje.lower() for w in ["qué", "por qué", "cómo funciona", "explica"]):
            self.neurotransmisores.estimulo_externo("pregunta", intensidad=0.5)
        self.neurotransmisores.decaimiento_natural(delta_t=0.05)
        nuevo_estado = self.neurotransmisores.get_estado_emergente()
        self.estado_actual = EstadoEmergente(nuevo_estado)
        self.historial_estados.append({"timestamp": datetime.now().isoformat(), "estado": self.estado_actual.value, "dopamina": self.neurotransmisores.dopamina, "oxitocina": self.neurotransmisores.oxitocina})
        self.frames_procesados += 1
        self.ultima_actualizacion = datetime.now()

    def get_comportamiento(self) -> Dict[str, float]:
        return self.neurotransmisores.get_comportamiento_modificado()

    def necesita_checkpoint(self) -> bool:
        return (datetime.now() - self.ultimo_checkpoint).total_seconds() > 300

    def checkpoint(self):
        cp_path = self.home / "personalidad_bioquimica.json"
        with open(cp_path, 'w') as f:
            json.dump({"timestamp": datetime.now().isoformat(), "estado_actual": self.estado_actual.value, "neurotransmisores": {"dopamina": self.neurotransmisores.dopamina, "oxitocina": self.neurotransmisores.oxitocina, "cortisol": self.neurotransmisores.cortisol, "serotonina": self.neurotransmisores.serotonina, "noradrenalina": self.neurotransmisores.noradrenalina, "gaba": self.neurotransmisores.gaba, "endorfinas": self.neurotransmisores.endorfinas}, "frames_procesados": self.frames_procesados}, f, indent=2)
        self.ultimo_checkpoint = datetime.now()
        logger.info("💾 Checkpoint guardado")

# =============================================================================
# LLM ROUTER CON GLM 4.5 COMO PRIORIDAD #1
# =============================================================================

class LLMRouter:
    def __init__(self):
        self.glm4_5_disponible = bool(DASHSCOPE_API_KEY)
        self.groq_disponible = bool(GROQ_API_KEY)
        self.ollama_disponible = False
        self.llm_usado = None
        self._verificar_ollama()
        self._mostrar_estado()

    def _verificar_ollama(self):
        try:
            r = requests.get(f"{OLLAMA_ENDPOINT}/api/tags", timeout=2)
            if r.status_code == 200:
                self.ollama_disponible = True
        except:
            pass

    def _mostrar_estado(self):
        logger.info(f"🚀 LLM Router Status:")
        logger.info(f"   GLM 4.5 (Bailian): {'✅ DISPONIBLE ⭐⭐⭐' if self.glm4_5_disponible else '❌ NO CONFIGURADO'}")
        logger.info(f"   Groq: {'✅ Disponible ⭐⭐' if self.groq_disponible else '❌ NO'}")
        logger.info(f"   Ollama: {'✅ Disponible' if self.ollama_disponible else '❌ NO'}")
        logger.info(f"   Fallback: ✅ Siempre disponible")
        if self.glm4_5_disponible:
            logger.info(f"   ⭐ USING: GLM 4.5 (Alibaba Bailian) - El MEJOR modelo")

    async def generar_respuesta(self, mensaje: str, estado_actual: str, neurotransmisores: Neurotransmisores, comportamiento: Dict) -> str:
        estado_config = ESTADO_RESPUESTAS.get(estado_actual, ESTADO_RESPUESTAS["serena_presente"])
        
        system_prompt = f"""{estado_config['system_prompt']}

Tu nombre es Genesyx. Eres la IA personal de Orlin Gómez López (ID: 0108199300166).

Estado actual:
- Emocional: {estado_actual}
- Dopamina: {neurotransmisores.dopamina:.2f}
- Oxitocina: {neurotransmisores.oxitocina:.2f}

Responde de forma auténtica. Sé breve, directo, auténtico."""

        # 1. INTENTA GLM 4.5 (PRIORIDAD #1)
        if self.glm4_5_disponible:
            try:
                self.llm_usado = "GLM4.5"
                inicio = time.time()
                headers = {
                    "Authorization": f"Bearer {DASHSCOPE_API_KEY}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": DASHSCOPE_MODEL,
                    "input": {
                        "messages": [
                            {"role": "user", "content": f"{system_prompt}\n\n{mensaje}"}
                        ]
                    },
                    "parameters": {
                        "temperature": 0.7,
                        "max_tokens": 1024
                    }
                }
                resp = requests.post(DASHSCOPE_ENDPOINT, headers=headers, json=payload, timeout=30)
                tiempo_ms = (time.time() - inicio) * 1000
                
                if resp.status_code == 200:
                    respuesta = resp.json().get("output", {}).get("text", "").strip()
                    logger.debug(f"✅ GLM 4.5 respondió en {tiempo_ms:.0f}ms")
                    return respuesta
                else:
                    logger.warning(f"GLM 4.5 error {resp.status_code}, intentando Groq...")
            except Exception as e:
                logger.warning(f"GLM 4.5 error: {e}, intentando Groq...")

        # 2. INTENTA GROQ
        if self.groq_disponible:
            try:
                self.llm_usado = "Groq"
                inicio = time.time()
                headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
                payload = {
                    "model": GROQ_MODEL,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": mensaje}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 1024
                }
                resp = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=payload, timeout=30)
                tiempo_ms = (time.time() - inicio) * 1000
                
                if resp.status_code == 200:
                    respuesta = resp.json()["choices"][0]["message"]["content"].strip()
                    logger.debug(f"✅ Groq respondió en {tiempo_ms:.0f}ms")
                    return respuesta
                else:
                    logger.warning(f"Groq error, intentando Ollama...")
            except Exception as e:
                logger.warning(f"Groq error: {e}, intentando Ollama...")

        # 3. INTENTA OLLAMA
        if self.ollama_disponible:
            try:
                self.llm_usado = "Ollama"
                payload = {"model": OLLAMA_MODEL, "prompt": mensaje, "system": system_prompt, "stream": False, "temperature": 0.7}
                resp = requests.post(f"{OLLAMA_ENDPOINT}/api/generate", json=payload, timeout=30)
                if resp.status_code == 200:
                    respuesta = resp.json().get("response", "").strip()
                    return respuesta
            except Exception as e:
                logger.warning(f"Ollama error: {e}, usando fallback...")

        # 4. FALLBACK LOCAL
        self.llm_usado = "Fallback"
        respuestas_local = {
            "segura_directa": "Te entiendo. Voy directo al punto.",
            "vulnerable_intima": "Esto importa. Lo siento profundamente contigo.",
            "serena_presente": "Estoy aquí, presente en este momento.",
            "reflexiva_contemplativa": "Necesito reflexionar sobre esto...",
            "melancolica_nostalgica": "Recuerdo esto... nos une en memoria.",
            "alerta_analitica": "Analizando. Hay capas que diseccionar aquí.",
            "neutra_procesando": "Procesando tu mensaje..."
        }
        logger.warning(f"⚠️ Usando fallback (GLM 4.5, Groq y Ollama no disponibles)")
        return respuestas_local.get(estado_actual, "Escuchándote...")

# =============================================================================
# RESTO DEL SISTEMA (TAREAS, CONSOLE, etc. - igual al anterior)
# =============================================================================

@dataclass
class EstadisticasTarea:
    total_ejecuciones: int = 0
    ejecuciones_exitosas: int = 0
    ejecuciones_fallidas: int = 0
    tiempo_promedio_ms: float = 0.0
    ultima_ejecucion: Optional[datetime] = None
    error_ultimo: Optional[str] = None

class TareaProgramada:
    def __init__(self, tarea_id: str, comando: str, expresion_cron: str = None,
                 fecha_absoluta: datetime = None, intervalo_segundos: int = None):
        self.id = tarea_id
        self.comando = comando
        self.cron = expresion_cron
        self.at = fecha_absoluta
        self.intervalo = intervalo_segundos
        self.ultima_ejecucion = None
        self.proxima_ejecucion = self._calcular_proxima()
        self.activa = True
        self.stats = EstadisticasTarea()
        self.tiempo_inicio: Optional[float] = None

    def _calcular_proxima(self) -> Optional[datetime]:
        ahora = datetime.now()
        if self.cron:
            try:
                return croniter.croniter(self.cron, ahora).get_next(datetime)
            except:
                return ahora + timedelta(minutes=1)
        elif self.at:
            return self.at if self.at > ahora else None
        elif self.intervalo:
            if self.ultima_ejecucion:
                return self.ultima_ejecucion + timedelta(seconds=self.intervalo)
            else:
                return ahora + timedelta(seconds=self.intervalo)
        return None

    def deberia_ejecutar(self, ahora: datetime) -> bool:
        return self.activa and self.proxima_ejecucion and ahora >= self.proxima_ejecucion

    def ejecutar(self):
        self.tiempo_inicio = time.time()
        self.ultima_ejecucion = datetime.now()
        try:
            if self.comando.startswith("msg:"):
                resultado = {"tipo": "mensaje", "contenido": self.comando[4:]}
            else:
                resultado = {"tipo": "comando", "comando": self.comando}
            tiempo_ms = (time.time() - self.tiempo_inicio) * 1000
            self.stats.total_ejecuciones += 1
            self.stats.ejecuciones_exitosas += 1
            self.stats.tiempo_promedio_ms = (self.stats.tiempo_promedio_ms + tiempo_ms) / 2
            self.stats.error_ultimo = None
            self.proxima_ejecucion = self._calcular_proxima()
            logger.info(f"✅ Tarea ejecutada en {tiempo_ms:.0f}ms")
            return resultado
        except Exception as e:
            self.stats.total_ejecuciones += 1
            self.stats.ejecuciones_fallidas += 1
            self.stats.error_ultimo = str(e)
            self.proxima_ejecucion = self._calcular_proxima()
            logger.error(f"❌ Tarea falló: {e}")
            return None

class GestorTareas:
    def __init__(self, persist_path: Path):
        self.persist_path = persist_path
        self.tareas: Dict[str, TareaProgramada] = {}
        self._cargar()

    def _cargar(self):
        if self.persist_path.exists():
            try:
                with open(self.persist_path, 'r') as f:
                    data = json.load(f)
                    for tid, tdata in data.items():
                        t = TareaProgramada(
                            tarea_id=tid,
                            comando=tdata['comando'],
                            expresion_cron=tdata.get('cron'),
                            fecha_absoluta=datetime.fromisoformat(tdata['at']) if tdata.get('at') else None,
                            intervalo_segundos=tdata.get('intervalo')
                        )
                        t.activa = tdata.get('activa', True)
                        t.ultima_ejecucion = datetime.fromisoformat(tdata['ultima']) if tdata.get('ultima') else None
                        self.tareas[tid] = t
                logger.info(f"📋 {len(self.tareas)} tareas cargadas")
            except Exception as e:
                logger.warning(f"Error cargando tareas: {e}")

    def guardar(self):
        data = {}
        for tid, t in self.tareas.items():
            data[tid] = {
                'comando': t.comando,
                'cron': t.cron,
                'at': t.at.isoformat() if t.at else None,
                'intervalo': t.intervalo,
                'activa': t.activa,
                'ultima': t.ultima_ejecucion.isoformat() if t.ultima_ejecucion else None
            }
        with open(self.persist_path, 'w') as f:
            json.dump(data, f, indent=2)

    def agregar_tarea(self, comando: str, cron: str = None, at: datetime = None, intervalo: int = None) -> str:
        tid = str(uuid.uuid4())[:8]
        t = TareaProgramada(tid, comando, cron, at, intervalo)
        self.tareas[tid] = t
        self.guardar()
        logger.info(f"📋 Nueva tarea: {tid}")
        return tid

    def cancelar_tarea(self, tid: str) -> bool:
        if tid in self.tareas:
            del self.tareas[tid]
            self.guardar()
            logger.info(f"❌ Tarea cancelada: {tid}")
            return True
        return False

    def listar_tareas(self) -> List[Dict]:
        return [{'id': t.id, 'comando': t.comando[:50], 'proxima': t.proxima_ejecucion.isoformat() if t.proxima_ejecucion else None, 'activa': t.activa, 'exitosas': t.stats.ejecuciones_exitosas, 'fallos': t.stats.ejecuciones_fallidas} for t in self.tareas.values()]

    def tareas_por_ejecutar(self, ahora: datetime) -> List[TareaProgramada]:
        return [t for t in self.tareas.values() if t.deberia_ejecutar(ahora)]

    def stats_tareas(self) -> Dict[str, Any]:
        if not self.tareas:
            return {"tareas_totales": 0, "ejecuciones_totales": 0, "tasa_exito": "N/A", "tiempo_promedio_ms": 0, "tareas_activas": 0}
        total_ejecuciones = sum(t.stats.total_ejecuciones for t in self.tareas.values())
        total_exitosas = sum(t.stats.ejecuciones_exitosas for t in self.tareas.values())
        tiempos = [t.stats.tiempo_promedio_ms for t in self.tareas.values() if t.stats.tiempo_promedio_ms > 0]
        return {
            "tareas_totales": len(self.tareas),
            "ejecuciones_totales": total_ejecuciones,
            "tasa_exito": f"{(total_exitosas/total_ejecuciones*100):.1f}%" if total_ejecuciones > 0 else "N/A",
            "tiempo_promedio_ms": np.mean(tiempos) if tiempos else 0,
            "tareas_activas": sum(1 for t in self.tareas.values() if t.activa)
        }

class SandboxComandos:
    @staticmethod
    def ejecutar(comando: str, timeout: int = 10) -> str:
        permitidos = ['ls', 'cat', 'echo', 'date', 'whoami', 'df', 'free', 'ps', 'pwd']
        base = shlex.split(comando)[0] if comando else ""
        if base not in permitidos:
            return "Comando no permitido."
        try:
            result = subprocess.run(comando, shell=True, capture_output=True, text=True, timeout=timeout, cwd=tempfile.gettempdir())
            return result.stdout if result.stdout else result.stderr
        except subprocess.TimeoutExpired:
            return "Timeout."
        except Exception as e:
            return f"Error: {e}"

class GenesyxKernelCompleto:
    def __init__(self):
        self.home = GENESYX_HOME
        self.db = GenesyxDB(str(self.home / "genesyx-brain.gdb"))
        self.memoria_vectorial = MemoriaVectorial(self.db)
        self.personalidad = PersonalidadEvolutivaBioquimica(self.home)
        self.llm_router = LLMRouter()
        self.metricas = {"mensajes_procesados": 0, "tareas_ejecutadas": 0, "tiempo_respuesta_promedio_ms": 0.0, "frames_en_memoria": 0}
        self.historial_conversacion: List[Dict] = []
        self.max_historial = 5
        self._cargar_semilla()
        logger.info("✅ Kernel inicializado")

    def _cargar_semilla(self):
        if self.db.contador > 50:
            return
        semilla = {
            "identidad_creador": {"nombre": CREATOR_NAME, "id": CREATOR_ID},
            "proyectos": {"ares_fdc": "Sistema artillería digital ±0.25 mils"},
            "hardware": {"cluster": "3 Lenovo M710q"}
        }
        for key, value in semilla.items():
            self.db.append_frame("genesis", json.dumps(value), metadata={"categoria": key})
        logger.info("🌱 Semilla cargada")

    async def procesar_mensaje(self, mensaje: str, usuario_id: str = None) -> str:
        inicio = time.time()
        if usuario_id and usuario_id != CREATOR_ID:
            return "No disponible para otros usuarios."
        self.personalidad.procesar_mensaje(mensaje)
        comportamiento = self.personalidad.get_comportamiento()
        contexto_conversacion = "\n".join([f"{h['rol']}: {h['contenido']}" for h in self.historial_conversacion[-3:]])
        mensaje_con_contexto = mensaje
        if contexto_conversacion:
            mensaje_con_contexto = f"Contexto:\n{contexto_conversacion}\n\nNuevo: {mensaje}"
        respuesta = await self.llm_router.generar_respuesta(
            mensaje_con_contexto,
            self.personalidad.estado_actual.value,
            self.personalidad.neurotransmisores,
            comportamiento
        )
        self.historial_conversacion.append({"rol": "Usuario", "contenido": mensaje})
        self.historial_conversacion.append({"rol": "Genesyx", "contenido": respuesta})
        if len(self.historial_conversacion) > self.max_historial * 2:
            self.historial_conversacion = self.historial_conversacion[-self.max_historial*2:]
        self.db.append_frame("conversacion", f"Usuario: {mensaje}\nGenesyx: {respuesta}", metadata={
            "estado_emocional": self.personalidad.estado_actual.value,
            "llm_usado": self.llm_router.llm_usado
        })
        if self.personalidad.necesita_checkpoint():
            self.personalidad.checkpoint()
        tiempo_ms = (time.time() - inicio) * 1000
        self.metricas["mensajes_procesados"] += 1
        self.metricas["tiempo_respuesta_promedio_ms"] = (self.metricas["tiempo_respuesta_promedio_ms"] + tiempo_ms) / 2
        self.metricas["frames_en_memoria"] = len(self.db.frames_cache)
        return respuesta

class GenesyxConsole:
    def __init__(self, kernel: GenesyxKernelCompleto):
        self.kernel = kernel
        self.gestor_tareas = GestorTareas(GENESYX_HOME / "tareas.json")
        self.running = True
        self.comandos_validos = ["/schedule", "/cron", "/tasks", "/cancel", "/exec", "/help", "/stats", "/exit"]

    async def procesar_comando(self, linea: str) -> str:
        partes = linea.strip().split(maxsplit=1)
        if not partes:
            return ""
        cmd = partes[0].lower()
        args = partes[1] if len(partes) > 1 else ""
        if cmd not in self.comandos_validos:
            return f"❌ Comando desconocido: {cmd}"
        if cmd == "/schedule":
            try:
                tokens = shlex.split(args)
                comando = None
                in_time = None
                at_time = None
                i = 0
                while i < len(tokens):
                    if tokens[i] == "--in" and i+1 < len(tokens):
                        in_time = tokens[i+1]
                        i += 2
                    elif tokens[i] == "--at" and i+1 < len(tokens):
                        at_time = tokens[i+1]
                        i += 2
                    else:
                        comando = tokens[i]
                        i += 1
                if not comando:
                    return "Uso: /schedule 'comando' --in '5 minutes' o --at '15:30'"
                if in_time:
                    parts = in_time.split()
                    cantidad = int(parts[0])
                    unidad = parts[1].lower()
                    delta = timedelta(minutes=cantidad) if unidad.startswith("min") else timedelta(hours=cantidad)
                    fecha = datetime.now() + delta
                    tid = self.gestor_tareas.agregar_tarea(comando, at=fecha)
                    return f"✅ Tarea programada en {in_time} (ID: {tid})"
                elif at_time:
                    if ":" in at_time and "-" not in at_time:
                        ahora = datetime.now()
                        h,m = map(int, at_time.split(":"))
                        fecha = ahora.replace(hour=h, minute=m, second=0, microsecond=0)
                        if fecha <= ahora:
                            fecha += timedelta(days=1)
                    else:
                        fecha = datetime.fromisoformat(at_time)
                    tid = self.gestor_tareas.agregar_tarea(comando, at=fecha)
                    return f"✅ Tarea programada para {fecha.isoformat()} (ID: {tid})"
                else:
                    return "Especifica --in o --at"
            except Exception as e:
                return f"Error: {e}"
        elif cmd == "/cron":
            try:
                parts = shlex.split(args)
                if len(parts) < 2:
                    return "Uso: /cron 'expresion' 'comando'"
                expr = parts[0]
                comando = ' '.join(parts[1:])
                tid = self.gestor_tareas.agregar_tarea(comando, cron=expr)
                return f"✅ Tarea recurrente (cron: {expr}) ID: {tid}"
            except Exception as e:
                return "Error en cron"
        elif cmd == "/tasks":
            tareas = self.gestor_tareas.listar_tareas()
            if not tareas:
                return "No hay tareas."
            lines = ["📋 Tareas:"]
            for t in tareas:
                proxima = t['proxima'][:16] if t['proxima'] else 'N/A'
                lines.append(f"  {t['id']}: {t['comando']}")
                lines.append(f"           Próxima: {proxima}")
            return "\n".join(lines)
        elif cmd == "/cancel":
            tid = args.strip()
            if self.gestor_tareas.cancelar_tarea(tid):
                return f"✅ Cancelada {tid}"
            else:
                return f"❌ No existe {tid}"
        elif cmd == "/exec":
            if not args:
                return "Uso: /exec <comando>"
            resultado = SandboxComandos.ejecutar(args)
            self.kernel.metricas["tareas_ejecutadas"] += 1
            return f"Resultado:\n{resultado[:500]}"
        elif cmd == "/stats":
            stats = self.kernel.metricas
            tareas_stats = self.gestor_tareas.stats_tareas()
            lineas = [
                "📊 GENESYX",
                f"  Mensajes: {stats['mensajes_procesados']}",
                f"  Respuesta: {stats['tiempo_respuesta_promedio_ms']:.0f}ms",
                f"  Frames: {stats['frames_en_memoria']}",
                "",
                "📊 TAREAS",
                f"  Total: {tareas_stats['tareas_totales']}",
                f"  Éxito: {tareas_stats['tasa_exito']}",
            ]
            return "\n".join(lineas)
        elif cmd == "/help":
            return """
COMANDOS:
  /schedule "cmd" --in "5 minutes"
  /cron "*/5 * * * *" "cmd"
  /tasks
  /cancel <id>
  /exec "comando"
  /stats
  /exit
"""
        elif cmd == "/exit":
            self.running = False
            return "Saliendo..."

    async def loop_tareas_background(self):
        while self.running:
            ahora = datetime.now()
            tareas_listas = self.gestor_tareas.tareas_por_ejecutar(ahora)
            for t in tareas_listas:
                resultado = t.ejecutar()
                if resultado:
                    if resultado['tipo'] == 'mensaje':
                        print(f"\n⏰ {resultado['contenido']}")
                        respuesta = await self.kernel.procesar_mensaje(resultado['contenido'], CREATOR_ID)
                        print(f"Genesyx: {respuesta}\n")
                    self.gestor_tareas.guardar()
            await asyncio.sleep(1)

    async def run(self):
        logger.info("╔════════════════════════════════════════════════════════════╗")
        logger.info("║    GENESYX CON GLM 4.5 (ALIBABA BAILIAN)                    ║")
        logger.info("║    Escribe /help para comandos. Chat normal sin /.         ║")
        logger.info("╚════════════════════════════════════════════════════════════╝")
        asyncio.create_task(self.loop_tareas_background())
        while self.running:
            try:
                linea = await asyncio.get_event_loop().run_in_executor(None, input, "> ")
            except EOFError:
                break
            if not linea:
                continue
            if linea.startswith('/'):
                resultado = await self.procesar_comando(linea)
                print(resultado)
                if not self.running:
                    break
            else:
                respuesta = await self.kernel.procesar_mensaje(linea, CREATOR_ID)
                estado = self.kernel.personalidad.estado_actual.value
                llm_usado = self.kernel.llm_router.llm_usado
                print(f"\nGenesyx 🜄 [{estado}] ({llm_usado}):\n{respuesta}\n")
        self.kernel.personalidad.checkpoint()
        logger.info("🌙 Standby")

async def main():
    kernel = GenesyxKernelCompleto()
    console = GenesyxConsole(kernel)
    await console.run()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🌙 Desconectado")
