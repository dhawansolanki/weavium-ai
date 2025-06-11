"""
Basic example demonstrating the core functionality of the agent framework.
This example creates a simple assistant agent and a user proxy agent,
then initiates a conversation between them.
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
from src.utils.logging_utils import setup_logger, get_default_log_file

def main():
    """Run the basic agent example."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="basic_agent_example",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting basic agent example")
    
    # Create the agent framework
    framework = AgentFramework()
    logger.info("Created agent framework")
    
    # Create an assistant agent
    assistant = framework.create_agent(
        agent_type="assistant",
        name="BasicAssistant",
        description="A helpful assistant that can answer questions",
        system_message="You are a helpful assistant. Answer questions concisely and accurately.",
        llm_config=None  # Use default config or None for local testing
    )
    logger.info("Created assistant agent")
    
    from src.agents.user_proxy_agent import UserProxyAgent
    
    # Create a user proxy agent
    user_proxy = UserProxyAgent(
        name="UserProxy",
        description="A proxy for the human user",
        system_message="You are a proxy for the human user. You help facilitate the conversation.",
        human_input_mode="ALWAYS",
        tools=framework.tool_registry.get_tool_dicts()
    )
    framework.agents[user_proxy.name] = user_proxy
    logger.info("Created user proxy agent")
    
    # Initiate a conversation
    logger.info("Starting conversation")
    user_proxy.initiate_chat(
        assistant,
        message="Hello! Can you tell me what the agent framework does?"
    )
    
    logger.info("Basic agent example completed")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
