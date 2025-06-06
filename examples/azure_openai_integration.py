"""
Azure OpenAI integration example using the Autogen Agents Framework.
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
from src.config.azure_openai import create_llm_config
from src.config.config_manager import AzureOpenAIConfig

def main():
    """Run the Azure OpenAI integration example."""
    
    # Create a new agent framework
    framework = AgentFramework()
    
    # Create custom Azure OpenAI configurations for different agents
    azure_config = AzureOpenAIConfig(
        api_key=os.getenv("AZURE_OPENAI_API_KEY", ""),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT", ""),
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2023-05-15"),
        deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    )
    
    # Create different LLM configs with different parameters
    creative_llm_config = create_llm_config(
        config=azure_config,
        temperature=0.9,  # Higher temperature for more creative responses
        max_tokens=2000
    )
    
    precise_llm_config = create_llm_config(
        config=azure_config,
        temperature=0.1,  # Lower temperature for more precise responses
        max_tokens=1000
    )
    
    # Create a creative assistant agent
    creative_assistant = framework.create_agent(
        agent_type="assistant",
        name="CreativeAssistant",
        description="A creative AI assistant that generates imaginative content.",
        system_message=(
            "You are a creative AI assistant. Your primary role is to generate imaginative, "
            "original content. You excel at creative writing, brainstorming ideas, and thinking "
            "outside the box. Be bold, innovative, and inspirational in your responses."
        ),
        llm_config=creative_llm_config,
        human_input_mode="NEVER"
    )
    
    # Create a precise assistant agent
    precise_assistant = framework.create_agent(
        agent_type="assistant",
        name="PreciseAssistant",
        description="A precise AI assistant that provides accurate, factual information.",
        system_message=(
            "You are a precise AI assistant. Your primary role is to provide accurate, factual "
            "information. You excel at answering questions clearly and concisely, with a focus "
            "on accuracy and precision. Avoid speculation and clearly indicate when you're unsure."
        ),
        llm_config=precise_llm_config,
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
    
    # Demonstrate different agent behaviors based on different Azure OpenAI configurations
    print("Starting conversation with the creative assistant...")
    framework.start_conversation(
        sender=user_proxy,
        receiver=creative_assistant,
        message="Write a short story about artificial intelligence in the year 2050."
    )
    
    print("\nStarting conversation with the precise assistant...")
    framework.start_conversation(
        sender=user_proxy,
        receiver=precise_assistant,
        message="Explain how neural networks work."
    )

if __name__ == "__main__":
    main()
