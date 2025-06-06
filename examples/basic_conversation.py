"""
Basic conversation example using the Autogen Agents Framework.
"""

import os
import sys
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.framework import AgentFramework

def main():
    """Run the basic conversation example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Register an MCP server (context7)
    framework.register_mcp_server(
        name="context7",
        endpoint="https://context7-api.example.com",  # Replace with actual endpoint
        api_key=os.getenv("CONTEXT7_API_KEY")
    )
    
    # Create an assistant agent
    assistant = framework.create_agent(
        agent_type="assistant",
        name="Assistant",
        description="A helpful AI assistant that can answer questions and perform tasks.",
        system_message=(
            "You are a helpful AI assistant. You can answer questions, provide information, "
            "and help with various tasks. You have access to tools that allow you to search "
            "the web, read and write files, make HTTP requests, and access MCP servers for "
            "additional capabilities."
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
    
    # Start a conversation
    framework.start_conversation(
        sender=user_proxy,
        receiver=assistant,
        message="Hello! Can you help me understand how to use the Autogen Agents Framework?"
    )

if __name__ == "__main__":
    main()
