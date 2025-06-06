# Autogen Agents Framework Documentation (Part 3)

## Agent Types

The Autogen Agents Framework supports several types of agents, each with specific roles and capabilities.

### Assistant Agent

Assistant agents are AI-powered agents that can respond to queries, perform tasks, and engage in conversations.

#### Features

- **LLM Integration**: Powered by language models like GPT-4
- **Tool Usage**: Can use registered tools to perform tasks
- **Memory Access**: Can access and update the memory system
- **Conversation Management**: Can participate in one-on-one and group conversations

#### Configuration

```python
assistant = framework.create_agent(
    agent_type="assistant",
    name="ResearchAssistant",
    description="Research specialist that finds and analyzes information",
    system_message="You are a research specialist. Your role is to find and analyze information.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": "your_api_key"
            }
        ]
    },
    tools=framework.tool_registry.get_all_tools()
)
```

### User Proxy Agent

User proxy agents represent human users in the system, facilitating interaction between humans and AI agents.

#### Features

- **Human Input Handling**: Can collect and process input from human users
- **Code Execution**: Can execute code on behalf of the user (if configured)
- **Tool Usage**: Can use tools to perform tasks
- **Conversation Initiation**: Can initiate conversations with other agents

#### Configuration

```python
user_proxy = framework.create_agent(
    agent_type="user_proxy",
    name="UserProxy",
    description="A proxy for the human user",
    system_message="You are a proxy for the human user. You help facilitate the conversation.",
    human_input_mode="TERMINATE",  # Options: ALWAYS, TERMINATE, NEVER
    code_execution_config={
        "work_dir": "./workspace",
        "use_docker": False
    }
)
```

### Specialized Agent

Specialized agents are domain-specific agents with enhanced capabilities in particular areas.

#### Features

- **Domain Knowledge**: Enhanced with specific domain knowledge
- **Specialized Instructions**: Tailored instructions for their domain
- **Guidelines**: Domain-specific guidelines for responses
- **Examples**: Examples of domain-specific interactions

#### Implementation

While the framework's `create_agent` method doesn't directly support the "specialized" agent type, you can create specialized agents by enhancing assistant agents with domain-specific system messages:

```python
# Define domain knowledge
coding_knowledge = {
    "instructions": "Analyze code, suggest improvements, and write clean, efficient code.",
    "guidelines": [
        "Always consider code readability and maintainability",
        "Follow language-specific best practices",
        "Include comments for complex logic",
        "Consider edge cases and error handling"
    ],
    "examples": [
        "Refactoring a function to be more efficient",
        "Debugging a complex issue",
        "Implementing a new feature with clean code"
    ]
}

# Create specialized system message
coder_system_message = f"You are a coding specialist. Your role is to write and review code.\n\n"
coder_system_message += f"Instructions: {coding_knowledge['instructions']}\n\n"
coder_system_message += "Guidelines:\n"
for guideline in coding_knowledge['guidelines']:
    coder_system_message += f"- {guideline}\n"
coder_system_message += "\nExamples:\n"
for example in coding_knowledge['examples']:
    coder_system_message += f"- {example}\n"

# Create specialized agent
coder = framework.create_agent(
    agent_type="assistant",
    name="Coder",
    description="Coding specialist that writes clean and efficient code",
    system_message=coder_system_message,
    tools=framework.tool_registry.get_all_tools()
)
```

### Group Chat Manager

Group chat managers orchestrate conversations between multiple agents.

#### Features

- **Conversation Coordination**: Manages the flow of conversation
- **Agent Selection**: Determines which agent should respond next
- **Topic Management**: Keeps the conversation on topic
- **Conflict Resolution**: Resolves conflicts between agents

#### Implementation

Group chat managers are implemented using Autogen's `GroupChatManager`:

```python
from autogen.agentchat.groupchat import GroupChat, GroupChatManager

# Create a group chat
group_chat = GroupChat(
    agents=[researcher, coder, planner, user_proxy],
    messages=[],
    max_round=10
)

# Create a group chat manager
manager = GroupChatManager(
    groupchat=group_chat,
    name="GroupChatManager",
    description="Manager for the group chat",
    system_message=(
        "You are the manager of this group chat. Your role is to facilitate discussion "
        "between the specialized agents and the user. Make sure each agent contributes "
        "according to their expertise."
    )
)
```

## Memory System

The memory system is a core component of the Autogen Agents Framework, enabling agents to retain information across conversations.

### Memory Manager

The `MemoryManager` class provides the interface for storing and retrieving memories.

#### Key Methods

- **store_memory**: Store a memory for an agent
- **retrieve_memories**: Retrieve memories for an agent
- **update_memory**: Update an existing memory
- **delete_memory**: Delete a memory
- **search_memories**: Search memories by content
- **create_conversation**: Create a new conversation
- **add_message**: Add a message to a conversation
- **get_conversation_history**: Get the history of a conversation
- **get_recent_conversations**: Get recent conversations

#### Memory Types

The framework supports different types of memories:

- **Facts**: Factual information about entities and concepts
- **Skills**: Agent capabilities and expertise
- **Experiences**: Past interactions and outcomes
- **Preferences**: User preferences and settings
- **Relationships**: Connections between entities

#### Memory Storage

Memories are stored in a SQLite database with the following schema:

- **memories**: Stores agent memories
  - id: Unique identifier
  - agent_name: Name of the agent
  - memory_type: Type of memory
  - content: Memory content (JSON or string)
  - created_at: Creation timestamp
  - updated_at: Update timestamp

- **conversations**: Stores conversation metadata
  - id: Unique identifier
  - conversation_id: Conversation identifier
  - title: Conversation title
  - created_at: Creation timestamp
  - updated_at: Update timestamp

