"""
Router Híbrido LLM (Modelos Chinos Gratuitos + Ollama Local)
Enrutamiento inteligente con modelos Qwen, DeepSeek, Yi, ChatGLM sin APIs externas
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
from enum import Enum
import time

logger = logging.getLogger(__name__)


class LLMProvider(Enum):
    """Proveedores soportados - Modelos chinos gratuitos y locales"""
    QWEN = "qwen"           # Alibaba Qwen (open-source)
    DEEPSEEK = "deepseek"   # DeepSeek AI (open-source)
    YI = "yi"               # 01.AI Yi models (open-source)
    CHATGLM = "chatglm"     # Zhipu ChatGLM (open-source)
    INTERNLM = "internlm"   # Shanghai AI Lab InternLM
    OLLAMA = "ollama"       # Local con modelos chinos


@dataclass
class ProviderConfig:
    """Configuración de proveedor"""
    endpoint: str
    model: str
    api_key: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    priority: int = 1
    is_local: bool = True


@dataclass
class RoutingDecision:
    """Decisión de enrutamiento"""
    provider: LLMProvider
    model: str
    confidence: float
    latency_estimate: float
    cost_estimate: float
    reason: str


class HybridLLMRouter:
    """
    Router híbrido para modelos chinos gratuitos (Qwen, DeepSeek, Yi, ChatGLM, InternLM)
    + Ollama local. Sin dependencias de APIs externas.
    Selección inteligente de proveedor según contexto
    """
    
    __slots__ = ['_configs', '_session', '_stats', '_cache', '_health_status']
    
    def __init__(self):
        self._configs: Dict[LLMProvider, ProviderConfig] = {}
        self._session: Optional[aiohttp.ClientSession] = None
        self._stats: Dict[str, Any] = {
            'requests': 0,
            'success': 0,
            'failures': 0,
            'avg_latency': 0.0
        }
        self._cache: Dict[str, Tuple[Any, datetime]] = {}
        self._health_status: Dict[LLMProvider, bool] = {}
        
        self._initialize_default_configs()
        
    def _initialize_default_configs(self) -> None:
        """Inicializa configuraciones con modelos chinos open-source"""
        self._configs = {
            LLMProvider.QWEN: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="qwen2.5:7b",
                timeout=60.0,
                priority=0,
                is_local=True
            ),
            LLMProvider.DEEPSEEK: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="deepseek-coder:6.7b",
                timeout=60.0,
                priority=1,
                is_local=True
            ),
            LLMProvider.YI: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="yi:34b",
                timeout=60.0,
                priority=2,
                is_local=True
            ),
            LLMProvider.CHATGLM: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="chatglm3:6b",
                timeout=60.0,
                priority=3,
                is_local=True
            ),
            LLMProvider.INTERNLM: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="internlm2:7b",
                timeout=60.0,
                priority=4,
                is_local=True
            ),
            LLMProvider.OLLAMA: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="qwen2.5:latest",
                timeout=60.0,
                priority=5,
                is_local=True
            )
        }
        
    async def initialize(self) -> None:
        """Inicializa sesión HTTP asíncrona"""
        connector = aiohttp.TCPConnector(
            limit=100,
            ttl_dns_cache=300,
            use_dns_cache=True
        )
        
        self._session = aiohttp.ClientSession(
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=60)
        )
        
        await self._check_all_providers_health()
        
        logger.info("HybridLLMRouter initialized with Chinese open-source models")
        
    async def _check_all_providers_health(self) -> None:
        """Verifica salud de todos los proveedores"""
        await self._check_provider_health(LLMProvider.OLLAMA)
        
    async def _check_provider_health(self, provider: LLMProvider) -> bool:
        """Verifica salud de Ollama local"""
        try:
            async with self._session.get(
                "http://localhost:11434/api/tags",
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                is_healthy = response.status == 200
                for p in LLMProvider:
                    self._health_status[p] = is_healthy
                return is_healthy
        except Exception as e:
            logger.warning(f"Ollama health check failed: {e}")
            for p in LLMProvider:
                self._health_status[p] = False
            return False
        
    def select_provider(
        self, 
        prompt_length: int, 
        context: Optional[str] = None,
        streaming: bool = False,
        priority_quality: bool = False,
        code_task: bool = False
    ) -> RoutingDecision:
        """Selecciona proveedor óptimo basado en múltiples factores"""
        candidates = []
        
        for provider, config in self._configs.items():
            if not self._health_status.get(provider, False):
                continue
                
            score = 0.0
            reasons = []
            
            # Prioridad base (menor número = mayor prioridad)
            score += (6 - config.priority) * 5
            
            # Qwen máxima prioridad por defecto
            if provider == LLMProvider.QWEN:
                score += 20
                reasons.append("Qwen default")
                
            # DeepSeek ESPECÍFICO para código (override)
            if code_task and provider == LLMProvider.DEEPSEEK:
                score += 100  # Máxima prioridad para código
                reasons.append("Code specialist (DeepSeek)")
                
            # Yi ESPECÍFICO para contexto largo (override)
            if prompt_length > 10000 and provider == LLMProvider.YI:
                score += 80  # Alta prioridad para contexto largo
                reasons.append("Long context (Yi-34B)")
                
            # Streaming
            if streaming:
                score += 10
                reasons.append("Streaming")
                
            # Calidad
            if priority_quality:
                if provider == LLMProvider.YI:
                    score += 30
                    reasons.append("High quality (Yi-34B)")
                elif provider == LLMProvider.QWEN:
                    score += 20
                    reasons.append("High quality (Qwen)")
                    
            # Latencia estimada
            latency_est = 0.8
            if provider == LLMProvider.CHATGLM:
                latency_est = 0.6
            elif provider == LLMProvider.QWEN:
                latency_est = 0.7
                
            cost_est = 0.0  # Todos gratuitos
            
            candidates.append((
                provider, config, score, latency_est, cost_est,
                "; ".join(reasons) if reasons else "Default"
            ))
            
        if not candidates:
            config = self._configs[LLMProvider.OLLAMA]
            return RoutingDecision(
                provider=LLMProvider.OLLAMA,
                model=config.model,
                confidence=0.5,
                latency_estimate=1.0,
                cost_estimate=0.0,
                reason="Fallback - Ollama local"
            )
            
        best = max(candidates, key=lambda x: x[2])
        
        return RoutingDecision(
            provider=best[0],
            model=best[1].model,
            confidence=min(1.0, best[2] / 100),
            latency_estimate=best[3],
            cost_estimate=best[4],
            reason=best[5]
        )
        
    async def route_request(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        streaming: bool = False,
        code_task: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Enruta solicitud al proveedor óptimo"""
        start_time = time.time()
        self._stats['requests'] += 1
        
        decision = self.select_provider(
            prompt_length=len(prompt),
            context=kwargs.get('context'),
            streaming=streaming,
            priority_quality=kwargs.get('priority_quality', False),
            code_task=code_task
        )
        
        logger.info(f"Routing to {decision.provider.value}: {decision.reason}")
        
        try:
            result = await self._request_ollama(
                prompt, system_prompt, streaming, decision.model
            )
            
            elapsed = time.time() - start_time
            self._stats['success'] += 1
            self._stats['avg_latency'] = (
                self._stats['avg_latency'] * 0.9 + elapsed * 0.1
            )
            
            result['routing'] = {
                'provider': decision.provider.value,
                'model': decision.model,
                'latency': elapsed,
                'reason': decision.reason
            }
            
            return result
            
        except Exception as e:
            self._stats['failures'] += 1
            logger.error(f"Request failed: {e}")
            
            if self._stats['failures'] < 3:
                logger.info("Attempting fallback...")
                return await self._fallback_request(prompt, system_prompt)
                
            raise
            
    async def _request_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        streaming: bool,
        model: str
    ) -> Dict[str, Any]:
        """Request a Ollama con modelo específico"""
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt or "Eres GenesyX, sistema operativo de conciencia personal.",
            "stream": streaming
        }
        
        async with self._session.post(
            "http://localhost:11434/api/generate",
            json=payload,
            timeout=aiohttp.ClientTimeout(total=60)
        ) as response:
            response.raise_for_status()
            
            if streaming:
                return {"stream": True, "response": response.content}
            else:
                data = await response.json()
                return {
                    "text": data.get("response", ""),
                    "raw": data
                }
                
    async def _fallback_request(
        self,
        prompt: str,
        system_prompt: Optional[str]
    ) -> Dict[str, Any]:
        """Request de fallback"""
        logger.warning("Using fallback to default model")
        return await self._request_ollama(
            prompt, system_prompt, False, "qwen2.5:latest"
        )
        
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del router"""
        return {
            **self._stats,
            'providers_health': self._health_status,
            'cache_size': len(self._cache)
        }
        
    async def close(self) -> None:
        """Cierra sesión HTTP"""
        if self._session:
            await self._session.close()
            self._session = None
        logger.info("HybridLLMRouter closed")
