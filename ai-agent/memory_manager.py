"""
Cognee Memory Manager for Promptly AI DevOps Assistant
Uses Cognee v1.x API: cognee.add() / cognee.cognify() / cognee.search()
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    import cognee
    from cognee.modules.search.types import SearchType
    COGNEE_AVAILABLE = True
except ImportError:
    COGNEE_AVAILABLE = False

logger = logging.getLogger(__name__)


def _configure_cognee(llm_api_key: str, llm_provider: str, vector_db_provider: str, graph_db_provider: str):
    """
    Apply runtime config to Cognee using its proper setter API.
    Must be called before any cognee.add/cognify/search call.
    """
    if not COGNEE_AVAILABLE:
        return
    try:
        cognee.config.set_llm_api_key(llm_api_key)
        cognee.config.set_llm_provider(llm_provider)
        cognee.config.set_vector_db_provider(vector_db_provider)
        cognee.config.set_graph_database_provider(graph_db_provider)
        logger.info(
            f"✅ Cognee configured: llm={llm_provider}, "
            f"vector={vector_db_provider}, graph={graph_db_provider}"
        )
    except Exception as e:
        logger.warning(f"⚠️  Cognee config apply failed: {e}")


class CogneeMemoryManager:
    """
    Manages agent memory using Cognee v1.x knowledge graph platform.
    - cognee.add()     → ingest text data
    - cognee.cognify() → process into knowledge graph
    - cognee.search()  → semantic search across stored memory
    Session memory is keyed by dataset_name for per-user isolation.
    """

    def __init__(self, enabled: bool = True, dataset_name: str = "promptly_agent"):
        self.enabled = enabled and COGNEE_AVAILABLE
        self.dataset_name = dataset_name
        self._init_error: Optional[str] = None
        # Local fallback cache when Cognee is unavailable
        self.session_cache: Dict[str, List[Dict]] = {}

        if not COGNEE_AVAILABLE:
            logger.warning("⚠️  Cognee package not found. Falling back to local session cache.")
            self.enabled = False
        else:
            logger.info(f"✅ Cognee v1.x Memory Manager ready (dataset: {dataset_name})")

    async def initialize(self) -> bool:
        """
        Configure and verify Cognee is reachable.
        """
        if not self.enabled:
            return False

        try:
            import os
            # Defensive: ensure Cognee's state directories exist no matter
            # what SYSTEM_ROOT_DIRECTORY / DATA_ROOT_DIRECTORY resolve to.
            # sqlite creates the .db file but never the parent directory,
            # which was the original cause of "unable to open database file".
            for env_key, default in [
                ("SYSTEM_ROOT_DIRECTORY", "/app/cognee_data/system"),
                ("DATA_ROOT_DIRECTORY", "/app/cognee_data/data"),
            ]:
                path = os.environ.get(env_key, default)
                os.makedirs(path, exist_ok=True)

            from config import Config
            _configure_cognee(
                llm_api_key=Config.LLM_API_KEY or Config.GROQ_API_KEY,
                llm_provider=Config.LLM_PROVIDER,
                vector_db_provider=Config.VECTOR_DB_PROVIDER,
                graph_db_provider=Config.GRAPH_DATABASE_PROVIDER,
            )
            # Lightweight connectivity check — empty graph returns [] not an error
            await cognee.search("init", SearchType.GRAPH_COMPLETION)
            logger.info("✅ Cognee connection verified")
            return True
        except Exception as e:
            import traceback
            self._init_error = traceback.format_exc()
            logger.error(f"❌ Cognee init failed — FULL ERROR: {self._init_error}")
            self.enabled = False
            return False

    # ------------------------------------------------------------------
    # remember — ingest + cognify a conversation turn
    # ------------------------------------------------------------------
    async def remember_conversation(
        self,
        query: str,
        response: str,
        agent_type: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> bool:
        sid = session_id or "default"
        dataset = f"{self.dataset_name}_{sid}"

        # Always keep a local copy for fast fallback
        if sid not in self.session_cache:
            self.session_cache[sid] = []
        self.session_cache[sid].append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response[:500],
            "agent_type": agent_type,
        })
        self.session_cache[sid] = self.session_cache[sid][-20:]

        if not self.enabled:
            return True

        try:
            memory_text = (
                f"[{agent_type.upper()} AGENT — session:{sid}]\n"
                f"User asked: {query}\n"
                f"Agent answered: {response}"
            )
            # Add text to Cognee dataset, then cognify into knowledge graph
            await cognee.add(memory_text, dataset_name=dataset)
            await cognee.cognify(datasets=[dataset])
            logger.info(f"💾 Cognee stored conversation (agent:{agent_type}, session:{sid})")
            return True

        except Exception as e:
            logger.warning(f"⚠️  Cognee remember failed: {e} — local cache kept")
            return False

    # ------------------------------------------------------------------
    # recall — search knowledge graph for relevant context
    # ------------------------------------------------------------------
    async def get_agent_context(
        self,
        agent_type: str,
        session_id: Optional[str] = None,
    ) -> str:
        sid = session_id or "default"

        if self.enabled:
            try:
                results = await cognee.search(
                    f"Previous {agent_type} interactions and decisions",
                    SearchType.GRAPH_COMPLETION
                )
                if results:
                    parts = []
                    for r in results[:3]:
                        if isinstance(r, str):
                            parts.append(r[:300])
                        elif isinstance(r, dict):
                            text = r.get("text") or r.get("content") or str(r)
                            parts.append(text[:300])
                    context = "\n".join(parts)
                    logger.info(f"🔍 Cognee recalled {len(results)} memories for {agent_type}")
                    return context
            except Exception as e:
                logger.warning(f"⚠️  Cognee search failed: {e} — using local cache")

        # Fallback: last 3 turns from local cache
        if sid in self.session_cache:
            recent = self.session_cache[sid][-3:]
            parts = [
                f"Previous {t['agent_type']} response: {t['response'][:200]}"
                for t in recent
            ]
            return "\n".join(parts)

        return ""

    # ------------------------------------------------------------------
    # forget — prune the knowledge graph
    # ------------------------------------------------------------------
    async def forget_memory(
        self,
        session_id: Optional[str] = None,
        all_data: bool = False,
    ) -> bool:
        if all_data:
            self.session_cache.clear()
        elif session_id and session_id in self.session_cache:
            del self.session_cache[session_id]

        if not self.enabled:
            return True

        try:
            await cognee.prune()
            logger.info("🗑️  Cognee memory pruned")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Cognee prune failed: {e}")
            return False

    # ------------------------------------------------------------------
    # stats
    # ------------------------------------------------------------------
    async def get_memory_stats(self) -> Dict[str, Any]:
        cognee_ok = False
        if self.enabled:
            try:
                await cognee.search("stats", SearchType.GRAPH_COMPLETION)
                cognee_ok = True
            except Exception:
                cognee_ok = False

        return {
            "enabled": self.enabled,
            "dataset": self.dataset_name,
            "cognee_connected": cognee_ok,
            "local_sessions": len(self.session_cache),
            "local_entries": sum(len(v) for v in self.session_cache.values()),
            "init_error": self._init_error,
        }


# ------------------------------------------------------------------
# Module-level singleton
# ------------------------------------------------------------------
_memory_manager: Optional[CogneeMemoryManager] = None


async def init_memory_manager(
    enabled: bool = True,
    dataset_name: str = "promptly_agent",
) -> CogneeMemoryManager:
    global _memory_manager
    _memory_manager = CogneeMemoryManager(enabled=enabled, dataset_name=dataset_name)
    await _memory_manager.initialize()
    return _memory_manager


def get_memory_manager() -> Optional[CogneeMemoryManager]:
    return _memory_manager
