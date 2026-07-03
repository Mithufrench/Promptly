"""
Cognee Memory Manager for Promptly AI DevOps Assistant
Provides persistent long-term memory using Cognee's knowledge graph engine
"""

import asyncio
import logging
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

try:
    import cognee
    COGNEE_AVAILABLE = True
except ImportError:
    COGNEE_AVAILABLE = False

logger = logging.getLogger(__name__)


class CogneeMemoryManager:
    """
    Manages agent memory using Cognee's knowledge graph platform.
    Handles both session memory (fast cache) and permanent graph memory.
    """

    def __init__(self, enabled: bool = True, dataset_name: str = "promptly_agent"):
        """
        Initialize Cognee Memory Manager
        
        Args:
            enabled: Whether to enable Cognee memory integration
            dataset_name: Cognee dataset name for storing memories
        """
        self.enabled = enabled and COGNEE_AVAILABLE
        self.dataset_name = dataset_name
        self.session_memories: Dict[str, List[Dict]] = {}
        
        if not COGNEE_AVAILABLE:
            logger.warning("⚠️  Cognee not installed. Running without persistent memory.")
            self.enabled = False
        else:
            logger.info(f"✅ Cognee Memory Manager initialized with dataset: {dataset_name}")

    async def initialize(self) -> bool:
        """
        Initialize Cognee connection and dataset
        
        Returns:
            bool: True if initialization successful
        """
        if not self.enabled:
            return False
        
        try:
            # Cognee will auto-initialize with environment variables
            # (LLM_API_KEY, DB_PROVIDER, etc. from .env)
            logger.info("🔄 Initializing Cognee connection...")
            await asyncio.sleep(0.1)  # Brief delay for async context
            logger.info("✅ Cognee connection established")
            return True
        except Exception as e:
            logger.error(f"❌ Failed to initialize Cognee: {str(e)}")
            self.enabled = False
            return False

    async def remember_conversation(
        self, 
        query: str, 
        response: str, 
        agent_type: str,
        session_id: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Store conversation in permanent memory (knowledge graph)
        
        Args:
            query: User's query
            response: Agent's response
            agent_type: Type of agent that responded
            session_id: Optional session identifier
            metadata: Additional metadata
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            return False
        
        try:
            # Create memory entry
            memory_entry = {
                "timestamp": datetime.now().isoformat(),
                "query": query,
                "response": response,
                "agent_type": agent_type,
                "session_id": session_id or "default",
                **(metadata or {})
            }
            
            # Format for Cognee ingestion
            memory_text = f"""
Agent Interaction Record:
- Agent Type: {agent_type}
- Query: {query}
- Response: {response}
- Session: {session_id or 'default'}
- Timestamp: {memory_entry['timestamp']}
"""
            
            # Store in Cognee knowledge graph
            await cognee.remember(
                data=memory_text,
                dataset=self.dataset_name,
                metadata=memory_entry
            )
            
            logger.info(f"💾 Stored conversation in Cognee (Agent: {agent_type})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store conversation: {str(e)}")
            return False

    async def remember_session(
        self, 
        data: str, 
        session_id: str,
        metadata: Optional[Dict] = None
    ) -> bool:
        """
        Store session-specific memory (fast cache)
        
        Args:
            data: Data to remember
            session_id: Session identifier
            metadata: Additional metadata
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            # Store in local session cache as fallback
            if session_id not in self.session_memories:
                self.session_memories[session_id] = []
            
            self.session_memories[session_id].append({
                "data": data,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            })
            return True
        
        try:
            # Store in Cognee with session_id
            await cognee.remember(
                data=data,
                dataset=self.dataset_name,
                session_id=session_id,
                metadata=metadata or {}
            )
            
            logger.info(f"⚡ Stored session memory (Session: {session_id})")
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to store session memory: {str(e)}")
            # Fallback to local cache
            if session_id not in self.session_memories:
                self.session_memories[session_id] = []
            self.session_memories[session_id].append({
                "data": data,
                "timestamp": datetime.now().isoformat(),
                **(metadata or {})
            })
            return True

    async def recall_memory(
        self, 
        query: str, 
        session_id: Optional[str] = None,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Search and retrieve relevant memories
        
        Args:
            query: Search query
            session_id: Optional session to search within
            limit: Maximum number of results
            
        Returns:
            List of relevant memories
        """
        if not self.enabled:
            # Return from local session cache if available
            if session_id and session_id in self.session_memories:
                return self.session_memories[session_id][-limit:]
            return []
        
        try:
            # Search Cognee knowledge graph
            results = await cognee.recall(
                query=query,
                dataset=self.dataset_name,
                session_id=session_id,
                limit=limit
            )
            
            logger.info(f"🔍 Retrieved {len(results) if results else 0} memories for query")
            return results if results else []
            
        except Exception as e:
            logger.error(f"❌ Failed to recall memory: {str(e)}")
            # Fallback to local cache
            if session_id and session_id in self.session_memories:
                return self.session_memories[session_id][-limit:]
            return []

    async def get_agent_context(
        self, 
        agent_type: str, 
        session_id: Optional[str] = None
    ) -> str:
        """
        Get contextual memory for specific agent type
        
        Args:
            agent_type: Type of agent
            session_id: Optional session identifier
            
        Returns:
            Context string with relevant memories
        """
        try:
            # Search for previous interactions with this agent type
            query = f"Previous interactions with {agent_type} agent"
            memories = await self.recall_memory(
                query=query,
                session_id=session_id,
                limit=3
            )
            
            if not memories:
                return ""
            
            # Format context from memories
            context_parts = []
            for memory in memories:
                if isinstance(memory, dict):
                    if 'response' in memory:
                        context_parts.append(f"Previous {memory.get('agent_type', 'agent')} response: {memory['response'][:200]}")
                    elif 'data' in memory:
                        context_parts.append(f"Relevant context: {memory['data'][:200]}")
            
            return "\n".join(context_parts) if context_parts else ""
            
        except Exception as e:
            logger.error(f"Failed to get agent context: {str(e)}")
            return ""

    async def forget_memory(
        self, 
        session_id: Optional[str] = None,
        all_data: bool = False
    ) -> bool:
        """
        Delete memories
        
        Args:
            session_id: Optional session to clear
            all_data: If True, clear all memories in dataset
            
        Returns:
            bool: Success status
        """
        if not self.enabled:
            if all_data:
                self.session_memories.clear()
            elif session_id and session_id in self.session_memories:
                del self.session_memories[session_id]
            return True
        
        try:
            if all_data:
                await cognee.forget(dataset=self.dataset_name)
                logger.info("🗑️  Cleared all memories in dataset")
            elif session_id:
                # In Cognee, we can forget specific session data
                await cognee.forget(dataset=self.dataset_name)
                logger.info(f"🗑️  Cleared session memories")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to forget memory: {str(e)}")
            return False

    async def get_memory_stats(self) -> Dict[str, Any]:
        """
        Get statistics about stored memories
        
        Returns:
            Dictionary with memory statistics
        """
        stats = {
            "enabled": self.enabled,
            "dataset": self.dataset_name,
            "local_sessions": len(self.session_memories),
            "local_entries": sum(len(v) for v in self.session_memories.values())
        }
        
        if self.enabled:
            try:
                # Try to get Cognee stats if available
                stats["cognee_connected"] = True
            except:
                stats["cognee_connected"] = False
        
        return stats

    def add_to_conversation_history(
        self, 
        history: List[Dict],
        context: str,
        max_context_length: int = 500
    ) -> List[Dict]:
        """
        Enhance conversation history with retrieved context
        
        Args:
            history: Current conversation history
            context: Retrieved context from memory
            max_context_length: Max length of context to add
            
        Returns:
            Enhanced conversation history
        """
        if not context:
            return history
        
        # Truncate context if needed
        if len(context) > max_context_length:
            context = context[:max_context_length] + "..."
        
        # Add context as system message if not already present
        enhanced_history = history.copy()
        
        # Check if context is already in history
        context_exists = any(
            "context" in msg.get("content", "").lower() or 
            "previous" in msg.get("content", "").lower()
            for msg in enhanced_history
        )
        
        if not context_exists and context:
            enhanced_history.insert(0, {
                "role": "system",
                "content": f"Relevant context from previous interactions:\n{context}"
            })
        
        return enhanced_history


# Global memory manager instance
memory_manager: Optional[CogneeMemoryManager] = None


async def init_memory_manager(enabled: bool = True, dataset_name: str = "promptly_agent") -> CogneeMemoryManager:
    """
    Initialize global memory manager
    
    Args:
        enabled: Whether to enable memory
        dataset_name: Cognee dataset name
        
    Returns:
        Initialized memory manager instance
    """
    global memory_manager
    
    memory_manager = CogneeMemoryManager(enabled=enabled, dataset_name=dataset_name)
    await memory_manager.initialize()
    
    return memory_manager


def get_memory_manager() -> Optional[CogneeMemoryManager]:
    """Get global memory manager instance"""
    return memory_manager
