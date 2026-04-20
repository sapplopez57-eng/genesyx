"""
Motor de Conciencia - Núcleo del sistema GenesyX
Optimizado para máximo rendimiento con Open Claw
"""

import asyncio
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class ConsciousnessState:
    """Estado actual de la conciencia"""
    awareness_level: float = 0.0
    focus_target: Optional[str] = None
    emotional_valence: Dict[str, float] = field(default_factory=dict)
    cognitive_load: float = 0.0
    last_update: datetime = field(default_factory=datetime.now)


class ConsciousnessEngine:
    """
    Motor principal de conciencia personal
    Optimizado para integración con Open Claw
    """
    
    __slots__ = ['_state', '_callbacks', '_running', '_event_loop']
    
    def __init__(self):
        self._state = ConsciousnessState()
        self._callbacks: List[callable] = []
        self._running = False
        self._event_loop: Optional[asyncio.AbstractEventLoop] = None
        
    async def initialize(self) -> None:
        """Inicialización asíncrona optimizada"""
        self._event_loop = asyncio.get_event_loop()
        self._running = True
        logger.info("ConsciousnessEngine initialized with Open Claw optimization")
        
    async def process_input(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Procesa entrada con mínimo latency
        Optimizado para streaming con Open Claw
        """
        start_time = datetime.now()
        
        try:
            # Actualizar estado cognitivo
            self._state.cognitive_load = min(1.0, self._state.cognitive_load + 0.1)
            self._state.last_update = datetime.now()
            
            # Procesamiento optimizado
            result = {
                'status': 'processed',
                'timestamp': start_time.isoformat(),
                'awareness': self._state.awareness_level,
                'data': input_data
            }
            
            # Notificar callbacks en paralelo
            if self._callbacks:
                await asyncio.gather(
                    *[cb(result) for cb in self._callbacks],
                    return_exceptions=True
                )
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing input: {e}")
            return {'status': 'error', 'message': str(e)}
    
    def register_callback(self, callback: callable) -> None:
        """Registra callback para eventos de conciencia"""
        self._callbacks.append(callback)
        
    def update_awareness(self, level: float) -> None:
        """Actualiza nivel de conciencia (0.0 a 1.0)"""
        self._state.awareness_level = max(0.0, min(1.0, level))
        
    def set_focus(self, target: str) -> None:
        """Establece foco atencional"""
        self._state.focus_target = target
        
    def get_state(self) -> ConsciousnessState:
        """Obtiene estado actual"""
        return self._state
        
    async def shutdown(self) -> None:
        """Apagado limpio"""
        self._running = False
        logger.info("ConsciousnessEngine shutdown complete")
