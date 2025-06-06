"""
Tool registry for the Autogen Agents Framework.
"""

from typing import Dict, Any, List, Callable, Optional
from ..config.config_manager import ToolConfig

class Tool:
    """Representation of a tool that can be used by agents."""
    
    def __init__(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a tool.
        
        Args:
            name: Tool name
            description: Tool description
            function: Function implementing the tool
            parameters: Tool parameters schema
        """
        self.name = name
        self.description = description
        self.function = function
        self.parameters = parameters or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the tool to a dictionary representation.
        
        Returns:
            Dictionary representation of the tool
        """
        return {
            "name": self.name,
            "description": self.description,
            "function": self.function,
            "parameters": self.parameters
        }
    
    @classmethod
    def from_config(cls, config: ToolConfig, function: Callable):
        """
        Create a tool from a configuration object.
        
        Args:
            config: Tool configuration
            function: Function implementing the tool
            
        Returns:
            A new Tool instance
        """
        return cls(
            name=config.name,
            description=config.description,
            function=function,
            parameters=config.parameters
        )


class ToolRegistry:
    """Registry for tools that can be used by agents."""
    
    def __init__(self):
        """Initialize a tool registry."""
        self.tools: Dict[str, Tool] = {}
    
    def register_tool(self, tool: Tool) -> None:
        """
        Register a tool.
        
        Args:
            tool: Tool to register
        """
        self.tools[tool.name] = tool
    
    def register_function(
        self,
        name: str,
        description: str,
        function: Callable,
        parameters: Optional[Dict[str, Any]] = None
    ) -> Tool:
        """
        Register a function as a tool.
        
        Args:
            name: Tool name
            description: Tool description
            function: Function implementing the tool
            parameters: Tool parameters schema
            
        Returns:
            The registered tool
        """
        tool = Tool(name, description, function, parameters)
        self.register_tool(tool)
        return tool
    
    def get_tool(self, name: str) -> Optional[Tool]:
        """
        Get a tool by name.
        
        Args:
            name: Tool name
            
        Returns:
            The tool, or None if not found
        """
        return self.tools.get(name)
    
    def get_all_tools(self) -> List[Tool]:
        """
        Get all registered tools.
        
        Returns:
            List of all tools
        """
        return list(self.tools.values())
    
    def get_tool_dicts(self) -> List[Dict[str, Any]]:
        """
        Get dictionary representations of all registered tools.
        
        Returns:
            List of tool dictionaries
        """
        return [tool.to_dict() for tool in self.tools.values()]
