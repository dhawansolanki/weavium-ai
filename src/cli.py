"""
Command-line interface for the Autogen Agents Framework.
"""

import os
import sys
import argparse
import json
from pathlib import Path
import dotenv

from .framework import AgentFramework
from .utils.memory_manager import MemoryManager
from .utils.logging_utils import setup_logger, get_default_log_file
from .config.config_manager import ConfigManager

def create_agent_command(args):
    """Create an agent from the command line."""
    # Load environment variables
    dotenv.load_dotenv()
    
    # Set up logging
    logger = setup_logger(
        name="autogen_framework_cli",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", get_default_log_file())
    )
    
    # Create a framework instance
    framework = AgentFramework()
    
    # Create the agent
    agent = framework.create_agent(
        agent_type=args.type,
        name=args.name,
        description=args.description,
        system_message=args.system_message,
        human_input_mode=args.human_input_mode
    )
    
    logger.info(f"Created agent: {agent.name}")
    print(f"Created agent: {agent.name}")
    
    # Save the agent configuration if requested
    if args.save_config:
        config_path = args.save_config
        framework.save_config(config_path)
        logger.info(f"Saved configuration to: {config_path}")
        print(f"Saved configuration to: {config_path}")

def run_conversation_command(args):
    """Run a conversation from the command line."""
    # Load environment variables
    dotenv.load_dotenv()
    
    # Set up logging
    logger = setup_logger(
        name="autogen_framework_cli",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", get_default_log_file())
    )
    
    # Create a framework instance
    framework = AgentFramework()
    
    # Load configuration if provided
    if args.config:
        config_manager = ConfigManager()
        config = config_manager.load_from_file(args.config)
        framework.load_config(config)
        logger.info(f"Loaded configuration from: {args.config}")
    
    # Create a memory manager if enabled
    if args.memory:
        memory_db_path = os.getenv("MEMORY_DB_PATH", "./data/cli_conversation.db")
        memory_manager = MemoryManager(db_path=memory_db_path)
        logger.info(f"Created memory manager with database at {memory_db_path}")
    
    # Create the agents
    assistant = framework.create_agent(
        agent_type="assistant",
        name=args.assistant_name,
        description="CLI assistant agent",
        system_message=args.assistant_system_message,
        human_input_mode="NEVER"
    )
    
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name=args.user_name,
        description="CLI user proxy agent",
        system_message="You are a proxy for the human user.",
        human_input_mode=args.human_input_mode,
        code_execution_config={"use_docker": args.use_docker}
    )
    
    logger.info(f"Created agents: {assistant.name} and {user_proxy.name}")
    
    # Start the conversation
    logger.info("Starting conversation")
    framework.start_conversation(
        sender=user_proxy,
        receiver=assistant,
        message=args.message
    )

def run_group_chat_command(args):
    """Run a group chat from the command line."""
    # Load environment variables
    dotenv.load_dotenv()
    
    # Set up logging
    logger = setup_logger(
        name="autogen_framework_cli",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=os.getenv("LOG_FILE", get_default_log_file())
    )
    
    # Create a framework instance
    framework = AgentFramework()
    
    # Load configuration if provided
    if args.config:
        config_manager = ConfigManager()
        config = config_manager.load_from_file(args.config)
        framework.load_config(config)
        logger.info(f"Loaded configuration from: {args.config}")
    
    # Create a memory manager if enabled
    if args.memory:
        memory_db_path = os.getenv("MEMORY_DB_PATH", "./data/cli_group_chat.db")
        memory_manager = MemoryManager(db_path=memory_db_path)
        logger.info(f"Created memory manager with database at {memory_db_path}")
    
    # Create the agents
    agents = []
    
    # Create specialized agents if requested
    if args.specialized:
        # Research agent
        research_knowledge = {
            "instructions": "You are a research specialist. Focus on finding and analyzing information.",
            "guidelines": [
                "Always cite your sources",
                "Consider multiple perspectives",
                "Distinguish between facts and opinions"
            ]
        }
        researcher = framework.create_agent(
            agent_type="specialized",
            name="Researcher",
            description="Research specialist",
            system_message="You are a research specialist in a group chat.",
            domain="research",
            domain_knowledge=research_knowledge
        )
        agents.append(researcher)
        
        # Coding agent
        coding_knowledge = {
            "instructions": "You are a coding specialist. Focus on writing clean, efficient code.",
            "guidelines": [
                "Follow language-specific best practices",
                "Write code that is easy to understand",
                "Include comments for complex logic"
            ]
        }
        coder = framework.create_agent(
            agent_type="specialized",
            name="Coder",
            description="Coding specialist",
            system_message="You are a coding specialist in a group chat.",
            domain="coding",
            domain_knowledge=coding_knowledge
        )
        agents.append(coder)
        
        # Planning agent
        planning_knowledge = {
            "instructions": "You are a planning specialist. Focus on organizing tasks and creating plans.",
            "guidelines": [
                "Break down complex problems into manageable steps",
                "Prioritize tasks based on importance",
                "Set realistic timelines"
            ]
        }
        planner = framework.create_agent(
            agent_type="specialized",
            name="Planner",
            description="Planning specialist",
            system_message="You are a planning specialist in a group chat.",
            domain="planning",
            domain_knowledge=planning_knowledge
        )
        agents.append(planner)
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name=args.user_name,
        description="CLI user proxy agent",
        system_message="You are a proxy for the human user in a group chat.",
        human_input_mode=args.human_input_mode,
        code_execution_config={"use_docker": args.use_docker}
    )
    agents.append(user_proxy)
    
    logger.info(f"Created {len(agents)} agents for the group chat")
    
    # Create a group chat
    group_chat = framework.create_group_chat(
        agents=agents,
        messages=[],
        max_round=args.max_round
    )
    
    # Set up the group chat manager
    manager = framework.create_group_chat_manager(
        groupchat=group_chat,
        name="GroupChatManager",
        description="CLI group chat manager",
        system_message=(
            "You are the manager of this group chat. Your role is to facilitate discussion "
            "between the agents and the user."
        )
    )
    
    logger.info("Created group chat and manager")
    
    # Start the group chat
    logger.info("Starting group chat")
    framework.start_group_chat(
        manager=manager,
        message=args.message
    )

