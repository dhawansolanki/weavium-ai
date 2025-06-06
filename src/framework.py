"""
Main framework module for the Autogen Agents Framework.
"""

import os
from typing import Dict, Any, List, Optional, Union, Type
from .config.config_manager import ConfigManager, AgentConfig, ToolConfig, MCPServerConfig
from .config.azure_openai import create_llm_config
from .agents.base_agent import BaseAgent
from .agents.assistant_agent import AssistantAgent
from .agents.user_proxy_agent import UserProxyAgent
from .tools.tool_registry import ToolRegistry
from .tools.basic_tools import register_basic_tools
from .mcp.mcp_client import MCPManager

class AgentFramework:
    """
    Main framework class for the Autogen Agents Framework.
    This class manages agents, tools, and MCP servers.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the agent framework.
        
        Args:
            config_path: Path to a JSON configuration file. If None, will try to load from environment variables.
        """
        self.config_manager = ConfigManager(config_path)
        self.tool_registry = ToolRegistry()
        self.mcp_manager = MCPManager()
        self.agents: Dict[str, BaseAgent] = {}
        
        # Register basic tools
        register_basic_tools(self.tool_registry)
    
    def create_agent(
        self,
        agent_type: str,
        name: str,
        description: str,
        system_message: str,
        llm_config: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        human_input_mode: str = "NEVER",
        code_execution_config: Optional[Dict[str, Any]] = None,
    ) -> BaseAgent:
        """
        Create a new agent.
        
        Args:
            agent_type: Type of agent ("assistant" or "user_proxy")
            name: Name of the agent
            description: Description of the agent
            system_message: System message for the agent
            llm_config: LLM configuration for the agent
            tools: List of tools available to the agent
            human_input_mode: Mode for human input ("ALWAYS", "NEVER", or "TERMINATE")
            code_execution_config: Configuration for code execution (only for user_proxy)
            
        Returns:
            The created agent
        """
        # Use Azure OpenAI configuration if llm_config is not provided
        if llm_config is None and agent_type != "user_proxy":
            azure_config = self.config_manager.get_azure_openai_config()
            llm_config = create_llm_config(azure_config)
        
        # Get tools from registry if not provided
        if tools is None:
            tools = self.tool_registry.get_tool_dicts()
        
        # Add MCP tools
        mcp_tools = self.mcp_manager.create_autogen_tools()
        if mcp_tools:
            tools = tools + mcp_tools
        
        # Create the agent based on type
        if agent_type == "assistant":
            agent = AssistantAgent(
                name=name,
                description=description,
                system_message=system_message,
                llm_config=llm_config,
                tools=tools,
                human_input_mode=human_input_mode,
            )
        elif agent_type == "user_proxy":
            agent = UserProxyAgent(
                name=name,
                description=description,
                system_message=system_message,
                llm_config=llm_config,
                tools=tools,
                human_input_mode=human_input_mode,
                code_execution_config=code_execution_config,
            )
        else:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        # Register the agent
        self.agents[name] = agent
        return agent
    
    def get_agent(self, name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.
        
        Args:
            name: Agent name
            
        Returns:
            The agent, or None if not found
        """
        return self.agents.get(name)
    
    def register_tool(
        self,
        name: str,
        description: str,
        function: Any,
        parameters: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Register a new tool.
        
        Args:
            name: Tool name
            description: Tool description
            function: Function implementing the tool
            parameters: Tool parameters schema
        """
        self.tool_registry.register_function(
            name=name,
            description=description,
            function=function,
            parameters=parameters
        )
    
    def register_mcp_server(
        self,
        name: str,
        endpoint: str,
        api_key: Optional[str] = None
    ) -> None:
        """
        Register an MCP server.
        
        Args:
            name: MCP server name
            endpoint: MCP server endpoint URL
            api_key: MCP server API key if required
        """
        config = MCPServerConfig(
            name=name,
            endpoint=endpoint,
            api_key=api_key
        )
        self.mcp_manager.register_client(config)
    
    def start_conversation(
        self,
        sender: Union[str, BaseAgent],
        receiver: Union[str, BaseAgent],
        message: str
    ) -> None:
        """
        Start a conversation between two agents.
        
        Args:
            sender: Sender agent name or agent object
            receiver: Receiver agent name or agent object
            message: Initial message
        """
        # Get agent objects if names were provided
        if isinstance(sender, str):
            sender = self.get_agent(sender)
            if sender is None:
                raise ValueError(f"Agent not found: {sender}")
        
        if isinstance(receiver, str):
            receiver = self.get_agent(receiver)
            if receiver is None:
                raise ValueError(f"Agent not found: {receiver}")
        
        # Start the conversation
        sender.initiate_chat(receiver, message)
    
    def save_config(self, config_path: str) -> None:
        """
        Save the current configuration to a file.
        
        Args:
            config_path: Path to save the configuration file
        """
        self.config_manager.save_config(config_path)
