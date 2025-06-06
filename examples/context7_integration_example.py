"""
Context7 MCP integration example using the Autogen Agents Framework.
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
from src.mcp.context7_client import Context7Client
from src.config.config_manager import MCPServerConfig

def main():
    """Run the Context7 MCP integration example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Create a Context7 MCP server configuration
    context7_config = MCPServerConfig(
        name="context7",
        endpoint=os.getenv("CONTEXT7_ENDPOINT", "https://context7-api.example.com"),
        api_key=os.getenv("CONTEXT7_API_KEY")
    )
    
    # Create a Context7 client
    context7_client = Context7Client(context7_config)
    
    # Get the tools for the Context7 client
    context7_tools = context7_client.create_autogen_tools()
    
    # Create a documentation assistant agent with Context7 tools
    docs_assistant = framework.create_agent(
        agent_type="assistant",
        name="DocsAssistant",
        description="An AI assistant that can access library documentation through Context7.",
        system_message=(
            "You are a documentation specialist AI assistant. Your primary role is to provide "
            "accurate and helpful information about libraries and frameworks by accessing "
            "up-to-date documentation through the Context7 MCP server. You can resolve library "
            "names to their Context7-compatible IDs and then fetch documentation for those libraries."
        ),
        tools=context7_tools,
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
    
    # Define a function to demonstrate the Context7 client directly
    def demonstrate_context7_client():
        """Demonstrate direct interaction with the Context7 client."""
        print("Demonstrating direct interaction with the Context7 client...")
        
        try:
            # Example: Resolve a library ID for React
            print("Resolving library ID for 'React'...")
            react_id_result = context7_client.resolve_library_id("React")
            print(f"Resolved library ID result: {react_id_result}")
            
            # Get library documentation if we have a valid ID
            if "libraryId" in react_id_result:
                library_id = react_id_result["libraryId"]
                print(f"Getting documentation for library ID: {library_id}...")
                docs_result = context7_client.get_library_docs(library_id, tokens=5000, topic="hooks")
                print(f"Documentation retrieved: {len(str(docs_result))} characters")
                
                # Print a sample of the documentation
                if "documentation" in docs_result:
                    doc_sample = docs_result["documentation"][:500] + "..." if len(docs_result["documentation"]) > 500 else docs_result["documentation"]
                    print(f"Documentation sample: {doc_sample}")
        except Exception as e:
            print(f"Error interacting with Context7 client: {e}")
    
    # Start a conversation with the documentation assistant
    print("Starting conversation with the documentation assistant...")
    framework.start_conversation(
        sender=user_proxy,
        receiver=docs_assistant,
        message=(
            "I'm working on a React project and need to understand how hooks work, "
            "particularly useEffect and useState. Can you provide documentation and examples?"
        )
    )
    
    # Demonstrate direct interaction with the Context7 client
    # Note: This would only work with actual Context7 credentials
    # demonstrate_context7_client()

if __name__ == "__main__":
    main()
