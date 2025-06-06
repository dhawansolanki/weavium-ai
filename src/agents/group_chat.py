"""
Group chat implementation for the Autogen Agents Framework.
"""

import autogen
from typing import Dict, Any, List, Optional, Union, Callable
from .base_agent import BaseAgent

class GroupChat:
    """
    Group chat for multiple agents to collaborate.
    This class manages conversations between multiple agents in a group setting.
    """
    
    def __init__(
        self,
        agents: List[Union[BaseAgent, autogen.ConversableAgent]],
        messages: Optional[List[Dict[str, Any]]] = None,
        max_round: int = 10,
        speaker_selection_method: str = "auto",
        allow_repeat_speaker: bool = True,
    ):
        """
        Initialize a group chat.
        
        Args:
            agents: List of agents participating in the group chat
            messages: Initial messages in the chat
            max_round: Maximum number of conversation rounds
            speaker_selection_method: Method for selecting the next speaker ("auto", "round_robin", or "random")
            allow_repeat_speaker: Whether to allow the same speaker to speak multiple times in a row
        """
        self.agents = []
        self.autogen_agents = []
        
        # Process agents to ensure they are all autogen.ConversableAgent instances
        for agent in agents:
            if isinstance(agent, BaseAgent):
                self.agents.append(agent)
                self.autogen_agents.append(agent.agent)
            else:
                self.autogen_agents.append(agent)
        
        # Create the autogen group chat
        self.group_chat = autogen.GroupChat(
            agents=self.autogen_agents,
            messages=messages or [],
            max_round=max_round,
            speaker_selection_method=speaker_selection_method,
            allow_repeat_speaker=allow_repeat_speaker,
        )
    
    def reset(self):
        """Reset the group chat."""
        self.group_chat.reset()
    
    def append_message(self, message: Dict[str, Any]):
        """
        Append a message to the group chat.
        
        Args:
            message: Message to append
        """
        self.group_chat.append_message(message)
    
    def select_speaker(self, last_speaker: Optional[autogen.ConversableAgent] = None) -> autogen.ConversableAgent:
        """
        Select the next speaker.
        
        Args:
            last_speaker: Last speaker in the conversation
            
        Returns:
            Next speaker
        """
        return self.group_chat.select_speaker(last_speaker)
    
    def messages_to_str(self) -> str:
        """
        Convert all messages to a string.
        
        Returns:
            String representation of all messages
        """
        return self.group_chat.messages_to_str()
    
    def get_agent_by_name(self, name: str) -> Optional[BaseAgent]:
        """
        Get an agent by name.
        
        Args:
            name: Agent name
            
        Returns:
            The agent, or None if not found
        """
        for agent in self.agents:
            if agent.name == name:
                return agent
        return None
    
    def initiate_chat(self, manager: Union[BaseAgent, autogen.ConversableAgent], message: str):
        """
        Initiate a group chat.
        
        Args:
            manager: Agent managing the conversation
            message: Initial message
        """
        manager_agent = manager.agent if isinstance(manager, BaseAgent) else manager
        manager_agent.initiate_chat(self.group_chat, message=message)


class GroupChatManager:
    """
    Manager for group chats.
    This class creates and manages group chats between multiple agents.
    """
    
    def __init__(self):
        """Initialize a group chat manager."""
        self.group_chats: Dict[str, GroupChat] = {}
    
    def create_group_chat(
        self,
        name: str,
        agents: List[Union[BaseAgent, autogen.ConversableAgent]],
        max_round: int = 10,
        speaker_selection_method: str = "auto",
        allow_repeat_speaker: bool = True,
    ) -> GroupChat:
        """
        Create a new group chat.
        
        Args:
            name: Name of the group chat
            agents: List of agents participating in the group chat
            max_round: Maximum number of conversation rounds
            speaker_selection_method: Method for selecting the next speaker
            allow_repeat_speaker: Whether to allow the same speaker to speak multiple times in a row
            
        Returns:
            The created group chat
        """
        group_chat = GroupChat(
            agents=agents,
            max_round=max_round,
            speaker_selection_method=speaker_selection_method,
            allow_repeat_speaker=allow_repeat_speaker,
        )
        self.group_chats[name] = group_chat
        return group_chat
    
    def get_group_chat(self, name: str) -> Optional[GroupChat]:
        """
        Get a group chat by name.
        
        Args:
            name: Group chat name
            
        Returns:
            The group chat, or None if not found
        """
        return self.group_chats.get(name)
    
    def initiate_chat(
        self,
        group_chat_name: str,
        manager: Union[BaseAgent, autogen.ConversableAgent],
        message: str
    ):
        """
        Initiate a chat in a group chat.
        
        Args:
            group_chat_name: Name of the group chat
            manager: Agent managing the conversation
            message: Initial message
        """
        group_chat = self.get_group_chat(group_chat_name)
        if group_chat is None:
            raise ValueError(f"Group chat not found: {group_chat_name}")
        
        group_chat.initiate_chat(manager, message)
