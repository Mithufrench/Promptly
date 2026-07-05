"""
Cognee Memory Manager for Promptly AI DevOps Assistant
Uses Cognee v1.x API: cognee.remember() / cognee.recall() / cognee.forget()
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

try:
    import cognee
    COGNEE_AVAILABLE = True
except ImportError:
    COGNEE_AVAILABLE = False

logger = logging.getLogger(__name__)


class CogneeMemoryManager:
    """
    Manages agent memory using Cognee v1.x knowledge graph platform.
    - remember()  → stores data into the knowledge graph
    - recall()    → semantic search across stored memory
    - forget()    → deletes memory
    Session memory is keyed by session_id for per-user isolation.
    """

    def __init__(self, enabled: bool = True, dataset_name: str = "promptly_agent"):
        self.enabled = enabled and COGNEE_AVAILABLE
        self.dataset_name = dataset_name
        # Local fallback cache when Cognee is unavailable
        self.session_cache: Dict[str, List[Dict]] = {}

        if not COGNEE_AVAILABLE:
            logger.warning("⚠️  Cognee package not found. Falling back to local session cache.")
            self.enabled = False
        else:
            logger.info(f"✅ Cognee v1.x Memory Manager ready (dataset: {dataset_name})")

    async def initialize(self) -> bool:
        """
        Verify Cognee is reachable.
        Cognee v1.x auto-configures from environment variables
        (LLM_API_KEY, DB_PROVIDER, etc.) — no explicit init call needed.
        """
        if not self.enabled:
            return False

        try:
            # Perform a lightweight recall to confirm the connection works
            await cognee.recall("init check")
            logger.info("✅ Cognee connection verified")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Cognee init check failed: {e} — falling back to local cache")
            self.enabled = False
            return False

    # ------------------------------------------------------------------
    # remember — store a conversation turn in the knowledge graph
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

        # Always keep a local copy for fast fallback
        if sid not in self.session_cache:
            self.session_cache[sid] = []
        self.session_cache[sid].append({
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "response": response[:500],   # cap length
            "agent_type": agent_type,
        })
        # Keep only the last 20 turns per session
        self.session_cache[sid] = self.session_cache[sid][-20:]

        if not self.enabled:
            return True     # local cache is enough

        try:
            memory_text = (
                f"[{agent_type.upper()} AGENT — session:{sid}]\n"
                f"User asked: {query}\n"
                f"Agent answered: {response}"
            )
            # Cognee v1.x: remember(data, session_id=...) stores into graph + session cache
            await cognee.remember(memory_text, session_id=sid)
            logger.info(f"💾 Cognee stored conversation (agent:{agent_type}, session:{sid})")
            return True

        except Exception as e:
            logger.warning(f"⚠️  Cognee remember failed: {e} — local cache kept")
            return False

    # ------------------------------------------------------------------
    # recall — retrieve relevant context for a query
    # ------------------------------------------------------------------
    async def get_agent_context(
        self,
        agent_type: str,
        session_id: Optional[str] = None,
    ) -> str:
        sid = session_id or "default"

        if self.enabled:
            try:
                # Cognee v1.x: recall(query, session_id=...) auto-routes search strategy
                results = await cognee.recall(
                    f"Previous {agent_type} interactions and decisions",
                    session_id=sid,
                )
                if results:
                    # results is a list of strings or dicts depending on Cognee version
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
                logger.warning(f"⚠️  Cognee recall failed: {e} — using local cache")

        # Fallback: return last 3 turns from local cache
        if sid in self.session_cache:
            recent = self.session_cache[sid][-3:]
            parts = [
                f"Previous {t['agent_type']} response: {t['response'][:200]}"
                for t in recent
            ]
            return "\n".join(parts)

        return ""

    # ------------------------------------------------------------------
    # forget — delete memories
    # ------------------------------------------------------------------
    async def forget_memory(
        self,
        session_id: Optional[str] = None,
        all_data: bool = False,
    ) -> bool:
        # Clear local cache
        if all_data:
            self.session_cache.clear()
        elif session_id and session_id in self.session_cache:
            del self.session_cache[session_id]

        if not self.enabled:
            return True

        try:
            # Cognee v1.x forget API
            await cognee.forget(dataset=self.dataset_name)
            logger.info("🗑️  Cognee memory cleared")
            return True
        except Exception as e:
            logger.warning(f"⚠️  Cognee forget failed: {e}")
            return False

    # ------------------------------------------------------------------
    # stats
    # ------------------------------------------------------------------
    async def get_memory_stats(self) -> Dict[str, Any]:
        cognee_ok = False
        if self.enabled:
            try:
                await cognee.recall("stats check")
                cognee_ok = True
            except Exception:
                cognee_ok = False

        return {
            "enabled": self.enabled,
            "dataset": self.dataset_name,
            "cognee_connected": cognee_ok,
            "local_sessions": len(self.session_cache),
            "local_entries": sum(len(v) for v in self.session_cache.values()),
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
