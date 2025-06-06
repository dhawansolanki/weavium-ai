"""
Base agent implementation for the Autogen Agents Framework.
"""

import autogen
from typing import Dict, Any, List, Optional, Union, Callable
from ..config.config_manager import AgentConfig

class BaseAgent:
    """Base class for all agents in the framework."""
    
    def __init__(
        self,
        name: str,
        description: str,
        system_message: str,
        llm_config: Dict[str, Any],
        tools: Optional[List[Dict[str, Any]]] = None,
        is_termination_msg: Optional[Callable[[Dict[str, Any]], bool]] = None,
        human_input_mode: str = "NEVER",
    ):
        """
        Initialize a base agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            system_message: System message for the agent
            llm_config: LLM configuration for the agent
            tools: List of tools available to the agent
            is_termination_msg: Function to determine if a message should terminate the conversation
            human_input_mode: Mode for human input ("ALWAYS", "NEVER", or "TERMINATE")
        """
        self.name = name
        self.description = description
        self.system_message = system_message
        self.llm_config = llm_config
        self.tools = tools or []
        self.is_termination_msg = is_termination_msg
        self.human_input_mode = human_input_mode
        self.agent = self._create_agent()
    
    def _create_agent(self) -> autogen.ConversableAgent:
        """Create the underlying Autogen agent."""
        return autogen.ConversableAgent(
            name=self.name,
            system_message=self.system_message,
            llm_config=self.llm_config,
            human_input_mode=self.human_input_mode,
            function_map={tool["name"]: tool["function"] for tool in self.tools if "function" in tool},
            is_termination_msg=self.is_termination_msg,
        )
    
    def register_tool(self, tool_name: str, tool_function: Callable, tool_description: str):
        """
        Register a new tool with the agent.
        
        Args:
            tool_name: Name of the tool
            tool_function: Function implementing the tool
            tool_description: Description of the tool
        """
        tool = {
            "name": tool_name,
            "function": tool_function,
            "description": tool_description
        }
        self.tools.append(tool)
        self.agent.register_function(function=tool_function, name=tool_name, description=tool_description)
    
    def send_message(self, message: str, recipient: Union[autogen.ConversableAgent, 'BaseAgent']):
        """
        Send a message to another agent.
        
        Args:
            message: Message to send
            recipient: Agent to send the message to
        """
        if isinstance(recipient, BaseAgent):
            recipient = recipient.agent
        self.agent.send(message, recipient)
    
    def initiate_chat(self, recipient: Union[autogen.ConversableAgent, 'BaseAgent'], message: str):
        """
        Initiate a chat with another agent.
        
        Args:
            recipient: Agent to chat with
            message: Initial message
        """
        if isinstance(recipient, BaseAgent):
            recipient = recipient.agent
        self.agent.initiate_chat(recipient, message=message)
    
    @classmethod
    def from_config(cls, config: AgentConfig, tools: Optional[List[Dict[str, Any]]] = None):
        """
        Create an agent from a configuration object.
        
        Args:
            config: Agent configuration
            tools: List of tools available to the agent
            
        Returns:
            A new BaseAgent instance
        """
        return cls(
            name=config.name,
            description=config.description,
            system_message=config.system_message,
            llm_config=config.llm_config,
            tools=tools,
        )
