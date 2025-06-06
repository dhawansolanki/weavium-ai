"""
Memory persistence example using the Autogen Agents Framework.
"""

import os
import sys
import dotenv
from pathlib import Path
import uuid

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.framework import AgentFramework
from src.utils.memory_manager import MemoryManager

def main():
    """Run the memory persistence example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Create a memory manager
    memory_manager = MemoryManager(db_path="agent_memories.db")
    
    # Create an assistant agent
    assistant = framework.create_agent(
        agent_type="assistant",
        name="MemoryAssistant",
        description="An AI assistant that can remember information across conversations.",
        system_message=(
            "You are an AI assistant with memory capabilities. You can remember information "
            "from previous conversations and recall it when needed. Try to remember important "
            "details about the user and their preferences."
        ),
        human_input_mode="NEVER"
    )
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name="User",
        description="A proxy for the human user.",
        system_message="You are a proxy for the human user. You can execute code and provide feedback.",
        human_input_mode="ALWAYS",
        code_execution_config={"use_docker": False}
    )
    
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())
    
    # Create a new conversation in memory
    memory_manager.create_conversation(conversation_id, "Memory Demonstration")
    
    # Store some memories for the assistant
    memory_manager.store_memory(
        agent_name="MemoryAssistant",
        memory_type="user_preference",
        content={
            "preference_type": "color",
            "value": "blue",
            "confidence": 0.9,
            "source": "user mentioned in previous conversation"
        }
    )
    
    memory_manager.store_memory(
        agent_name="MemoryAssistant",
        memory_type="user_fact",
        content={
            "fact_type": "hobby",
            "value": "playing chess",
            "confidence": 0.8,
            "source": "user mentioned in previous conversation"
        }
    )
    
    memory_manager.store_memory(
        agent_name="MemoryAssistant",
        memory_type="conversation_summary",
        content="Previously discussed AI ethics and the importance of responsible AI development."
    )
    
    # Define a custom function to demonstrate memory retrieval
    def retrieve_agent_memory(agent_name, memory_type=None):
        """
        Retrieve memories for an agent.
        
        Args:
            agent_name: Name of the agent
            memory_type: Type of memory to retrieve (None for all types)
            
        Returns:
            Agent's memories
        """
        memories = memory_manager.retrieve_memories(agent_name, memory_type)
        return {
            "success": True,
            "agent_name": agent_name,
            "memory_type": memory_type,
            "memories": memories
        }
    
    # Register the memory retrieval function as a tool
    framework.register_tool(
        name="retrieve_memory",
        description="Retrieve memories for an agent",
        function=retrieve_agent_memory,
        parameters={
            "agent_name": {
                "type": "string",
                "description": "Name of the agent"
            },
            "memory_type": {
                "type": "string",
                "description": "Type of memory to retrieve (None for all types)"
            }
        }
    )
    
    # Define a function to store new memories
    def store_agent_memory(agent_name, memory_type, content):
        """
        Store a new memory for an agent.
        
        Args:
            agent_name: Name of the agent
            memory_type: Type of memory
            content: Memory content
            
        Returns:
            Result of the operation
        """
        success = memory_manager.store_memory(agent_name, memory_type, content)
        return {
            "success": success,
            "agent_name": agent_name,
            "memory_type": memory_type,
            "message": "Memory stored successfully" if success else "Failed to store memory"
        }
    
    # Register the memory storage function as a tool
    framework.register_tool(
        name="store_memory",
        description="Store a new memory for an agent",
        function=store_agent_memory,
        parameters={
            "agent_name": {
                "type": "string",
                "description": "Name of the agent"
            },
            "memory_type": {
                "type": "string",
                "description": "Type of memory"
            },
            "content": {
                "type": "object",
                "description": "Memory content"
            }
        }
    )
    
    # Define a function to log conversation messages
    def log_message(sender, receiver, content):
        """
        Log a message in the conversation history.
        
        Args:
            sender: Name of the sender
            receiver: Name of the receiver
            content: Message content
            
        Returns:
            Result of the operation
        """
        success = memory_manager.add_message(conversation_id, sender, receiver, content)
        return {
            "success": success,
            "conversation_id": conversation_id,
            "message": "Message logged successfully" if success else "Failed to log message"
        }
    
    # Register the message logging function as a tool
    framework.register_tool(
        name="log_message",
        description="Log a message in the conversation history",
        function=log_message,
        parameters={
            "sender": {
                "type": "string",
                "description": "Name of the sender"
            },
            "receiver": {
                "type": "string",
                "description": "Name of the receiver"
            },
            "content": {
                "type": "string",
                "description": "Message content"
            }
        }
    )
    
    # Start a conversation with the memory-enabled assistant
    print("Starting conversation with the memory-enabled assistant...")
    
    # Log the initial message
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="User",
        receiver="MemoryAssistant",
        content="Hello! Do you remember anything about me?"
    )
    
    # Start the conversation
    framework.start_conversation(
        sender=user_proxy,
        receiver=assistant,
        message="Hello! Do you remember anything about me?"
    )
    
    # After the conversation, demonstrate retrieving the conversation history
    print("\nRetrieving conversation history...")
    conversation_history = memory_manager.get_conversation_history(conversation_id)
    for message in conversation_history:
        print(f"{message['timestamp']} - {message['sender']} to {message['receiver']}: {message['content']}")

if __name__ == "__main__":
    main()
