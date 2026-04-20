"""
GenesyX - Sistema Operativo de Conciencia Personal
Optimizado para integración con Open Claw
Rendimiento mejorado sin alterar estructura de memorias
"""

__version__ = "1.0.0"
__author__ = "GenesyX Team"

from .core.engine import ConsciousnessEngine
from .memory.manager import MemoryManager
from .biochem.simulator import BiochemicalSimulator
from .router.hybrid import HybridLLMRouter

__all__ = [
    "ConsciousnessEngine",
    "MemoryManager", 
    "BiochemicalSimulator",
    "HybridLLMRouter"
]