- **messages**: Stores conversation messages
  - id: Unique identifier
  - conversation_id: Conversation identifier
  - sender: Message sender
  - receiver: Message receiver
  - content: Message content
  - timestamp: Message timestamp

### Memory Usage Examples

#### Storing Facts

```python
memory_manager.store_memory(
    agent_name="AssistantAgent",
    memory_type="fact",
    content={
        "subject": "user",
        "predicate": "likes",
        "object": "Python programming"
    }
)
```

#### Storing Skills

```python
memory_manager.store_memory(
    agent_name="AssistantAgent",
    memory_type="skill",
    content={
        "skill_name": "coding",
        "proficiency": "expert",
        "description": "Ability to write clean, efficient Python code"
    }
)
```

#### Storing Experiences

```python
memory_manager.store_memory(
    agent_name="AssistantAgent",
    memory_type="experience",
    content={
        "event": "helped user debug code",
        "outcome": "successful",
        "learning": "User prefers detailed explanations"
    }
)
```

#### Retrieving Memories

```python
# Retrieve all memories for an agent
all_memories = memory_manager.retrieve_memories("AssistantAgent")

# Retrieve specific memory types
fact_memories = memory_manager.retrieve_memories("AssistantAgent", "fact")
```

#### Searching Memories

```python
# Search for memories containing "Python"
python_memories = memory_manager.search_memories("Python")
```

#### Managing Conversations

```python
# Create a conversation
conversation_id = str(uuid.uuid4())
memory_manager.create_conversation(conversation_id, "Python Debugging Session")

# Add messages
memory_manager.add_message(
    conversation_id=conversation_id,
    sender="User",
    receiver="AssistantAgent",
    content="I'm having trouble with my Python code."
)

memory_manager.add_message(
    conversation_id=conversation_id,
    sender="AssistantAgent",
    receiver="User",
    content="I'd be happy to help. Can you share the code and the error message?"
)

# Get conversation history
history = memory_manager.get_conversation_history(conversation_id)
```

## MCP Integration

The Autogen Agents Framework includes built-in support for Model Context Protocol (MCP) servers, particularly Context7, which enables agents to access external knowledge and tools.

### Context7 Integration

[Context7](https://context7.com) is an MCP server that provides access to documentation and knowledge bases for various libraries and frameworks.

#### Context7Client

The `Context7Client` class provides methods for interacting with the Context7 API:

- **get_library_docs**: Get documentation for a library
- **resolve_library_id**: Resolve a library name to a Context7-compatible ID
- **search_libraries**: Search for libraries

#### Configuration

```python
from autogen_agents_framework.integrations.context7 import Context7Client

context7_client = Context7Client(
    api_key="your_context7_api_key",
    api_url="https://api.context7.com/v1"
)
```

#### Usage Examples

```python
# Resolve a library name to a Context7-compatible ID
library_id = context7_client.resolve_library_id("next.js")

# Get documentation for a library
docs = context7_client.get_library_docs("/vercel/next.js")

# Create Context7 tools for agents
context7_tools = context7_client.create_tools()
```

### Other MCP Servers

The framework is designed to be extensible, allowing integration with other MCP servers:

```python
from autogen_agents_framework.integrations.mcp import MCPClient

class CustomMCPClient(MCPClient):
    def __init__(self, api_key, api_url):
        super().__init__(api_key, api_url)
    
    def get_resource(self, resource_id):
        # Implementation for getting a resource
        pass
    
    def create_tools(self):
        # Implementation for creating tools
        pass
```

## Tools and Extensions

The Autogen Agents Framework includes a tool registry system that allows agents to discover and use various tools.

### Tool Registry

The `ToolRegistry` class provides methods for registering and retrieving tools:

- **register_tool**: Register a tool with the registry
- **get_tool**: Get a tool by name
- **get_all_tools**: Get all registered tools
- **get_tools_by_category**: Get tools by category

#### Tool Structure

Tools follow the Autogen tool structure:

```python
tool = {
    "name": "calculator",
    "description": "A calculator tool for performing arithmetic operations",
    "parameters": {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The arithmetic expression to evaluate"
            }
        },
        "required": ["expression"]
    },
    "function": calculator_function
}
```

#### Registering Tools

```python
# Register a tool
framework.tool_registry.register_tool(
    name="calculator",
    description="A calculator tool for performing arithmetic operations",
    parameters={
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The arithmetic expression to evaluate"
            }
        },
        "required": ["expression"]
    },
    function=calculator_function,
    category="math"
)
```

#### Using Tools

```python
# Get all tools
all_tools = framework.tool_registry.get_all_tools()

# Get tools by category
math_tools = framework.tool_registry.get_tools_by_category("math")

# Create an agent with tools
assistant = framework.create_agent(
    agent_type="assistant",
    name="MathAssistant",
    description="A math assistant",
    system_message="You are a math assistant.",
    tools=math_tools
)
```

### Built-in Tools

The framework includes several built-in tools:

- **Calculator**: Perform arithmetic operations
- **WebSearch**: Search the web for information
- **FileReader**: Read files from the filesystem
- **FileWriter**: Write files to the filesystem
- **CodeExecutor**: Execute code in various languages

### Custom Tools

You can create custom tools by defining a function and registering it with the tool registry:

```python
def weather_tool(location):
    """Get the current weather for a location."""
    # Implementation
    return {"temperature": 72, "conditions": "sunny"}

framework.tool_registry.register_tool(
    name="weather",
    description="Get the current weather for a location",
    parameters={
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location to get weather for"
            }
        },
        "required": ["location"]
    },
    function=weather_tool,
    category="weather"
)
```
