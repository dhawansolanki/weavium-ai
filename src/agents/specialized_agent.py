"""
Specialized agent implementation for the Autogen Agents Framework.
"""

from typing import Dict, Any, List, Optional, Callable
from .base_agent import BaseAgent
from ..config.config_manager import AgentConfig

class SpecializedAgent(BaseAgent):
    """
    Specialized agent that can be customized for specific domains or tasks.
    This agent can be configured with domain-specific knowledge and capabilities.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        system_message: str,
        llm_config: Dict[str, Any],
        domain: str,
        domain_knowledge: Dict[str, Any],
        tools: Optional[List[Dict[str, Any]]] = None,
        is_termination_msg: Optional[Callable[[Dict[str, Any]], bool]] = None,
        human_input_mode: str = "NEVER",
    ):
        """
        Initialize a specialized agent.
        
        Args:
            name: Name of the agent
            description: Description of the agent
            system_message: System message for the agent
            llm_config: LLM configuration for the agent
            domain: Domain of specialization (e.g., "finance", "healthcare", "coding")
            domain_knowledge: Domain-specific knowledge and configuration
            tools: List of tools available to the agent
            is_termination_msg: Function to determine if a message should terminate the conversation
            human_input_mode: Mode for human input ("ALWAYS", "NEVER", or "TERMINATE")
        """
        self.domain = domain
        self.domain_knowledge = domain_knowledge
        
        # Enhance system message with domain-specific instructions
        enhanced_system_message = self._enhance_system_message(system_message)
        
        super().__init__(
            name=name,
            description=description,
            system_message=enhanced_system_message,
            llm_config=llm_config,
            tools=tools,
            is_termination_msg=is_termination_msg,
            human_input_mode=human_input_mode,
        )
    
    def _enhance_system_message(self, system_message: str) -> str:
        """
        Enhance the system message with domain-specific instructions.
        
        Args:
            system_message: Original system message
            
        Returns:
            Enhanced system message
        """
        domain_instructions = self.domain_knowledge.get("instructions", "")
        domain_guidelines = self.domain_knowledge.get("guidelines", [])
        domain_examples = self.domain_knowledge.get("examples", [])
        
        # Build enhanced system message
        enhanced_message = f"{system_message}\n\n"
        enhanced_message += f"Domain of specialization: {self.domain}\n\n"
        
        if domain_instructions:
            enhanced_message += f"Domain-specific instructions:\n{domain_instructions}\n\n"
        
        if domain_guidelines:
            enhanced_message += "Domain-specific guidelines:\n"
            for i, guideline in enumerate(domain_guidelines, 1):
                enhanced_message += f"{i}. {guideline}\n"
            enhanced_message += "\n"
        
        if domain_examples:
            enhanced_message += "Domain-specific examples:\n"
            for i, example in enumerate(domain_examples, 1):
                enhanced_message += f"Example {i}:\n"
                if isinstance(example, dict):
                    for key, value in example.items():
                        enhanced_message += f"- {key}: {value}\n"
                else:
                    enhanced_message += f"{example}\n"
                enhanced_message += "\n"
        
        return enhanced_message
    
    @classmethod
    def from_config(cls, config: AgentConfig, domain: str, domain_knowledge: Dict[str, Any], tools: Optional[List[Dict[str, Any]]] = None):
        """
        Create a specialized agent from a configuration object.
        
        Args:
            config: Agent configuration
            domain: Domain of specialization
            domain_knowledge: Domain-specific knowledge and configuration
            tools: List of tools available to the agent
            
        Returns:
            A new SpecializedAgent instance
        """
        return cls(
            name=config.name,
            description=config.description,
            system_message=config.system_message,
            llm_config=config.llm_config,
            domain=domain,
            domain_knowledge=domain_knowledge,
            tools=tools,
        )
