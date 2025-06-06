"""
Unit tests for the memory manager.
"""

import os
import sys
import unittest
import tempfile
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from src.utils.memory_manager import MemoryManager

class TestMemoryManager(unittest.TestCase):
    """Test cases for the memory manager."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Create a temporary database file
        self.temp_db = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        self.temp_db.close()
        self.memory_manager = MemoryManager(db_path=self.temp_db.name)
    
    def tearDown(self):
        """Tear down test fixtures."""
        # Remove the temporary database file
        os.unlink(self.temp_db.name)
    
    def test_create_conversation(self):
        """Test creating a conversation."""
        # Create a conversation
        result = self.memory_manager.create_conversation("test-conversation", "Test Conversation")
        self.assertTrue(result)
        
        # Get recent conversations
        conversations = self.memory_manager.get_recent_conversations()
        self.assertEqual(len(conversations), 1)
        self.assertEqual(conversations[0]["conversation_id"], "test-conversation")
        self.assertEqual(conversations[0]["title"], "Test Conversation")
    
    def test_add_message(self):
        """Test adding a message to a conversation."""
        # Add a message to a new conversation
        result = self.memory_manager.add_message(
            "test-conversation",
            "sender",
            "receiver",
            "Hello, world!"
        )
        self.assertTrue(result)
        
        # Get conversation history
        history = self.memory_manager.get_conversation_history("test-conversation")
        self.assertEqual(len(history), 1)
        self.assertEqual(history[0]["sender"], "sender")
        self.assertEqual(history[0]["receiver"], "receiver")
        self.assertEqual(history[0]["content"], "Hello, world!")
    
    def test_store_and_retrieve_memory(self):
        """Test storing and retrieving memories."""
        # Store a string memory
        result = self.memory_manager.store_memory(
            "test-agent",
            "fact",
            "The sky is blue"
        )
        self.assertTrue(result)
        
        # Store a dictionary memory
        result = self.memory_manager.store_memory(
            "test-agent",
            "preference",
            {"color": "blue", "food": "pizza"}
        )
        self.assertTrue(result)
        
        # Retrieve all memories for the agent
        memories = self.memory_manager.retrieve_memories("test-agent")
        self.assertEqual(len(memories), 2)
        
        # Retrieve memories by type
        fact_memories = self.memory_manager.retrieve_memories("test-agent", "fact")
        self.assertEqual(len(fact_memories), 1)
        self.assertEqual(fact_memories[0]["content"], "The sky is blue")
        
        preference_memories = self.memory_manager.retrieve_memories("test-agent", "preference")
        self.assertEqual(len(preference_memories), 1)
        self.assertEqual(preference_memories[0]["content"]["color"], "blue")
        self.assertEqual(preference_memories[0]["content"]["food"], "pizza")
    
    def test_update_memory(self):
        """Test updating a memory."""
        # Store a memory
        self.memory_manager.store_memory(
            "test-agent",
            "fact",
            "The sky is blue"
        )
        
        # Retrieve the memory to get its ID
        memories = self.memory_manager.retrieve_memories("test-agent", "fact")
        memory_id = memories[0]["id"]
        
        # Update the memory
        result = self.memory_manager.update_memory(memory_id, "The sky is sometimes gray")
        self.assertTrue(result)
        
        # Retrieve the updated memory
        updated_memories = self.memory_manager.retrieve_memories("test-agent", "fact")
        self.assertEqual(updated_memories[0]["content"], "The sky is sometimes gray")
    
    def test_delete_memory(self):
        """Test deleting a memory."""
        # Store a memory
        self.memory_manager.store_memory(
            "test-agent",
            "fact",
            "The sky is blue"
        )
        
        # Retrieve the memory to get its ID
        memories = self.memory_manager.retrieve_memories("test-agent", "fact")
        memory_id = memories[0]["id"]
        
        # Delete the memory
        result = self.memory_manager.delete_memory(memory_id)
        self.assertTrue(result)
        
        # Verify the memory is deleted
        memories = self.memory_manager.retrieve_memories("test-agent", "fact")
        self.assertEqual(len(memories), 0)
    
    def test_search_memories(self):
        """Test searching memories."""
        # Store some memories
        self.memory_manager.store_memory(
            "test-agent",
            "fact",
            "The sky is blue"
        )
        self.memory_manager.store_memory(
            "test-agent",
            "fact",
            "The grass is green"
        )
        self.memory_manager.store_memory(
            "test-agent",
            "preference",
            {"color": "blue", "food": "pizza"}
        )
        
        # Search for memories containing "blue"
        results = self.memory_manager.search_memories("blue")
        self.assertEqual(len(results), 2)  # Should find both the fact and the preference
        
        # Search for memories containing "green"
        results = self.memory_manager.search_memories("green")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["content"], "The grass is green")

if __name__ == "__main__":
    unittest.main()
