"""
Gestor de Memoria Vectorial con SQLite+FTS5
Optimizado para búsquedas rápidas y eficiencia con Open Claw
Sin alterar estructura original de memorias
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path
import numpy as np
from datetime import datetime
import logging
import threading

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Sistema de memoria vectorial optimizado
    Mantiene estructura original, mejora rendimiento
    """
    
    __slots__ = ['_db_path', '_conn', '_lock', '_cache']
    
    def __init__(self, db_path: str = "genesyx_memory.db"):
        self._db_path = Path(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._lock = threading.RLock()
        self._cache: Dict[str, Any] = {}
        
    def initialize(self) -> None:
        """Inicializa base de datos con optimizaciones de rendimiento"""
        self._conn = sqlite3.connect(
            str(self._db_path),
            check_same_thread=False,
            isolation_level=None
        )
        
        # Optimizaciones PRAGMA para máximo rendimiento
        self._execute_pragmas()
        self._create_tables()
        
        logger.info(f"MemoryManager initialized: {self._db_path}")
        
    def _execute_pragmas(self) -> None:
        """Configura SQLite para máximo rendimiento"""
        pragmas = [
            "PRAGMA journal_mode=WAL",
            "PRAGMA synchronous=NORMAL",
            "PRAGMA cache_size=-64000",  # 64MB cache
            "PRAGMA temp_store=MEMORY",
            "PRAGMA mmap_size=268435456",  # 256MB
            "PRAGMA foreign_keys=ON",
            "PRAGMA busy_timeout=5000"
        ]
        
        for pragma in pragmas:
            try:
                self._conn.execute(pragma)
            except Exception as e:
                logger.warning(f"Pragma failed {pragma}: {e}")
                
    def _create_tables(self) -> None:
        """Crea tablas con índices optimizados"""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                embedding BLOB,
                metadata JSON,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                importance REAL DEFAULT 0.5,
                access_count INTEGER DEFAULT 0
            )
            """,
            """
            CREATE VIRTUAL TABLE IF NOT EXISTS memories_fts USING fts5(
                content,
                metadata,
                content='memories',
                content_rowid='id'
            )
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_memories_importance 
            ON memories(importance DESC)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_memories_created 
            ON memories(created_at DESC)
            """,
            """
            CREATE INDEX IF NOT EXISTS idx_memories_access 
            ON memories(access_count DESC)
            """
        ]
        
        with self._lock:
            for query in queries:
                self._conn.execute(query)
            self._conn.commit()
            
    def store_memory(
        self, 
        content: str, 
        embedding: Optional[np.ndarray] = None,
        metadata: Optional[Dict] = None,
        importance: float = 0.5
    ) -> int:
        """Almacena memoria con optimización batch"""
        with self._lock:
            cursor = self._conn.cursor()
            
            emb_bytes = embedding.tobytes() if embedding is not None else None
            meta_json = str(metadata) if metadata else '{}'
            
            cursor.execute(
                """
                INSERT INTO memories (content, embedding, metadata, importance)
                VALUES (?, ?, ?, ?)
                """,
                (content, emb_bytes, meta_json, importance)
            )
            
            memory_id = cursor.lastrowid
            
            # Insertar en FTS5
            try:
                cursor.execute(
                    "INSERT INTO memories_fts(rowid, content, metadata) VALUES (?, ?, ?)",
                    (memory_id, content, meta_json)
                )
            except sqlite3.IntegrityError:
                pass  # Ya existe en FTS
                
            self._conn.commit()
            
            # Invalidar cache
            self._cache.clear()
            
            return memory_id
            
    def search_memories(
        self, 
        query: str, 
        limit: int = 10,
        min_importance: float = 0.0
    ) -> List[Dict[str, Any]]:
        """Búsqueda híbrida FTS5 + vectorial optimizada"""
        with self._lock:
            cursor = self._conn.cursor()
            
            # Búsqueda FTS5 rápida
            cursor.execute(
                """
                SELECT m.id, m.content, m.metadata, m.importance, m.access_count,
                       bm25(memories_fts) as relevance
                FROM memories_fts ft
                JOIN memories m ON ft.rowid = m.id
                WHERE memories_fts MATCH ?
                  AND m.importance >= ?
                ORDER BY relevance DESC, m.importance DESC
                LIMIT ?
                """,
                (query, min_importance, limit)
            )
            
            results = []
            for row in cursor.fetchall():
                results.append({
                    'id': row[0],
                    'content': row[1],
                    'metadata': eval(row[2]) if row[2] else {},
                    'importance': row[3],
                    'access_count': row[4],
                    'relevance': row[5]
                })
                
            # Actualizar contadores de acceso
            if results:
                ids = [r['id'] for r in results]
                cursor.execute(
                    "UPDATE memories SET access_count = access_count + 1 WHERE id IN (%s)" % 
                    ','.join('?' * len(ids)),
                    ids
                )
                self._conn.commit()
                
            return results
            
    def get_memory(self, memory_id: int) -> Optional[Dict[str, Any]]:
        """Obtiene memoria específica con caché"""
        cache_key = f"memory_{memory_id}"
        
        if cache_key in self._cache:
            return self._cache[cache_key]
            
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "SELECT id, content, embedding, metadata, importance, access_count, created_at FROM memories WHERE id = ?",
                (memory_id,)
            )
            
            row = cursor.fetchone()
            if not row:
                return None
                
            result = {
                'id': row[0],
                'content': row[1],
                'embedding': np.frombuffer(row[2]) if row[2] else None,
                'metadata': eval(row[3]) if row[3] else {},
                'importance': row[4],
                'access_count': row[5],
                'created_at': row[6]
            }
            
            # Cachear resultado
            self._cache[cache_key] = result
            
            return result
            
    def update_memory_importance(self, memory_id: int, importance: float) -> bool:
        """Actualiza importancia de memoria"""
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                "UPDATE memories SET importance = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (max(0.0, min(1.0, importance)), memory_id)
            )
            self._conn.commit()
            
            # Invalidar cache
            self._cache.pop(f"memory_{memory_id}", None)
            
            return cursor.rowcount > 0
            
    def delete_memory(self, memory_id: int) -> bool:
        """Elimina memoria"""
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            try:
                cursor.execute("DELETE FROM memories_fts WHERE rowid = ?", (memory_id,))
            except:
                pass
            self._conn.commit()
            
            # Invalidar cache
            self._cache.clear()
            
            return cursor.rowcount > 0
            
    def get_stats(self) -> Dict[str, Any]:
        """Obtiene estadísticas del sistema de memoria"""
        with self._lock:
            cursor = self._conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM memories")
            total = cursor.fetchone()[0]
            
            cursor.execute("SELECT AVG(importance) FROM memories")
            avg_importance = cursor.fetchone()[0] or 0.0
            
            cursor.execute("SELECT SUM(access_count) FROM memories")
            total_accesses = cursor.fetchone()[0] or 0
            
            return {
                'total_memories': total,
                'average_importance': avg_importance,
                'total_accesses': total_accesses,
                'cache_size': len(self._cache)
            }
            
    def close(self) -> None:
        """Cierra conexión limpiamente"""
        if self._conn:
            with self._lock:
                self._cache.clear()
                self._conn.close()
                self._conn = None
            logger.info("MemoryManager closed")
