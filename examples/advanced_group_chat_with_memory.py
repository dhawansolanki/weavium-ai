"""
Advanced group chat example with specialized agents and memory persistence.
"""

import os
import sys
import uuid
import dotenv
from pathlib import Path
# We'll use direct agent conversations instead of autogen's GroupChat

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.framework import AgentFramework
from src.utils.memory_manager import MemoryManager

def main():
    """Run the advanced group chat example with memory persistence."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Create a memory manager
    memory_manager = MemoryManager(db_path="group_chat_memories.db")
    
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())
    memory_manager.create_conversation(conversation_id, "Advanced Group Chat")
    
    # Define domain knowledge for specialized agents
    research_knowledge = {
        "instructions": "You are a research specialist. Focus on finding and analyzing information.",
        "guidelines": [
            "Always cite your sources",
            "Consider multiple perspectives",
            "Distinguish between facts and opinions",
            "Identify gaps in available information"
        ],
        "examples": [
            "When asked about climate change, I should provide data from peer-reviewed studies.",
            "When analyzing market trends, I should consider economic indicators from multiple sources."
        ]
    }
    
    coding_knowledge = {
        "instructions": "You are a coding specialist. Focus on writing clean, efficient, and well-documented code.",
        "guidelines": [
            "Follow language-specific best practices",
            "Write code that is easy to understand and maintain",
            "Include comments for complex logic",
            "Consider edge cases and error handling"
        ],
        "examples": [
            "When writing Python code, I should follow PEP 8 style guidelines.",
            "When implementing algorithms, I should analyze time and space complexity."
        ]
    }
    
    planning_knowledge = {
        "instructions": "You are a planning specialist. Focus on organizing tasks and creating actionable plans.",
        "guidelines": [
            "Break down complex problems into manageable steps",
            "Prioritize tasks based on importance and dependencies",
            "Set realistic timelines",
            "Identify potential risks and mitigation strategies"
        ],
        "examples": [
            "When planning a software project, I should create a roadmap with milestones.",
            "When organizing tasks, I should consider resource constraints and dependencies."
        ]
    }
    
    # Define a function to log messages to the memory manager
    def log_message_to_memory(sender_name, receiver_name, content):
        """Log a message to the memory manager."""
        memory_manager.add_message(conversation_id, sender_name, receiver_name, content)
        return True
    
    # Define a function to retrieve agent memories
    def get_agent_memories(agent_name, memory_type=None):
        """Retrieve memories for an agent."""
        memories = memory_manager.retrieve_memories(agent_name, memory_type)
        return memories
    
    # Define a function to store agent memories
    def store_agent_memory(agent_name, memory_type, content):
        """Store a memory for an agent."""
        success = memory_manager.store_memory(agent_name, memory_type, content)
        return success
    
    # Register memory-related tools
    framework.register_tool(
        name="log_message",
        description="Log a message to the conversation history",
        function=log_message_to_memory,
        parameters={
            "sender_name": {
                "type": "string",
                "description": "Name of the sender"
            },
            "receiver_name": {
                "type": "string",
                "description": "Name of the receiver"
            },
            "content": {
                "type": "string",
                "description": "Message content"
            }
        }
    )
    
    framework.register_tool(
        name="get_memories",
        description="Retrieve memories for an agent",
        function=get_agent_memories,
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
    
    framework.register_tool(
        name="store_memory",
        description="Store a memory for an agent",
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
    
    # Create specialized agents
    # Incorporate domain knowledge into system message
    enhanced_system_message = f"You are a research specialist in a group chat. Your role is to find and analyze information.\n\nDomain Knowledge: {research_knowledge}"
    
    researcher = framework.create_agent(
        agent_type="assistant",
        name="Researcher",
        description="Research specialist that finds and analyzes information",
        system_message=enhanced_system_message
    )
    
    # Incorporate domain knowledge into system message for coder
    enhanced_coder_message = f"You are a coding specialist in a group chat. Your role is to write and review code.\n\nDomain Knowledge: {coding_knowledge}"
    
    coder = framework.create_agent(
        agent_type="assistant",
        name="Coder",
        description="Coding specialist that writes clean and efficient code",
        system_message=enhanced_coder_message
    )
    
    # Incorporate domain knowledge into system message for planner
    enhanced_planner_message = f"You are a planning specialist in a group chat. Your role is to organize tasks and create actionable plans.\n\nDomain Knowledge: {planning_knowledge}"
    
    planner = framework.create_agent(
        agent_type="assistant",
        name="Planner",
        description="Planning specialist that organizes tasks and creates plans",
        system_message=enhanced_planner_message
    )
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name="User",
        description="A proxy for the human user",
        system_message="You are a proxy for the human user in a group chat.",
        human_input_mode="ALWAYS",
        code_execution_config={"use_docker": False}
    )
    
    # Store initial memories for agents
    memory_manager.store_memory(
        agent_name="Researcher",
        memory_type="skill",
        content={
            "skill_name": "information_gathering",
            "proficiency": "expert",
            "description": "Ability to gather information from various sources and synthesize it"
        }
    )
    
    memory_manager.store_memory(
        agent_name="Coder",
        memory_type="skill",
        content={
            "skill_name": "python_programming",
            "proficiency": "expert",
            "description": "Ability to write clean, efficient Python code"
        }
    )
    
    memory_manager.store_memory(
        agent_name="Planner",
        memory_type="skill",
        content={
            "skill_name": "task_organization",
            "proficiency": "expert",
            "description": "Ability to break down complex problems into manageable tasks"
        }
    )
    
    # Create a coordinator agent to facilitate the conversation between other agents
    coordinator = framework.create_agent(
        agent_type="assistant",
        name="Coordinator",
        description="Coordinates the conversation between specialized agents",
        system_message="You are a coordinator for specialized agents. Your role is to facilitate discussion and delegate tasks between a researcher, coder, and planner."
    )
    
    # Define a function to print conversation history
    def print_conversation_history():
        """Print the conversation history from the memory manager."""
        print("\n=== Conversation History ===\n")
        history = memory_manager.get_conversation_history(conversation_id)
        for i, message in enumerate(history, 1):
            print(f"{i}. {message['timestamp']} - {message['sender']} to {message['receiver']}: {message['content'][:100]}...")
    
    # Define the initial message
    initial_message = (
        "I need help building a web application that analyzes stock market data. "
        "I need research on which APIs to use, code for data analysis, and a project plan."
    )
    
    # Start the group chat
    print("Starting the advanced group chat with specialized agents and memory persistence...")
    
    # Log the initial message to memory
    memory_manager.add_message(conversation_id, "User", "Coordinator", initial_message)
    
    # Start a conversation sequence instead of using GroupChat
    # First, user talks to coordinator
    print("\n[User -> Coordinator]")
    user_proxy.initiate_chat(coordinator, message=initial_message)
    
    # Then coordinator delegates to researcher
    print("\n[Coordinator -> Researcher]")
    research_request = "Please research APIs for stock market data analysis and provide recommendations."
    coordinator.initiate_chat(researcher, message=research_request)
    memory_manager.add_message(conversation_id, "Coordinator", "Researcher", research_request)
    
    # Then coordinator delegates to planner
    print("\n[Coordinator -> Planner]")
    planning_request = "Please create a project plan for building a web application that analyzes stock market data."
    coordinator.initiate_chat(planner, message=planning_request)  
    memory_manager.add_message(conversation_id, "Coordinator", "Planner", planning_request)
    
    # Finally, coordinator delegates to coder
    print("\n[Coordinator -> Coder]")
    coding_request = "Please provide sample code for parsing and analyzing stock market data."
    coordinator.initiate_chat(coder, message=coding_request)
    memory_manager.add_message(conversation_id, "Coordinator", "Coder", coding_request)
    
    # Print the conversation history
    print_conversation_history()
    
    # Print agent memories after the conversation
    print("\n=== Agent Memories After Conversation ===")
    for agent_name in ["Researcher", "Coder", "Planner"]:
        memories = memory_manager.retrieve_memories(agent_name)
        print(f"\n{agent_name}'s Memories:")
        for memory in memories:
            print(f"- Type: {memory['memory_type']}")
            if isinstance(memory['content'], dict):
                for key, value in memory['content'].items():
                    print(f"  {key}: {value}")
            else:
                print(f"  Content: {memory['content']}")

if __name__ == "__main__":
    main()
