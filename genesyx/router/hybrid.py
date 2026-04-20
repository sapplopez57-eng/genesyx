"""
Router Híbrido LLM (Ollama/Groq) Optimizado para Open Claw
Enrutamiento inteligente con mínimo latency
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
    """Proveedores soportados"""
    OLLAMA = "ollama"
    GROQ = "groq"
    OPENCLAW = "openclaw"


@dataclass
class ProviderConfig:
    """Configuración de proveedor"""
    endpoint: str
    model: str
    api_key: Optional[str] = None
    timeout: float = 30.0
    max_retries: int = 3
    priority: int = 1


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
    Router híbrido optimizado para Open Claw
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
        
        # Configurar proveedores por defecto
        self._initialize_default_configs()
        
    def _initialize_default_configs(self) -> None:
        """Inicializa configuraciones por defecto"""
        self._configs = {
            LLMProvider.OLLAMA: ProviderConfig(
                endpoint="http://localhost:11434/api/generate",
                model="llama3.2:latest",
                timeout=60.0,
                priority=2
            ),
            LLMProvider.GROQ: ProviderConfig(
                endpoint="https://api.groq.com/openai/v1/chat/completions",
                model="llama-3.2-90b-vision-preview",
                api_key=None,  # Configurar via env
                timeout=30.0,
                priority=1
            ),
            LLMProvider.OPENCLAW: ProviderConfig(
                endpoint="http://localhost:8080/v1/chat/completions",
                model="openclaw-model",
                timeout=45.0,
                priority=0  # Máxima prioridad para Open Claw
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
        
        # Verificar salud inicial
        await self._check_all_providers_health()
        
        logger.info("HybridLLMRouter initialized with Open Claw priority")
        
    async def _check_all_providers_health(self) -> None:
        """Verifica salud de todos los proveedores"""
        tasks = [self._check_provider_health(provider) for provider in LLMProvider]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for provider, result in zip(LLMProvider, results):
            self._health_status[provider] = isinstance(result, bool) and result
            
    async def _check_provider_health(self, provider: LLMProvider) -> bool:
        """Verifica salud de un proveedor específico"""
        if provider not in self._configs:
            return False
            
        config = self._configs[provider]
        
        try:
            if provider == LLMProvider.OLLAMA:
                async with self._session.get(
                    "http://localhost:11434/api/tags",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
                    
            elif provider == LLMProvider.GROQ:
                if not config.api_key:
                    return False
                async with self._session.get(
                    f"{config.endpoint.split('/chat')[0]}/models",
                    headers={"Authorization": f"Bearer {config.api_key}"},
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
                    
            elif provider == LLMProvider.OPENCLAW:
                async with self._session.get(
                    f"{config.endpoint.split('/chat')[0]}/health",
                    timeout=aiohttp.ClientTimeout(total=5)
                ) as response:
                    return response.status == 200
                    
        except Exception as e:
            logger.warning(f"Health check failed for {provider.value}: {e}")
            return False
            
        return False
        
    def select_provider(
        self, 
        prompt_length: int, 
        context: Optional[str] = None,
        streaming: bool = False,
        priority_quality: bool = False
    ) -> RoutingDecision:
        """
        Selecciona proveedor óptimo basado en múltiples factores
        Optimizado para decisión rápida
        """
        candidates = []
        
        for provider, config in self._configs.items():
            # Verificar salud
            if not self._health_status.get(provider, False):
                continue
                
            # Calcular score
            score = 0.0
            reasons = []
            
            # Prioridad base
            score += (3 - config.priority) * 10
            
            # Open Claw tiene máxima prioridad
            if provider == LLMProvider.OPENCLAW:
                score += 50
                reasons.append("Open Claw integration")
                
            # Longitud del prompt
            if prompt_length > 10000:
                if provider == LLMProvider.GROQ:
                    score += 20
                    reasons.append("Long context handling")
                    
            # Streaming preference
            if streaming:
                if provider == LLMProvider.OLLAMA:
                    score += 15
                    reasons.append("Streaming optimized")
                    
            # Quality priority
            if priority_quality:
                if provider == LLMProvider.GROQ:
                    score += 25
                    reasons.append("High quality mode")
                    
            # Estimación de latencia
            latency_est = config.timeout * 0.5
            if provider == LLMProvider.OPENCLAW:
                latency_est = 0.3  # Local, baja latencia
            elif provider == LLMProvider.OLLAMA:
                latency_est = 1.0  # Local, media latencia
                
            # Estimación de costo
            cost_est = 0.0
            if provider == LLMProvider.GROQ:
                cost_est = prompt_length * 0.00001  # Aproximado
                
            candidates.append((
                provider,
                config,
                score,
                latency_est,
                cost_est,
                "; ".join(reasons) if reasons else "Default selection"
            ))
            
        if not candidates:
            # Fallback a Ollama local
            config = self._configs[LLMProvider.OLLAMA]
            return RoutingDecision(
                provider=LLMProvider.OLLAMA,
                model=config.model,
                confidence=0.5,
                latency_estimate=1.0,
                cost_estimate=0.0,
                reason="Fallback - no providers available"
            )
            
        # Seleccionar mejor candidato
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
        **kwargs
    ) -> Dict[str, Any]:
        """
        Enruta solicitud al proveedor óptimo
        """
        start_time = time.time()
        self._stats['requests'] += 1
        
        # Seleccionar proveedor
        decision = self.select_provider(
            prompt_length=len(prompt),
            context=kwargs.get('context'),
            streaming=streaming,
            priority_quality=kwargs.get('priority_quality', False)
        )
        
        logger.info(f"Routing to {decision.provider.value}: {decision.reason}")
        
        try:
            # Ejecutar request
            if decision.provider == LLMProvider.OPENCLAW:
                result = await self._request_openclaw(
                    prompt, system_prompt, streaming, **kwargs
                )
            elif decision.provider == LLMProvider.GROQ:
                result = await self._request_groq(
                    prompt, system_prompt, streaming, **kwargs
                )
            else:  # OLLAMA
                result = await self._request_ollama(
                    prompt, system_prompt, streaming, **kwargs
                )
                
            # Actualizar stats
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
            
            # Reintentar con fallback
            if self._stats['failures'] < 3:
                logger.info("Attempting fallback...")
                return await self._fallback_request(prompt, system_prompt, **kwargs)
                
            raise
            
    async def _request_openclaw(
        self,
        prompt: str,
        system_prompt: Optional[str],
        streaming: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """Request a Open Claw optimizado"""
        config = self._configs[LLMProvider.OPENCLAW]
        
        payload = {
            "model": config.model,
            "messages": [
                {"role": "system", "content": system_prompt or "Eres GenesyX, sistema operativo de conciencia personal."},
                {"role": "user", "content": prompt}
            ],
            "stream": streaming
        }
        
        async with self._session.post(
            config.endpoint,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=config.timeout)
        ) as response:
            response.raise_for_status()
            
            if streaming:
                return {"stream": True, "response": response.content}
            else:
                data = await response.json()
                return {
                    "text": data.get("choices", [{}])[0].get("message", {}).get("content", ""),
                    "raw": data
                }
                
    async def _request_groq(
        self,
        prompt: str,
        system_prompt: Optional[str],
        streaming: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """Request a Groq"""
        config = self._configs[LLMProvider.GROQ]
        
        headers = {
            "Authorization": f"Bearer {config.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": config.model,
            "messages": [
                {"role": "system", "content": system_prompt or "Eres GenesyX."},
                {"role": "user", "content": prompt}
            ]
        }
        
        async with self._session.post(
            config.endpoint,
            json=payload,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=config.timeout)
        ) as response:
            response.raise_for_status()
            data = await response.json()
            
            return {
                "text": data.get("choices", [{}])[0].get("message", {}).get("content", ""),
                "raw": data
            }
            
    async def _request_ollama(
        self,
        prompt: str,
        system_prompt: Optional[str],
        streaming: bool,
        **kwargs
    ) -> Dict[str, Any]:
        """Request a Ollama local"""
        config = self._configs[LLMProvider.OLLAMA]
        
        payload = {
            "model": config.model,
            "prompt": prompt,
            "system": system_prompt or "Eres GenesyX.",
            "stream": streaming
        }
        
        async with self._session.post(
            config.endpoint,
            json=payload,
            timeout=aiohttp.ClientTimeout(total=config.timeout)
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
        system_prompt: Optional[str],
        **kwargs
    ) -> Dict[str, Any]:
        """Request de fallback a Ollama"""
        logger.warning("Using fallback to Ollama")
        return await self._request_ollama(prompt, system_prompt, False, **kwargs)
        
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
