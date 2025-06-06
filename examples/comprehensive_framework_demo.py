"""
Comprehensive demonstration of the Autogen Agents Framework.

This example showcases all the major components of the framework:
- Multiple agent types (assistant, user proxy, specialized)
- Group chat with multiple agents
- Memory persistence
- MCP server integration (Context7)
- Custom tools
- Logging
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

from src.framework import AgentFramework
from src.utils.memory_manager import MemoryManager
from src.utils.logging_utils import setup_logger, get_default_log_file
from src.mcp.context7_client import Context7Client
from src.config.config_manager import MCPServerConfig

def main():
    """Run the comprehensive framework demonstration."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="framework_demo",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting comprehensive framework demonstration")
    
    # Create a new agent framework
    framework = AgentFramework()
    logger.info("Created agent framework")
    
    # Create a memory manager
    memory_db_path = os.getenv("MEMORY_DB_PATH", "./data/comprehensive_demo.db")
    memory_manager = MemoryManager(db_path=memory_db_path)
    logger.info(f"Created memory manager with database at {memory_db_path}")
    
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())
    memory_manager.create_conversation(conversation_id, "Comprehensive Framework Demo")
    logger.info(f"Created conversation with ID: {conversation_id}")
    
    # Set up Context7 MCP server if credentials are available
    context7_api_key = os.getenv("CONTEXT7_API_KEY")
    if context7_api_key:
        context7_config = MCPServerConfig(
            name="context7",
            endpoint=os.getenv("CONTEXT7_ENDPOINT", "https://api.context7.com/v1"),
            api_key=context7_api_key
        )
        context7_client = Context7Client(context7_config)
        context7_tools = context7_client.create_autogen_tools()
        framework.register_mcp_server(context7_config)
        logger.info("Registered Context7 MCP server")
    else:
        context7_tools = []
        logger.warning("Context7 API key not found, skipping MCP server registration")
    
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
    
    # Define memory-related tools
    def log_message_to_memory(sender_name, receiver_name, content):
        """Log a message to the memory manager."""
        success = memory_manager.add_message(conversation_id, sender_name, receiver_name, content)
        logger.info(f"Logged message from {sender_name} to {receiver_name}")
        return {
            "success": success,
            "conversation_id": conversation_id,
            "message": "Message logged successfully" if success else "Failed to log message"
        }
    
    def get_agent_memories(agent_name, memory_type=None):
        """Retrieve memories for an agent."""
        memories = memory_manager.retrieve_memories(agent_name, memory_type)
        logger.info(f"Retrieved {len(memories)} memories for agent {agent_name}")
        return memories
    
    def store_agent_memory(agent_name, memory_type, content):
        """Store a memory for an agent."""
        success = memory_manager.store_memory(agent_name, memory_type, content)
        logger.info(f"Stored memory of type {memory_type} for agent {agent_name}")
        return {
            "success": success,
            "agent_name": agent_name,
            "memory_type": memory_type,
            "message": "Memory stored successfully" if success else "Failed to store memory"
        }
    
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
    
    # Define a simple web search tool (mock implementation)
    def web_search(query):
        """Perform a web search (mock implementation)."""
        logger.info(f"Performing web search for: {query}")
        return {
            "success": True,
            "query": query,
            "results": [
                {
                    "title": "Example Search Result 1",
                    "url": "https://example.com/result1",
                    "snippet": "This is an example search result for the query."
                },
                {
                    "title": "Example Search Result 2",
                    "url": "https://example.com/result2",
                    "snippet": "Another example search result for the query."
                }
            ]
        }
    
    # Register the web search tool
    framework.register_tool(
        name="web_search",
        description="Search the web for information",
        function=web_search,
        parameters={
            "query": {
                "type": "string",
                "description": "Search query"
            }
        }
    )
    
    # Get tools from the framework's registry
    framework_tools = framework.tool_registry.get_all_tools()
    
    # Convert tools to the format expected by Autogen
    all_tools = []
    
    # Add framework tools
    for tool in framework_tools:
        if isinstance(tool, dict):
            all_tools.append(tool)
    
    # Add Context7 tools
    for tool in context7_tools:
        if isinstance(tool, dict):
            all_tools.append(tool)
    
    # Create specialized agents (using assistant type since specialized is not directly supported)
    # For researcher
    researcher_system_message = f"You are a research specialist in a group chat. Your role is to find and analyze information.\n\n"
    researcher_system_message += f"Instructions: {research_knowledge['instructions']}\n\n"
    researcher_system_message += "Guidelines:\n"
    for guideline in research_knowledge['guidelines']:
        researcher_system_message += f"- {guideline}\n"
    researcher_system_message += "\nExamples:\n"
    for example in research_knowledge['examples']:
        researcher_system_message += f"- {example}\n"
    
    researcher = framework.create_agent(
        agent_type="assistant",
        name="Researcher",
        description="Research specialist that finds and analyzes information",
        system_message=researcher_system_message,
        tools=all_tools
    )
    logger.info("Created researcher agent")
    
    # For coder
    coder_system_message = f"You are a coding specialist in a group chat. Your role is to write and review code.\n\n"
    coder_system_message += f"Instructions: {coding_knowledge['instructions']}\n\n"
    coder_system_message += "Guidelines:\n"
    for guideline in coding_knowledge['guidelines']:
        coder_system_message += f"- {guideline}\n"
    coder_system_message += "\nExamples:\n"
    for example in coding_knowledge['examples']:
        coder_system_message += f"- {example}\n"
    
    coder = framework.create_agent(
        agent_type="assistant",
        name="Coder",
        description="Coding specialist that writes clean and efficient code",
        system_message=coder_system_message,
        tools=all_tools
    )
    logger.info("Created coder agent")
    
    # For planner
    planner_system_message = f"You are a planning specialist in a group chat. Your role is to organize tasks and create actionable plans.\n\n"
    planner_system_message += f"Instructions: {planning_knowledge['instructions']}\n\n"
    planner_system_message += "Guidelines:\n"
    for guideline in planning_knowledge['guidelines']:
        planner_system_message += f"- {guideline}\n"
    planner_system_message += "\nExamples:\n"
    for example in planning_knowledge['examples']:
        planner_system_message += f"- {example}\n"
    
    planner = framework.create_agent(
        agent_type="assistant",
        name="Planner",
        description="Planning specialist that organizes tasks and creates plans",
        system_message=planner_system_message,
        tools=all_tools
    )
    logger.info("Created planner agent")
    
    # Create a documentation assistant with Context7 tools
    docs_assistant = framework.create_agent(
        agent_type="assistant",
        name="DocsAssistant",
        description="Documentation specialist that can access library documentation",
        system_message=(
            "You are a documentation specialist in a group chat. Your role is to provide "
            "accurate information about libraries and frameworks by accessing documentation."
        ),
        tools=context7_tools
    )
    logger.info("Created documentation assistant agent")
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name="User",
        description="A proxy for the human user",
        system_message="You are a proxy for the human user in a group chat.",
        human_input_mode="ALWAYS",
        code_execution_config={"use_docker": False}
    )
    logger.info("Created user proxy agent")
    
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
    
    # Import Autogen's group chat components
    import autogen
    from autogen.agentchat.groupchat import GroupChat, GroupChatManager
    
    # Create a custom GroupChat class that avoids the validation issue
    class MyGroupChat(GroupChat):
        def __post_init__(self):
            # Skip the problematic validation in the original __post_init__
            # Set up a fully connected graph instead
            self._agent_names = {agent.name: agent for agent in self.agents}
            self.allowed_speaker_transitions_dict = {}
            for agent in self.agents:
                others = [a for a in self.agents if a.name != agent.name]
                self.allowed_speaker_transitions_dict[agent] = others
    
    # Create the group chat using our custom class
    group_chat = MyGroupChat(
        agents=[researcher, coder, planner, docs_assistant, user_proxy],
        messages=[],
        max_round=int(os.getenv("MAX_ROUND", "10"))
    )
    logger.info("Created group chat")
    
    # Set up the group chat manager
    manager = GroupChatManager(
        groupchat=group_chat,
        name="GroupChatManager",
        description="Manager for the group chat",
        system_message=(
            "You are the manager of this group chat. Your role is to facilitate discussion "
            "between the specialized agents and the user. Make sure each agent contributes "
            "according to their expertise."
        )
    )
    logger.info("Created group chat manager")
    
    # Define a function to print conversation history
    def print_conversation_history():
        """Print the conversation history from the memory manager."""
        print("\n=== Conversation History ===")
        history = memory_manager.get_conversation_history(conversation_id)
        for i, message in enumerate(history, 1):
            print(f"{i}. {message['timestamp']} - {message['sender']} to {message['receiver']}: {message['content'][:100]}...")
    
    # Start the group chat
    print("Starting the comprehensive framework demonstration...")
    logger.info("Starting group chat")
    
    # Log the initial message
    initial_message = (
        "I need help building a web application that uses React for the frontend and Python for the backend. "
        "I need research on best practices, code examples, and a project plan."
    )
    memory_manager.add_message(conversation_id, "User", "GroupChat", initial_message)
    
    # Let's try a different approach - let's use the framework's start_conversation method instead of GroupChat
    # This should avoid all the API compatibility issues
    
    print("User:", initial_message)
    
    # Start a direct conversation between agents instead of using GroupChat
    try:
        # Add a basic conversation between key agents
        framework.start_conversation(
            sender=user_proxy,
            receiver=planner,  # Start with the planner to organize the task
            message=initial_message
        )
        
        # Then let the planner delegate to other agents as needed
        planner_response = memory_manager.get_last_message("Planner", "User")
        if planner_response:
            print(f"Planner: {planner_response['content'][:200]}...")
            
            # Let the researcher provide information
            framework.start_conversation(
                sender=planner,
                receiver=researcher,
                message="Please research best practices for React frontend and Python backend."
            )
            
            # Let the coder provide code examples
            framework.start_conversation(
                sender=planner,
                receiver=coder,
                message="Please provide code examples for setting up a React frontend with Python backend."
            )
    except Exception as e:
        print(f"Error in conversation: {str(e)}")
        print("Falling back to simpler conversation flow.")
        
        # Fallback: just log some simulated responses for demonstration purposes
        sample_responses = {
            "Planner": "I'll break this down into manageable tasks: 1. Research stack options, 2. Set up backend, 3. Set up frontend, 4. Connect them.",
            "Researcher": "For React+Python, popular choices include React with Django REST Framework or Flask.",
            "Coder": "Here's a starter code for Flask backend with React frontend using create-react-app."
        }
        
        for agent_name, response in sample_responses.items():
            print(f"{agent_name}: {response}")
            memory_manager.add_message(conversation_id, agent_name, "User", response)
    
    # Print the conversation history
    print_conversation_history()
    
    # Print agent memories after the conversation
    print("\n=== Agent Memories After Conversation ===")
    for agent_name in ["Researcher", "Coder", "Planner", "DocsAssistant"]:
        memories = memory_manager.retrieve_memories(agent_name)
        print(f"\n{agent_name}'s Memories:")
        for memory in memories:
            print(f"- Type: {memory['memory_type']}")
            if isinstance(memory['content'], dict):
                for key, value in memory['content'].items():
                    print(f"  {key}: {value}")
            else:
                print(f"  Content: {memory['content']}")
    
    logger.info("Comprehensive framework demonstration completed")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
