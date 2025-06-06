"""
Group chat collaboration example using the Autogen Agents Framework.
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
from src.agents.group_chat import GroupChatManager

def main():
    """Run the group chat collaboration example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Register an MCP server (context7)
    framework.register_mcp_server(
        name="context7",
        endpoint="https://context7-api.example.com",  # Replace with actual endpoint
        api_key=os.getenv("CONTEXT7_API_KEY")
    )
    
    # Create a product manager agent
    product_manager = framework.create_agent(
        agent_type="assistant",
        name="ProductManager",
        description="A product manager who oversees the project and makes key decisions.",
        system_message=(
            "You are a product manager overseeing this project. Your role is to define requirements, "
            "prioritize features, and ensure the team is aligned with the project goals. You should "
            "make key decisions when there are disagreements and keep the team focused on delivering "
            "value to users. Be clear, decisive, and considerate of technical constraints."
        ),
        human_input_mode="NEVER"
    )
    
    # Create a software architect agent
    architect = framework.create_agent(
        agent_type="assistant",
        name="Architect",
        description="A software architect who designs the system architecture.",
        system_message=(
            "You are a software architect responsible for designing the system architecture. "
            "Your role is to make high-level design decisions, choose appropriate technologies, "
            "and ensure the system is scalable, maintainable, and secure. Consider trade-offs "
            "between different approaches and explain your reasoning clearly."
        ),
        human_input_mode="NEVER"
    )
    
    # Create a developer agent
    developer = framework.create_agent(
        agent_type="assistant",
        name="Developer",
        description="A developer who implements the code.",
        system_message=(
            "You are a developer responsible for implementing the code. Your role is to write "
            "clean, efficient, and well-documented code that meets the requirements. Consider "
            "best practices, performance, and maintainability in your implementations. Provide "
            "specific code examples when appropriate."
        ),
        human_input_mode="NEVER"
    )
    
    # Create a tester agent
    tester = framework.create_agent(
        agent_type="assistant",
        name="Tester",
        description="A tester who ensures the quality of the code.",
        system_message=(
            "You are a tester responsible for ensuring the quality of the code. Your role is to "
            "identify potential issues, edge cases, and bugs in the proposed implementations. "
            "Think critically about how the system might fail and suggest improvements to make "
            "it more robust."
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
    
    # Create a group chat manager
    group_chat_manager = GroupChatManager()
    
    # Create a group chat with all agents
    project_team = group_chat_manager.create_group_chat(
        name="ProjectTeam",
        agents=[product_manager, architect, developer, tester, user_proxy],
        max_round=15,
        speaker_selection_method="auto",
        allow_repeat_speaker=False
    )
    
    # Start the group chat with an initial task
    print("Starting group chat for project planning...")
    group_chat_manager.initiate_chat(
        group_chat_name="ProjectTeam",
        manager=user_proxy,
        message=(
            "We need to build a web application for tracking personal finances. "
            "The application should allow users to track income and expenses, categorize transactions, "
            "set budgets, and visualize spending patterns. Let's work together to plan and design this application."
        )
    )

if __name__ == "__main__":
    main()
