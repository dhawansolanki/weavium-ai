"""
Assistant agent implementation for the Autogen Agents Framework.
"""

import autogen
from typing import Dict, Any, List, Optional, Callable
from .base_agent import BaseAgent
from ..config.config_manager import AgentConfig

class AssistantAgent(BaseAgent):
    """
    Assistant agent that can help with various tasks.
    This agent is designed to be helpful, harmless, and honest.
    """
    
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
        Initialize an assistant agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            system_message: System message for the agent
            llm_config: LLM configuration for the agent
            tools: List of tools available to the agent
            is_termination_msg: Function to determine if a message should terminate the conversation
            human_input_mode: Mode for human input ("ALWAYS", "NEVER", or "TERMINATE")
        """
        super().__init__(
            name=name,
            description=description,
            system_message=system_message,
            llm_config=llm_config,
            tools=tools,
            is_termination_msg=is_termination_msg,
            human_input_mode=human_input_mode,
        )
    
    def _create_agent(self) -> autogen.AssistantAgent:
        """Create the underlying Autogen assistant agent."""
        return autogen.AssistantAgent(
            name=self.name,
            system_message=self.system_message,
            llm_config=self.llm_config,
            human_input_mode=self.human_input_mode,
            function_map={tool["name"]: tool["function"] for tool in self.tools if "function" in tool},
            is_termination_msg=self.is_termination_msg,
        )
    
    @classmethod
    def from_config(cls, config: AgentConfig, tools: Optional[List[Dict[str, Any]]] = None):
        """
        Create an assistant agent from a configuration object.
        
        Args:
            config: Agent configuration
            tools: List of tools available to the agent
            
        Returns:
            A new AssistantAgent instance
        """
        return cls(
            name=config.name,
            description=config.description,
            system_message=config.system_message,
            llm_config=config.llm_config,
            tools=tools,
        )