def main():
    """Main entry point for the CLI."""
    # Create the top-level parser
    parser = argparse.ArgumentParser(description="Autogen Agents Framework CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Create the parser for the "create-agent" command
    create_agent_parser = subparsers.add_parser("create-agent", help="Create an agent")
    create_agent_parser.add_argument("--type", "-t", required=True, choices=["assistant", "user_proxy", "specialized"], help="Type of agent to create")
    create_agent_parser.add_argument("--name", "-n", required=True, help="Name of the agent")
    create_agent_parser.add_argument("--description", "-d", default="", help="Description of the agent")
    create_agent_parser.add_argument("--system-message", "-s", required=True, help="System message for the agent")
    create_agent_parser.add_argument("--human-input-mode", choices=["ALWAYS", "NEVER", "TERMINATE"], default="NEVER", help="Human input mode")
    create_agent_parser.add_argument("--save-config", help="Path to save the configuration")
    
    # Create the parser for the "run-conversation" command
    run_conversation_parser = subparsers.add_parser("run-conversation", help="Run a conversation between two agents")
    run_conversation_parser.add_argument("--config", "-c", help="Path to a configuration file")
    run_conversation_parser.add_argument("--assistant-name", default="Assistant", help="Name of the assistant agent")
    run_conversation_parser.add_argument("--assistant-system-message", default="You are a helpful AI assistant.", help="System message for the assistant agent")
    run_conversation_parser.add_argument("--user-name", default="User", help="Name of the user proxy agent")
    run_conversation_parser.add_argument("--human-input-mode", choices=["ALWAYS", "NEVER", "TERMINATE"], default="ALWAYS", help="Human input mode")
    run_conversation_parser.add_argument("--use-docker", action="store_true", help="Use Docker for code execution")
    run_conversation_parser.add_argument("--memory", action="store_true", help="Enable memory persistence")
    run_conversation_parser.add_argument("--message", "-m", required=True, help="Initial message to start the conversation")
    
    # Create the parser for the "run-group-chat" command
    run_group_chat_parser = subparsers.add_parser("run-group-chat", help="Run a group chat with multiple agents")
    run_group_chat_parser.add_argument("--config", "-c", help="Path to a configuration file")
    run_group_chat_parser.add_argument("--specialized", action="store_true", help="Include specialized agents in the group chat")
    run_group_chat_parser.add_argument("--user-name", default="User", help="Name of the user proxy agent")
    run_group_chat_parser.add_argument("--human-input-mode", choices=["ALWAYS", "NEVER", "TERMINATE"], default="ALWAYS", help="Human input mode")
    run_group_chat_parser.add_argument("--use-docker", action="store_true", help="Use Docker for code execution")
    run_group_chat_parser.add_argument("--memory", action="store_true", help="Enable memory persistence")
    run_group_chat_parser.add_argument("--max-round", type=int, default=10, help="Maximum number of rounds for the group chat")
    run_group_chat_parser.add_argument("--message", "-m", required=True, help="Initial message to start the group chat")
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Execute the appropriate command
    if args.command == "create-agent":
        create_agent_command(args)
    elif args.command == "run-conversation":
        run_conversation_command(args)
    elif args.command == "run-group-chat":
        run_group_chat_command(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
