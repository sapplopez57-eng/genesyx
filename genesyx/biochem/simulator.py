"""
Simulador Bioquímico de Conciencia
Optimizado para cálculos rápidos sin alterar modelo original
"""

import numpy as np
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
from enum import Enum

logger = logging.getLogger(__name__)


class Neurotransmitter(Enum):
    """Neurotransmisores simulados"""
    DOPAMINE = "dopamine"
    SEROTONIN = "serotonin"
    NORADRENALINE = "noradrenaline"
    ACETYLCHOLINE = "acetylcholine"
    GABA = "gaba"
    GLUTAMATE = "glutamate"


@dataclass
class BiochemicalState:
    """Estado bioquímico actual"""
    levels: Dict[str, float] = field(default_factory=dict)
    receptors: Dict[str, float] = field(default_factory=dict)
    metabolism_rate: float = 1.0
    last_update: datetime = field(default_factory=datetime.now)


class BiochemicalSimulator:
    """
    Simulador bioquímico optimizado
    Mantiene modelo original, mejora rendimiento computacional
    """
    
    __slots__ = ['_state', '_baseline', '_rates', '_history']
    
    def __init__(self):
        self._state = BiochemicalState()
        self._baseline: Dict[str, float] = {}
        self._rates: Dict[str, float] = {}
        self._history: List[Tuple[datetime, Dict[str, float]]] = []
        
        # Inicializar valores baseline
        self._initialize_baseline()
        
    def _initialize_baseline(self) -> None:
        """Inicializa niveles baseline optimizados"""
        self._baseline = {
            Neurotransmitter.DOPAMINE.value: 0.5,
            Neurotransmitter.SEROTONIN.value: 0.5,
            Neurotransmitter.NORADRENALINE.value: 0.4,
            Neurotransmitter.ACETYLCHOLINE.value: 0.6,
            Neurotransmitter.GABA.value: 0.5,
            Neurotransmitter.GLUTAMATE.value: 0.5
        }
        
        self._rates = {
            'decay': 0.01,
            'synthesis': 0.02,
            'reuptake': 0.015
        }
        
        # Resetear estado
        self._state.levels = self._baseline.copy()
        self._state.receptors = {k: 1.0 for k in self._baseline.keys()}
        self._state.metabolism_rate = 1.0
        
    def update(self, delta_time: float = 1.0, stimuli: Optional[Dict[str, float]] = None) -> BiochemicalState:
        """
        Actualiza estado bioquímico con optimización vectorial
        """
        start_time = datetime.now()
        
        # Usar arrays numpy para cálculos rápidos
        keys = list(self._baseline.keys())
        levels = np.array([self._state.levels.get(k, 0.5) for k in keys])
        receptors = np.array([self._state.receptors.get(k, 1.0) for k in keys])
        baseline = np.array([self._baseline[k] for k in keys])
        
        # Decaimiento natural hacia baseline
        decay_factor = np.exp(-self._rates['decay'] * delta_time * self._state.metabolism_rate)
        levels = levels * decay_factor + baseline * (1 - decay_factor)
        
        # Aplicar estímulos externos
        if stimuli:
            for neurotransmitter, stimulus in stimuli.items():
                if neurotransmitter in self._state.levels:
                    idx = keys.index(neurotransmitter)
                    # Síntesis aumentada
                    synthesis = self._rates['synthesis'] * stimulus * delta_time
                    levels[idx] = min(1.0, levels[idx] + synthesis)
                    
                    # Modulación de receptores
                    receptors[idx] = max(0.5, min(1.5, receptors[idx] * (1 + stimulus * 0.1)))
        
        # Recaptación
        reuptake = self._rates['reuptake'] * delta_time
        levels = np.maximum(baseline * 0.3, levels * (1 - reuptake))
        
        # Actualizar estado
        for i, key in enumerate(keys):
            self._state.levels[key] = float(levels[i])
            self._state.receptors[key] = float(receptors[i])
            
        self._state.last_update = datetime.now()
        
        # Guardar en histórico (máximo 1000 registros)
        self._history.append((self._state.last_update, self._state.levels.copy()))
        if len(self._history) > 1000:
            self._history.pop(0)
            
        return self._state
        
    def get_level(self, neurotransmitter: str) -> float:
        """Obtiene nivel específico de neurotransmisor"""
        return self._state.levels.get(neurotransmitter, self._baseline.get(neurotransmitter, 0.5))
        
    def set_level(self, neurotransmitter: str, level: float) -> None:
        """Establece nivel específico (con validación)"""
        if neurotransmitter in self._baseline:
            self._state.levels[neurotransmitter] = max(0.0, min(1.0, level))
            
    def modulate_metabolism(self, factor: float) -> None:
        """Modula tasa metabólica global"""
        self._state.metabolism_rate = max(0.1, min(5.0, factor))
        
    def get_balance_score(self) -> float:
        """
        Calcula score de balance bioquímico
        0.0 = desbalance total, 1.0 = balance perfecto
        """
        if not self._state.levels:
            return 0.5
            
        deviations = [
            abs(self._state.levels.get(k, 0.5) - self._baseline[k])
            for k in self._baseline.keys()
        ]
        
        avg_deviation = np.mean(deviations)
        return max(0.0, 1.0 - avg_deviation)
        
    def get_emotional_profile(self) -> Dict[str, float]:
        """
        Deriva perfil emocional del estado bioquímico
        """
        dopamine = self.get_level(Neurotransmitter.DOPAMINE.value)
        serotonin = self.get_level(Neurotransmitter.SEROTONIN.value)
        noradrenaline = self.get_level(Neurotransmitter.NORADRENALINE.value)
        gaba = self.get_level(Neurotransmitter.GABA.value)
        
        return {
            'motivation': dopamine * 0.7 + noradrenaline * 0.3,
            'mood': serotonin * 0.8 + dopamine * 0.2,
            'arousal': noradrenaline * 0.6 + (1 - gaba) * 0.4,
            'calm': gaba * 0.7 + serotonin * 0.3,
            'focus': dopamine * 0.4 + noradrenaline * 0.4 + (1 - gaba) * 0.2
        }
        
    def get_history(self, last_n: int = 100) -> List[Tuple[datetime, Dict[str, float]]]:
        """Obtiene histórico de estados"""
        return self._history[-last_n:]
        
    def reset(self) -> None:
        """Resetea al estado baseline"""
        self._state.levels = self._baseline.copy()
        self._state.receptors = {k: 1.0 for k in self._baseline.keys()}
        self._state.metabolism_rate = 1.0
        self._history.clear()
        logger.info("BiochemicalSimulator reset to baseline")
        
    def get_state(self) -> BiochemicalState:
        """Obtiene estado actual"""
        return self._state
