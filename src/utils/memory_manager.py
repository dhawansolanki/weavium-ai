"""
Memory manager for the Autogen Agents Framework.
"""

import json
import os
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import sqlite3

class MemoryManager:
    """
    Memory manager for storing and retrieving agent conversation history and knowledge.
    This class provides persistent storage for agent memories and conversation history.
    """
    
    def __init__(self, db_path: str = "agent_memory.db"):
        """
        Initialize a memory manager.
        
        Args:
            db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self._initialize_db()
    
    def _initialize_db(self):
        """Initialize the SQLite database with required tables."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create conversations table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT UNIQUE,
            title TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        ''')
        
        # Create messages table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id TEXT,
            sender TEXT,
            receiver TEXT,
            content TEXT,
            timestamp TIMESTAMP,
            FOREIGN KEY (conversation_id) REFERENCES conversations (conversation_id)
        )
        ''')
        
        # Create memories table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            agent_name TEXT,
            memory_type TEXT,
            content TEXT,
            created_at TIMESTAMP,
            updated_at TIMESTAMP
        )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_conversation(self, conversation_id: str, title: str) -> bool:
        """
        Create a new conversation.
        
        Args:
            conversation_id: Unique identifier for the conversation
            title: Title of the conversation
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO conversations (conversation_id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (conversation_id, title, now, now)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error creating conversation: {e}")
            return False
    
    def add_message(self, conversation_id: str, sender: str, receiver: str, content: str) -> bool:
        """
        Add a message to a conversation.
        
        Args:
            conversation_id: Conversation identifier
            sender: Name of the sender agent
            receiver: Name of the receiver agent
            content: Message content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if conversation exists
            cursor.execute("SELECT conversation_id FROM conversations WHERE conversation_id = ?", (conversation_id,))
            if cursor.fetchone() is None:
                # Create conversation if it doesn't exist
                self.create_conversation(conversation_id, f"Conversation {conversation_id}")
            
            # Add message
            now = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO messages (conversation_id, sender, receiver, content, timestamp) VALUES (?, ?, ?, ?, ?)",
                (conversation_id, sender, receiver, content, now)
            )
            
            # Update conversation timestamp
            cursor.execute(
                "UPDATE conversations SET updated_at = ? WHERE conversation_id = ?",
                (now, conversation_id)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error adding message: {e}")
            return False
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict[str, Any]]:
        """
        Get the history of a conversation.
        
        Args:
            conversation_id: Conversation identifier
            
        Returns:
            List of messages in the conversation
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT sender, receiver, content, timestamp FROM messages WHERE conversation_id = ? ORDER BY timestamp",
                (conversation_id,)
            )
            
            messages = []
            for row in cursor.fetchall():
                messages.append({
                    "sender": row[0],
                    "receiver": row[1],
                    "content": row[2],
                    "timestamp": row[3]
                })
            
            conn.close()
            return messages
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def get_recent_conversations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent conversations.
        
        Args:
            limit: Maximum number of conversations to return
            
        Returns:
            List of recent conversations
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT conversation_id, title, created_at, updated_at FROM conversations ORDER BY updated_at DESC LIMIT ?",
                (limit,)
            )
            
            conversations = []
            for row in cursor.fetchall():
                conversations.append({
                    "conversation_id": row[0],
                    "title": row[1],
                    "created_at": row[2],
                    "updated_at": row[3]
                })
            
            conn.close()
            return conversations
        except Exception as e:
            print(f"Error getting recent conversations: {e}")
            return []
    
    def store_memory(self, agent_name: str, memory_type: str, content: Union[str, Dict[str, Any]]) -> bool:
        """
        Store a memory for an agent.
        
        Args:
            agent_name: Name of the agent
            memory_type: Type of memory (e.g., "fact", "skill", "experience")
            content: Memory content (string or JSON-serializable object)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert content to JSON string if it's a dictionary
            if isinstance(content, dict):
                content = json.dumps(content)
            
            now = datetime.now().isoformat()
            cursor.execute(
                "INSERT INTO memories (agent_name, memory_type, content, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
                (agent_name, memory_type, content, now, now)
            )
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Error storing memory: {e}")
            return False
    
    def retrieve_memories(self, agent_name: str, memory_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Retrieve memories for an agent.
        
        Args:
            agent_name: Name of the agent
            memory_type: Type of memory to retrieve (None for all types)
            
        Returns:
            List of memories
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if memory_type:
                cursor.execute(
                    "SELECT id, memory_type, content, created_at, updated_at FROM memories WHERE agent_name = ? AND memory_type = ?",
                    (agent_name, memory_type)
                )
            else:
                cursor.execute(
                    "SELECT id, memory_type, content, created_at, updated_at FROM memories WHERE agent_name = ?",
                    (agent_name,)
                )
            
            memories = []
            for row in cursor.fetchall():
                content = row[2]
                try:
                    # Try to parse content as JSON
                    content = json.loads(content)
                except:
                    # If not JSON, keep as string
                    pass
                
                memories.append({
                    "id": row[0],
                    "memory_type": row[1],
                    "content": content,
                    "created_at": row[3],
                    "updated_at": row[4]
                })
            
            conn.close()
            return memories
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
    
    def update_memory(self, memory_id: int, content: Union[str, Dict[str, Any]]) -> bool:
        """
        Update an existing memory.
        
        Args:
            memory_id: ID of the memory to update
            content: New memory content
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Convert content to JSON string if it's a dictionary
            if isinstance(content, dict):
                content = json.dumps(content)
            
            now = datetime.now().isoformat()
            cursor.execute(
                "UPDATE memories SET content = ?, updated_at = ? WHERE id = ?",
                (content, now, memory_id)
            )
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error updating memory: {e}")
            return False
    
    def delete_memory(self, memory_id: int) -> bool:
        """
        Delete a memory.
        
        Args:
            memory_id: ID of the memory to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
            
            conn.commit()
            conn.close()
            return cursor.rowcount > 0
        except Exception as e:
            print(f"Error deleting memory: {e}")
            return False
    
    def search_memories(self, query: str) -> List[Dict[str, Any]]:
        """
        Search memories by content.
        
        Args:
            query: Search query
            
        Returns:
            List of matching memories
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute(
                "SELECT id, agent_name, memory_type, content, created_at, updated_at FROM memories WHERE content LIKE ?",
                (f"%{query}%",)
            )
            
            memories = []
            for row in cursor.fetchall():
                content = row[3]
                try:
                    # Try to parse content as JSON
                    content = json.loads(content)
                except:
                    # If not JSON, keep as string
                    pass
                
                memories.append({
                    "id": row[0],
                    "agent_name": row[1],
                    "memory_type": row[2],
                    "content": content,
                    "created_at": row[4],
                    "updated_at": row[5]
                })
            
            conn.close()
            return memories
        except Exception as e:
            print(f"Error searching memories: {e}")
            return []
