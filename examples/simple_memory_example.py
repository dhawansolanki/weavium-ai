"""
Simple example demonstrating the memory manager with a basic conversation.
"""

import os
import sys
import uuid
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.utils.memory_manager import MemoryManager
from src.utils.logging_utils import setup_logger, get_default_log_file

def main():
    """Run the simple memory example."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="simple_memory_example",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting simple memory example")
    
    # Create a memory manager
    memory_db_path = os.getenv("MEMORY_DB_PATH", "./data/simple_memory.db")
    memory_manager = MemoryManager(db_path=memory_db_path)
    logger.info(f"Created memory manager with database at {memory_db_path}")
    
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())
    memory_manager.create_conversation(conversation_id, "Simple Memory Example")
    logger.info(f"Created conversation with ID: {conversation_id}")
    
    # Store some memories
    memory_manager.store_memory(
        agent_name="Assistant",
        memory_type="fact",
        content={
            "subject": "user",
            "predicate": "likes",
            "object": "Python programming"
        }
    )
    logger.info("Stored fact memory for Assistant")
    
    memory_manager.store_memory(
        agent_name="Assistant",
        memory_type="skill",
        content={
            "skill_name": "coding",
            "proficiency": "expert",
            "description": "Ability to write clean, efficient Python code"
        }
    )
    logger.info("Stored skill memory for Assistant")
    
    # Add some messages to the conversation
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="User",
        receiver="Assistant",
        content="Hello, can you help me with a Python problem?"
    )
    logger.info("Added user message to conversation")
    
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="Assistant",
        receiver="User",
        content="Of course! I'd be happy to help with your Python problem. What specifically are you working on?"
    )
    logger.info("Added assistant message to conversation")
    
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="User",
        receiver="Assistant",
        content="I'm trying to implement a memory manager for my agents."
    )
    logger.info("Added user message to conversation")
    
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="Assistant",
        receiver="User",
        content="That's a great project! A memory manager is essential for maintaining context and knowledge across conversations. Would you like me to help you design the database schema for it?"
    )
    logger.info("Added assistant message to conversation")
    
    # Retrieve and print conversation history
    print("\n=== Conversation History ===")
    history = memory_manager.get_conversation_history(conversation_id)
    for i, message in enumerate(history, 1):
        print(f"{i}. {message['timestamp']} - {message['sender']} to {message['receiver']}: {message['content']}")
    
    # Retrieve and print agent memories
    print("\n=== Agent Memories ===")
    memories = memory_manager.retrieve_memories("Assistant")
    for memory in memories:
        print(f"- Type: {memory['memory_type']}")
        if isinstance(memory['content'], dict):
            for key, value in memory['content'].items():
                print(f"  {key}: {value}")
        else:
            print(f"  Content: {memory['content']}")
    
    # Search for memories
    print("\n=== Memory Search ===")
    search_results = memory_manager.search_memories("Python")
    print(f"Found {len(search_results)} memories containing 'Python':")
    for memory in search_results:
        print(f"- Agent: {memory['agent_name']}")
        print(f"- Type: {memory['memory_type']}")
        if isinstance(memory['content'], dict):
            for key, value in memory['content'].items():
                print(f"  {key}: {value}")
        else:
            print(f"  Content: {memory['content']}")
    
    logger.info("Simple memory example completed")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
