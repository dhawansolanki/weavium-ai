"""
MCP server integration example using the Autogen Agents Framework.
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
from src.mcp.mcp_client import MCPClient, MCPManager

def main():
    """Run the MCP server integration example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Register the Context7 MCP server
    framework.register_mcp_server(
        name="context7",
        endpoint="https://context7-api.example.com",  # Replace with actual endpoint
        api_key=os.getenv("CONTEXT7_API_KEY")
    )
    
    # Create an assistant agent with MCP capabilities
    assistant = framework.create_agent(
        agent_type="assistant",
        name="MCPAssistant",
        description="An AI assistant that can access MCP servers for enhanced capabilities.",
        system_message=(
            "You are an AI assistant with access to MCP (Model Context Protocol) servers. "
            "You can use these servers to access external knowledge, tools, and capabilities. "
            "Specifically, you have access to the Context7 MCP server, which provides documentation "
            "for various libraries and frameworks. Use these capabilities to provide accurate and "
            "helpful responses."
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
    
    # Define a custom function to demonstrate direct MCP server interaction
    def demonstrate_mcp_interaction():
        """Demonstrate direct interaction with MCP servers."""
        print("Demonstrating direct MCP server interaction...")
        
        # Get the MCP manager
        mcp_manager = framework.mcp_manager
        
        # Get the Context7 client
        context7_client = mcp_manager.get_client("context7")
        if context7_client is None:
            print("Context7 client not found!")
            return
        
        # Example: Resolve a library ID
        try:
            print("Resolving library ID for 'React'...")
            result = context7_client.resolve_library_id("React")
            print(f"Resolved library ID: {result}")
            
            # Get library documentation
            if "libraryId" in result:
                library_id = result["libraryId"]
                print(f"Getting documentation for library ID: {library_id}...")
                docs = context7_client.get_library_docs(library_id, tokens=5000)
                print(f"Documentation retrieved: {len(docs)} characters")
        except Exception as e:
            print(f"Error interacting with MCP server: {e}")
    
    # Start a conversation with the assistant
    print("Starting conversation with the MCP-enabled assistant...")
    framework.start_conversation(
        sender=user_proxy,
        receiver=assistant,
        message="Can you tell me about React hooks using the Context7 MCP server?"
    )
    
    # Demonstrate direct MCP interaction
    # Note: This would only work with actual MCP server credentials
    # demonstrate_mcp_interaction()

if __name__ == "__main__":
    main()
