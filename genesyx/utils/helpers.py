"""
Utilidades de alto rendimiento para GenesyX
Funciones optimizadas sin dependencias innecesarias
"""

import hashlib
import time
from typing import Any, Dict, List, Optional, Callable
from functools import wraps
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def generate_id(content: str) -> str:
    """Genera ID único optimizado usando SHA256"""
    return hashlib.sha256(
        f"{content}{time.time()}".encode()
    ).hexdigest()[:16]


def timing_decorator(func: Callable) -> Callable:
    """Decorador para medir tiempo de ejecución"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.debug(f"{func.__name__} executed in {elapsed:.4f}s")
        return result
    return wrapper


class PerformanceMonitor:
    """Monitor de rendimiento en tiempo real"""
    
    __slots__ = ['_metrics', '_start_time']
    
    def __init__(self):
        self._metrics: Dict[str, List[float]] = {}
        self._start_time = time.time()
        
    def record(self, metric_name: str, value: float) -> None:
        """Registra métrica"""
        if metric_name not in self._metrics:
            self._metrics[metric_name] = []
        self._metrics[metric_name].append(value)
        
        # Mantener solo últimos 1000 valores
        if len(self._metrics[metric_name]) > 1000:
            self._metrics[metric_name] = self._metrics[metric_name][-1000:]
            
    def get_stats(self, metric_name: str) -> Dict[str, float]:
        """Obtiene estadísticas de métrica"""
        if metric_name not in self._metrics or not self._metrics[metric_name]:
            return {'count': 0, 'avg': 0, 'min': 0, 'max': 0}
            
        values = self._metrics[metric_name]
        return {
            'count': len(values),
            'avg': sum(values) / len(values),
            'min': min(values),
            'max': max(values)
        }
        
    def get_uptime(self) -> float:
        """Obtiene tiempo de actividad en segundos"""
        return time.time() - self._start_time


class RingBuffer:
    """Buffer circular optimizado para streaming"""
    
    __slots__ = ['_buffer', '_size', '_index', '_full']
    
    def __init__(self, size: int = 1000):
        self._size = size
        self._buffer = [None] * size
        self._index = 0
        self._full = False
        
    def append(self, item: Any) -> None:
        """Añade elemento al buffer"""
        self._buffer[self._index] = item
        self._index = (self._index + 1) % self._size
        if self._index == 0:
            self._full = True
            
    def get_all(self) -> List[Any]:
        """Obtiene todos los elementos en orden"""
        if self._full:
            return self._buffer[self._index:] + self._buffer[:self._index]
        else:
            return self._buffer[:self._index]
            
    def get_last(self, n: int) -> List[Any]:
        """Obtiene últimos n elementos"""
        all_items = self.get_all()
        return all_items[-n:] if n < len(all_items) else all_items
        
    def clear(self) -> None:
        """Limpia el buffer"""
        self._buffer = [None] * self._size
        self._index = 0
        self._full = False


def batch_iterator(items: List[Any], batch_size: int):
    """Iterador por lotes optimizado"""
    for i in range(0, len(items), batch_size):
        yield items[i:i + batch_size]


async def async_retry(
    func: Callable,
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0
):
    """Ejecuta función asíncrona con reintentos exponenciales"""
    import asyncio
    
    current_delay = delay
    last_exception = None
    
    for attempt in range(max_retries):
        try:
            return await func()
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1} failed: {e}")
            
            if attempt < max_retries - 1:
                await asyncio.sleep(current_delay)
                current_delay *= backoff
                
    raise last_exception


def safe_json_serialize(obj: Any) -> Any:
    """Serializa objeto a formato JSON-safe"""
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: safe_json_serialize(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [safe_json_serialize(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return safe_json_serialize(obj.__dict__)
    else:
        return str(obj)
