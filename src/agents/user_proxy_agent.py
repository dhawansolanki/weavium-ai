"""
User proxy agent implementation for the Autogen Agents Framework.
"""

import autogen
from typing import Dict, Any, List, Optional, Callable, Union
from .base_agent import BaseAgent
from ..config.config_manager import AgentConfig

class UserProxyAgent(BaseAgent):
    """
    User proxy agent that represents a human user in the agent system.
    This agent can execute code, provide human feedback, and interact with other agents.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        system_message: str,
        llm_config: Optional[Dict[str, Any]] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        is_termination_msg: Optional[Callable[[Dict[str, Any]], bool]] = None,
        human_input_mode: str = "ALWAYS",
        code_execution_config: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a user proxy agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            system_message: System message for the agent
            llm_config: LLM configuration for the agent (can be None for user proxy)
            tools: List of tools available to the agent
            is_termination_msg: Function to determine if a message should terminate the conversation
            human_input_mode: Mode for human input ("ALWAYS", "NEVER", or "TERMINATE")
            code_execution_config: Configuration for code execution
        """
        self.code_execution_config = code_execution_config or {"use_docker": False}
        super().__init__(
            name=name,
            description=description,
            system_message=system_message,
            llm_config=llm_config or {},
            tools=tools,
            is_termination_msg=is_termination_msg,
            human_input_mode=human_input_mode,
        )
    
    def _create_agent(self) -> autogen.UserProxyAgent:
        """Create the underlying Autogen user proxy agent."""
        return autogen.UserProxyAgent(
            name=self.name,
            system_message=self.system_message,
            human_input_mode=self.human_input_mode,
            function_map={tool["name"]: tool["function"] for tool in self.tools if "function" in tool},
            code_execution_config=self.code_execution_config,
            llm_config=self.llm_config if self.llm_config else None,
            is_termination_msg=self.is_termination_msg,
        )
    
    def execute_code(self, code: str, lang: str = "python") -> str:
        """
        Execute code through the user proxy agent.
        
        Args:
            code: Code to execute
            lang: Programming language of the code
            
        Returns:
            Execution result
        """
        return self.agent.execute_code(code, lang=lang)
    
    def get_human_feedback(self, prompt: str = "") -> str:
        """
        Get feedback from the human user.
        
        Args:
            prompt: Prompt to show to the user
            
        Returns:
            User feedback
        """
        return self.agent.get_human_feedback(prompt)
    
    @classmethod
    def from_config(cls, config: AgentConfig, tools: Optional[List[Dict[str, Any]]] = None, code_execution_config: Optional[Dict[str, Any]] = None):
        """
        Create a user proxy agent from a configuration object.
        
        Args:
            config: Agent configuration
            tools: List of tools available to the agent
            code_execution_config: Configuration for code execution
            
        Returns:
            A new UserProxyAgent instance
        """
        return cls(
            name=config.name,
            description=config.description,
            system_message=config.system_message,
            llm_config=config.llm_config,
            tools=tools,
            code_execution_config=code_execution_config,
        )
