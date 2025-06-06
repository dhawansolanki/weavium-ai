"""
Multi-agent collaboration example using the Autogen Agents Framework.
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
    """Run the multi-agent collaboration example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Register an MCP server (context7)
    framework.register_mcp_server(
        name="context7",
        endpoint="https://context7-api.example.com",  # Replace with actual endpoint
        api_key=os.getenv("CONTEXT7_API_KEY")
    )
    
    # Create a researcher agent
    researcher = framework.create_agent(
        agent_type="assistant",
        name="Researcher",
        description="An AI agent specialized in research and information gathering.",
        system_message=(
            "You are a research specialist AI. Your primary role is to gather information, "
            "analyze data, and provide well-researched insights. You have access to web search, "
            "document analysis, and MCP servers for additional research capabilities. "
            "Focus on providing accurate, comprehensive information with proper citations."
        ),
        human_input_mode="NEVER"
    )
    
    # Create a coder agent
    coder = framework.create_agent(
        agent_type="assistant",
        name="Coder",
        description="An AI agent specialized in writing and reviewing code.",
        system_message=(
            "You are a coding specialist AI. Your primary role is to write, review, and optimize code. "
            "You can implement solutions in various programming languages, explain code functionality, "
            "and suggest improvements. You have access to documentation through MCP servers. "
            "Focus on writing clean, efficient, and well-documented code."
        ),
        human_input_mode="NEVER"
    )
    
    # Create a planner agent
    planner = framework.create_agent(
        agent_type="assistant",
        name="Planner",
        description="An AI agent specialized in planning and coordination.",
        system_message=(
            "You are a planning specialist AI. Your primary role is to coordinate tasks, "
            "create project plans, and manage workflows. You can break down complex problems "
            "into manageable steps and delegate tasks to other specialized agents. "
            "Focus on creating clear, efficient plans and ensuring all aspects of a problem are addressed."
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
    
    # Register custom tool for inter-agent communication
    def ask_agent(agent_name, question):
        """
        Ask a question to another agent.
        
        Args:
            agent_name: Name of the agent to ask
            question: Question to ask
            
        Returns:
            Agent's response
        """
        agent = framework.get_agent(agent_name)
        if agent is None:
            return {"success": False, "error": f"Agent not found: {agent_name}"}
        
        # This is a simplified implementation
        # In a real implementation, you would use the agent's messaging capabilities
        return {
            "success": True,
            "agent": agent_name,
            "response": f"Response from {agent_name} (simulated): I've processed your question about '{question}'"
        }
    
    framework.register_tool(
        name="ask_agent",
        description="Ask a question to another agent",
        function=ask_agent,
        parameters={
            "agent_name": {
                "type": "string",
                "description": "Name of the agent to ask",
                "enum": ["Researcher", "Coder", "Planner"]
            },
            "question": {
                "type": "string",
                "description": "Question to ask"
            }
        }
    )
    
    # Start a conversation with the planner agent
    framework.start_conversation(
        sender=user_proxy,
        receiver=planner,
        message=(
            "I need to build a web application that analyzes stock market data and visualizes trends. "
            "Can you coordinate with the researcher and coder to create a plan for this project?"
        )
    )

if __name__ == "__main__":
    main()
