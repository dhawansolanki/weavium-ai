# Autogen Agents Framework Documentation

## Table of Contents
1. [Introduction](#introduction)
2. [Framework Architecture](#framework-architecture)
3. [Key Features](#key-features)
4. [Use Cases](#use-cases)
5. [Getting Started](#getting-started)
6. [Configuration](#configuration)
7. [Agent Types](#agent-types)
8. [Memory System](#memory-system)
9. [MCP Integration](#mcp-integration)
10. [Tools and Extensions](#tools-and-extensions)
11. [Command Line Interface](#command-line-interface)
12. [Examples](#examples)
13. [Testing](#testing)
14. [Deployment](#deployment)
15. [Best Practices](#best-practices)
16. [Troubleshooting](#troubleshooting)
17. [Future Roadmap](#future-roadmap)
18. [Contributing](#contributing)
19. [License](#license)

## Introduction

The Autogen Agents Framework is a powerful, extensible system built on top of Microsoft's Autogen library, designed to simplify the creation, management, and orchestration of AI agents. This framework enables developers to build sophisticated multi-agent systems that can collaborate, maintain memory across conversations, integrate with external tools and knowledge bases, and solve complex tasks through agent cooperation.

### What is Autogen?

[Autogen](https://github.com/microsoft/autogen) is Microsoft's open-source framework for building LLM applications with multi-agent conversations. It provides the foundation for creating conversable agents that can interact with each other and with humans. Autogen enables developers to define different agent roles, customize their behaviors, and orchestrate their interactions.

### What Our Framework Adds

The Autogen Agents Framework extends the base Autogen capabilities with:

1. **Simplified Agent Creation**: A streamlined API for creating and configuring different types of agents
2. **Persistent Memory**: A robust memory system that allows agents to retain information across conversations
3. **MCP Integration**: Built-in support for Model Context Protocol (MCP) servers like Context7
4. **Tool Registry**: A centralized system for registering, managing, and sharing tools between agents
5. **Standardized Logging**: Comprehensive logging utilities for debugging and monitoring agent interactions
6. **CLI Support**: Command-line interface for creating agents and running conversations
7. **Specialized Agents**: Support for domain-specific agents with enhanced capabilities
8. **Group Chat Management**: Utilities for creating and managing multi-agent conversations
9. **Environment Management**: Tools for setting up and configuring the framework environment

This framework is designed to be accessible to developers of all skill levels while providing the flexibility and power needed for advanced use cases.

## Framework Architecture

The Autogen Agents Framework follows a modular, layered architecture that promotes separation of concerns and extensibility.

### Core Components

1. **AgentFramework**: The central class that coordinates all framework components and provides the main API for creating and managing agents.

2. **Agents**: Different types of agents that can be created and customized:
   - **BaseAgent**: Abstract base class for all agents
   - **AssistantAgent**: AI-powered agent that can respond to queries and perform tasks
   - **UserProxyAgent**: Agent that represents a human user in the system
   - **SpecializedAgent**: Domain-specific agents with enhanced capabilities

3. **Memory System**:
   - **MemoryManager**: Manages persistent storage of agent memories and conversation history
   - **Memory Types**: Different types of memories (facts, skills, experiences, etc.)

4. **Tool System**:
   - **ToolRegistry**: Central registry for managing available tools
   - **Tool**: Base class for creating custom tools
   - **Built-in Tools**: Pre-configured tools for common tasks

5. **MCP Integration**:
   - **MCPClient**: Client for connecting to MCP servers
   - **Context7Client**: Specialized client for the Context7 MCP server

6. **Utilities**:
   - **LoggingUtils**: Utilities for configuring and managing logs
   - **ConfigUtils**: Utilities for loading and managing configuration
   - **EnvUtils**: Utilities for environment setup and management

### System Flow

1. **Initialization**: The framework is initialized with configuration parameters
2. **Agent Creation**: Agents are created and configured based on their roles
3. **Tool Registration**: Tools are registered with the framework
4. **Conversation**: Agents communicate with each other and with humans
5. **Memory Storage**: Important information is stored in the memory system
6. **Tool Usage**: Agents use tools to perform tasks and access external resources

This architecture allows for flexible composition of agents, tools, and memories to create complex multi-agent systems tailored to specific use cases.

## Key Features

### Multi-Agent Collaboration

The framework enables the creation of systems where multiple agents with different roles and capabilities can work together to solve complex problems. This collaboration is facilitated through:

- **Group Chat**: Agents can participate in group conversations
- **Role-Based Interactions**: Each agent has a specific role and expertise
- **Orchestration**: Group chat managers can coordinate agent interactions

### Persistent Memory

One of the most powerful features of the framework is its robust memory system that allows agents to:

- **Store Facts**: Retain factual information about entities and concepts
- **Remember Skills**: Keep track of their capabilities and expertise
- **Record Experiences**: Remember past interactions and outcomes
- **Maintain Conversation History**: Preserve the context of conversations

This memory system uses a SQLite database for persistence, ensuring that information is retained across sessions and restarts.

### MCP Integration

The framework includes built-in support for Model Context Protocol (MCP) servers, particularly Context7, which enables:

- **External Knowledge Access**: Agents can access documentation and knowledge bases
- **Tool Extension**: MCP servers can provide additional tools and capabilities
- **Specialized Expertise**: Agents can leverage domain-specific knowledge

### Tool Registry

The tool registry provides a centralized system for:

- **Tool Registration**: Register custom tools with the framework
- **Tool Discovery**: Agents can discover available tools
- **Tool Sharing**: Tools can be shared between agents
- **Tool Configuration**: Tools can be configured with custom parameters

### Logging and Monitoring

Comprehensive logging utilities enable:

- **Debugging**: Detailed logs for troubleshooting issues
- **Monitoring**: Track agent interactions and performance
- **Auditing**: Review agent decisions and actions
- **Analysis**: Analyze conversation patterns and outcomes

### Command Line Interface

The framework includes a powerful CLI that allows users to:

- **Create Agents**: Create and configure agents from the command line
- **Run Conversations**: Initiate and manage conversations
- **Execute Group Chats**: Set up and run multi-agent conversations
- **Manage Configuration**: Configure framework parameters

### Containerization

Docker support enables:

- **Consistent Environment**: Ensure consistent behavior across different systems
- **Easy Deployment**: Simplify deployment to production environments
- **Isolation**: Isolate the framework from other applications
- **Scalability**: Scale the system based on demand
# Autogen Agents Framework Documentation (Part 2)

## Use Cases

The Autogen Agents Framework is designed to support a wide range of applications across various domains. Here are some key use cases where the framework excels:

### Conversational AI Systems

The framework is ideal for building sophisticated conversational AI systems that can:

- **Answer Complex Questions**: Leverage multiple agents with different expertise to provide comprehensive answers
- **Maintain Context**: Use the memory system to remember previous interactions and user preferences
- **Access External Knowledge**: Integrate with MCP servers to access documentation and knowledge bases
- **Provide Personalized Responses**: Adapt responses based on user history and preferences

### Collaborative Problem Solving

Multi-agent systems can tackle complex problems through collaboration:

- **Software Development**: Agents with different roles (architect, developer, tester) can collaborate on coding tasks
- **Research**: Specialized agents can gather, analyze, and synthesize information from various sources
- **Planning**: Agents can work together to create and refine plans for complex projects
- **Decision Support**: Multiple agents can provide different perspectives on decisions

### Knowledge Management

The framework's memory system makes it powerful for knowledge management applications:

- **Knowledge Base Construction**: Agents can build and maintain knowledge bases over time
- **Information Retrieval**: Retrieve relevant information from past conversations and stored memories
- **Knowledge Synthesis**: Combine information from multiple sources to create new insights
- **Expertise Modeling**: Model domain expertise through specialized agents and memories

### Workflow Automation

Agents can automate complex workflows that require multiple steps and decision points:

- **Customer Support**: Route and resolve customer inquiries based on their nature and complexity
- **Content Creation**: Generate, review, and refine content through multi-agent collaboration
- **Data Processing**: Extract, transform, and analyze data through specialized agents
- **Task Coordination**: Coordinate complex tasks across different systems and domains

### Education and Training

The framework can be used to create educational experiences:

- **Tutoring Systems**: Specialized agents can provide instruction in different subjects
- **Skill Development**: Guide users through learning new skills with personalized feedback
- **Simulations**: Create simulated environments for training and practice
- **Assessment**: Evaluate user knowledge and provide targeted feedback

### Enterprise Applications

In enterprise settings, the framework can support:

- **Business Intelligence**: Analyze data and provide insights through specialized agents
- **Project Management**: Coordinate and track project activities across teams
- **Customer Relationship Management**: Maintain customer information and interactions
- **Knowledge Worker Augmentation**: Enhance knowledge worker productivity through AI assistance

## Getting Started

### Prerequisites

Before using the Autogen Agents Framework, ensure you have:

- **Python 3.8+**: The framework requires Python 3.8 or higher
- **pip**: For installing dependencies
- **Virtual Environment**: Recommended for isolating dependencies
- **OpenAI API Key**: For accessing OpenAI models (or other supported LLM providers)
- **Context7 API Key**: Optional, for MCP integration

### Installation

#### From PyPI (Recommended)

```bash
pip install autogen-agents-framework
```

#### From Source

```bash
git clone https://github.com/yourusername/autogen-agents-framework.git
cd autogen-agents-framework
pip install -e .
```

### Environment Setup

1. **Create Environment File**:

Create a `.env` file in your project root with the following variables:

```
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Context7 MCP Server Configuration
CONTEXT7_API_KEY=your_context7_api_key
CONTEXT7_API_URL=https://api.context7.com/v1

# Memory Configuration
MEMORY_DB_PATH=./data/agent_memories.db

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/framework.log

# Caching Configuration
CACHE_DIR=./cache

# Group Chat Configuration
MAX_ROUND=10
```

2. **Run Setup Script**:

```bash
python setup_environment.py
```

This script will:
- Create necessary directories
- Install dependencies
- Set up the environment file
- Make scripts executable

### Basic Usage

#### Creating Agents

```python
from autogen_agents_framework import AgentFramework

# Initialize the framework
framework = AgentFramework()

# Create an assistant agent
assistant = framework.create_agent(
    agent_type="assistant",
    name="MyAssistant",
    description="A helpful assistant",
    system_message="You are a helpful assistant.",
    llm_config={
        "config_list": [
            {
                "model": "gpt-4",
                "api_key": "your_api_key"
            }
        ]
    }
)

# Create a user proxy agent
user_proxy = framework.create_agent(
    agent_type="user_proxy",
    name="UserProxy",
    description="A proxy for the human user",
    system_message="You are a proxy for the human user.",
    human_input_mode="TERMINATE"
)
```

#### Starting a Conversation

```python
# Initiate a conversation
user_proxy.initiate_chat(
    assistant,
    message="Hello! Can you help me with a Python problem?"
)
```

#### Using the Memory System

```python
from autogen_agents_framework.utils.memory_manager import MemoryManager

# Create a memory manager
memory_manager = MemoryManager(db_path="./data/memories.db")

# Store a memory
memory_manager.store_memory(
    agent_name="MyAssistant",
    memory_type="fact",
    content={
        "subject": "user",
        "predicate": "likes",
        "object": "Python programming"
    }
)

# Retrieve memories
memories = memory_manager.retrieve_memories("MyAssistant")
```

#### Using MCP Integration

```python
from autogen_agents_framework.integrations.context7 import Context7Client

# Create a Context7 client
context7_client = Context7Client(
    api_key="your_context7_api_key",
    api_url="https://api.context7.com/v1"
)

# Get documentation for a library
docs = context7_client.get_library_docs("/vercel/next.js")
```

#### Using the CLI

```bash
# Create an assistant agent
autogen-framework create-agent assistant MyAssistant "A helpful assistant" --system-message "You are a helpful assistant."

# Run a conversation
autogen-framework run-conversation UserProxy MyAssistant "Hello! Can you help me with a Python problem?"
```

## Configuration

The Autogen Agents Framework can be configured through environment variables, configuration files, or programmatically.

### Environment Variables

Key environment variables include:

- **AZURE_OPENAI_API_KEY**: API key for Azure OpenAI
- **AZURE_OPENAI_ENDPOINT**: Endpoint URL for Azure OpenAI
- **AZURE_OPENAI_API_VERSION**: API version for Azure OpenAI
- **AZURE_OPENAI_DEPLOYMENT_NAME**: Deployment name for Azure OpenAI
- **CONTEXT7_API_KEY**: API key for Context7
- **CONTEXT7_API_URL**: API URL for Context7
- **MEMORY_DB_PATH**: Path to the memory database
- **LOG_LEVEL**: Logging level (DEBUG, INFO, WARNING, ERROR)
- **LOG_FILE**: Path to the log file
- **CACHE_DIR**: Directory for caching
- **MAX_ROUND**: Maximum number of rounds in a group chat

### Configuration File

You can also use a configuration file (`config.json` or `config.yaml`) to configure the framework:

```json
{
  "llm": {
    "provider": "azure_openai",
    "config": {
      "api_key": "your_api_key",
      "endpoint": "https://your-endpoint.openai.azure.com/",
      "api_version": "2023-05-15",
      "deployment_name": "your_deployment_name"
    }
  },
  "memory": {
    "db_path": "./data/agent_memories.db"
  },
  "logging": {
    "level": "INFO",
    "file": "./logs/framework.log"
  },
  "mcp": {
    "context7": {
      "api_key": "your_context7_api_key",
      "api_url": "https://api.context7.com/v1"
    }
  },
  "group_chat": {
    "max_round": 10
  }
}
```

### Programmatic Configuration

You can also configure the framework programmatically:

```python
from autogen_agents_framework import AgentFramework

framework = AgentFramework(
    llm_config={
        "provider": "azure_openai",
        "config": {
            "api_key": "your_api_key",
            "endpoint": "https://your-endpoint.openai.azure.com/",
            "api_version": "2023-05-15",
            "deployment_name": "your_deployment_name"
        }
    },
    memory_config={
        "db_path": "./data/agent_memories.db"
    },
    logging_config={
        "level": "INFO",
        "file": "./logs/framework.log"
    },
    mcp_config={
        "context7": {
            "api_key": "your_context7_api_key",
            "api_url": "https://api.context7.com/v1"
        }
    },
    group_chat_config={
        "max_round": 10
    }
)
```
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
# Autogen Agents Framework Documentation (Part 4)

## Command Line Interface

The Autogen Agents Framework includes a powerful command-line interface (CLI) that allows users to create agents, run conversations, and manage the framework without writing code.

### Installation

The CLI is automatically installed when you install the framework:

```bash
pip install autogen-agents-framework
```

This installs the `autogen-framework` command.

### Available Commands

#### Create Agent

Create a new agent:

```bash
autogen-framework create-agent <agent_type> <name> <description> [options]
```

Options:
- `--system-message TEXT`: System message for the agent
- `--llm-config FILE`: Path to LLM configuration file
- `--tools TEXT`: Comma-separated list of tool names
- `--human-input-mode TEXT`: Human input mode (ALWAYS, TERMINATE, NEVER)
- `--code-execution-config FILE`: Path to code execution configuration file

Example:
```bash
autogen-framework create-agent assistant ResearchAssistant "Research specialist" --system-message "You are a research specialist."
```

#### Run Conversation

Run a conversation between two agents:

```bash
autogen-framework run-conversation <sender> <receiver> <message> [options]
```

Options:
- `--max-turns INTEGER`: Maximum number of conversation turns
- `--save-history`: Save conversation history to memory

Example:
```bash
autogen-framework run-conversation UserProxy ResearchAssistant "Find information about climate change"
```

#### Run Group Chat

Run a group chat with multiple agents:

```bash
autogen-framework run-group-chat <manager> <agents> <message> [options]
```

Options:
- `--max-rounds INTEGER`: Maximum number of conversation rounds
- `--save-history`: Save conversation history to memory

Example:
```bash
autogen-framework run-group-chat GroupChatManager "UserProxy,ResearchAssistant,Coder,Planner" "Create a climate change visualization app"
```

#### List Agents

List all available agents:

```bash
autogen-framework list-agents
```

#### List Tools

List all available tools:

```bash
autogen-framework list-tools [--category TEXT]
```

#### Memory Commands

Manage the memory system:

```bash
# Store a memory
autogen-framework store-memory <agent_name> <memory_type> <content>

# Retrieve memories
autogen-framework retrieve-memories <agent_name> [--memory-type TEXT]

# Search memories
autogen-framework search-memories <query>
```

### Configuration

The CLI can be configured through environment variables or a configuration file:

```bash
# Set environment variables
export AUTOGEN_FRAMEWORK_CONFIG_FILE=./config.json

# Or use command-line options
autogen-framework --config-file ./config.json <command>
```

## Examples

The Autogen Agents Framework includes several example scripts that demonstrate different aspects of the framework.

### Basic Agent Example

This example demonstrates the basic functionality of creating agents and initiating a conversation:

```python
# basic_agent_example.py
import os
import sys
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.framework import AgentFramework
from src.utils.logging_utils import setup_logger, get_default_log_file

def main():
    """Run the basic agent example."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="basic_agent_example",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting basic agent example")
    
    # Create the agent framework
    framework = AgentFramework()
    logger.info("Created agent framework")
    
    # Create an assistant agent
    assistant = framework.create_agent(
        agent_type="assistant",
        name="BasicAssistant",
        description="A helpful assistant that can answer questions",
        system_message="You are a helpful assistant. Answer questions concisely and accurately.",
        llm_config=None  # Use default config or None for local testing
    )
    logger.info("Created assistant agent")
    
    # Create a user proxy agent
    user_proxy = framework.create_agent(
        agent_type="user_proxy",
        name="UserProxy",
        description="A proxy for the human user",
        system_message="You are a proxy for the human user. You help facilitate the conversation.",
        human_input_mode="NEVER"  # Don't require human input for this example
    )
    logger.info("Created user proxy agent")
    
    # Initiate a conversation
    logger.info("Starting conversation")
    user_proxy.initiate_chat(
        assistant,
        message="Hello! Can you tell me what the agent framework does?"
    )
    
    logger.info("Basic agent example completed")

if __name__ == "__main__":
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
```

### Memory Example

This example demonstrates the memory system:

```python
# simple_memory_example.py
import os
import sys
import uuid
import dotenv
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

# Load environment variables from .env file
dotenv.load_dotenv()

from src.utils.memory_manager import MemoryManager
from src.utils.logging_utils import setup_logger, get_default_log_file

def main():
    """Run the simple memory example."""
    
    # Set up logging
    log_file = os.getenv("LOG_FILE", get_default_log_file())
    logger = setup_logger(
        name="simple_memory_example",
        level=os.getenv("LOG_LEVEL", "INFO"),
        log_file=log_file
    )
    logger.info("Starting simple memory example")
    
    # Create a memory manager
    memory_db_path = os.getenv("MEMORY_DB_PATH", "./data/simple_memory.db")
    memory_manager = MemoryManager(db_path=memory_db_path)
    logger.info(f"Created memory manager with database at {memory_db_path}")
    
    # Generate a unique conversation ID
    conversation_id = str(uuid.uuid4())
    memory_manager.create_conversation(conversation_id, "Simple Memory Example")
    logger.info(f"Created conversation with ID: {conversation_id}")
    
    # Store some memories
    memory_manager.store_memory(
        agent_name="Assistant",
        memory_type="fact",
        content={
            "subject": "user",
            "predicate": "likes",
            "object": "Python programming"
        }
    )
    logger.info("Stored fact memory for Assistant")
    
    memory_manager.store_memory(
        agent_name="Assistant",
        memory_type="skill",
        content={
            "skill_name": "coding",
            "proficiency": "expert",
            "description": "Ability to write clean, efficient Python code"
        }
    )
    logger.info("Stored skill memory for Assistant")
    
    # Add some messages to the conversation
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="User",
        receiver="Assistant",
        content="Hello, can you help me with a Python problem?"
    )
    logger.info("Added user message to conversation")
    
    memory_manager.add_message(
        conversation_id=conversation_id,
        sender="Assistant",
        receiver="User",
        content="Of course! I'd be happy to help with your Python problem. What specifically are you working on?"
    )
    logger.info("Added assistant message to conversation")
    
    # Retrieve and print conversation history
    print("\n=== Conversation History ===")
    history = memory_manager.get_conversation_history(conversation_id)
    for i, message in enumerate(history, 1):
        print(f"{i}. {message['timestamp']} - {message['sender']} to {message['receiver']}: {message['content']}")
    
    # Retrieve and print agent memories
    print("\n=== Agent Memories ===")
    memories = memory_manager.retrieve_memories("Assistant")
    for memory in memories:
        print(f"- Type: {memory['memory_type']}")
        if isinstance(memory['content'], dict):
            for key, value in memory['content'].items():
                print(f"  {key}: {value}")
        else:
            print(f"  Content: {memory['content']}")
    
    # Search for memories
    print("\n=== Memory Search ===")
    search_results = memory_manager.search_memories("Python")
    print(f"Found {len(search_results)} memories containing 'Python':")
    for memory in search_results:
        print(f"- Agent: {memory['agent_name']}")
        print(f"- Type: {memory['memory_type']}")
        if isinstance(memory['content'], dict):
            for key, value in memory['content'].items():
                print(f"  {key}: {value}")
        else:
            print(f"  Content: {memory['content']}")
    
    logger.info("Simple memory example completed")

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    os.makedirs("./data", exist_ok=True)
    
    # Create logs directory if it doesn't exist
    os.makedirs("./logs", exist_ok=True)
    
    main()
```

### Comprehensive Framework Demo

This example demonstrates the full capabilities of the framework, including multi-agent interactions, memory persistence, MCP integration, specialized agents, and group chat management:

```python
# comprehensive_framework_demo.py
# (See the examples directory for the full implementation)
```

## Testing

The Autogen Agents Framework includes a comprehensive test suite to ensure reliability and correctness.

### Running Tests

To run the tests, use the `run_tests.py` script:

```bash
python run_tests.py
```

Options:
- `--verbose`: Enable verbose output
- `--test-path`: Specify a specific test path to run

### Test Structure

The tests are organized into the following categories:

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test interactions between components
- **End-to-End Tests**: Test complete workflows

### Writing Tests

When contributing to the framework, it's important to write tests for new features:

```python
import unittest
from src.framework import AgentFramework

class TestAgentFramework(unittest.TestCase):
    def setUp(self):
        self.framework = AgentFramework()
    
    def test_create_agent(self):
        agent = self.framework.create_agent(
            agent_type="assistant",
            name="TestAgent",
            description="Test agent",
            system_message="You are a test agent."
        )
        self.assertEqual(agent.name, "TestAgent")
        self.assertEqual(agent.description, "Test agent")
```

## Deployment

The Autogen Agents Framework can be deployed in various environments, from local development to production.

### Local Development

For local development, you can install the framework directly:

```bash
pip install -e .
```

### Docker Deployment

For containerized deployment, use the provided Dockerfile:

```bash
# Build the Docker image
docker build -t autogen-agents-framework .

# Run the container
docker run -it --rm autogen-agents-framework
```

### Production Deployment

For production deployment, consider the following best practices:

- **Environment Variables**: Use environment variables for configuration
- **Secrets Management**: Use a secrets manager for API keys
- **Logging**: Configure appropriate logging levels
- **Monitoring**: Set up monitoring for the application
- **Scaling**: Consider horizontal scaling for high-traffic applications

## Best Practices

### Agent Design

- **Clear Roles**: Give each agent a clear, specific role
- **Detailed System Messages**: Provide detailed system messages to guide agent behavior
- **Appropriate Tools**: Equip agents with the tools they need for their roles
- **Memory Usage**: Use the memory system to maintain context and knowledge

### Memory Management

- **Structured Memories**: Use structured memories (dictionaries) for better organization
- **Memory Types**: Use appropriate memory types for different kinds of information
- **Regular Cleanup**: Periodically clean up outdated or irrelevant memories
- **Search Optimization**: Use specific search queries to find relevant memories

### Conversation Management

- **Clear Instructions**: Provide clear instructions to agents at the start of conversations
- **Appropriate Max Rounds**: Set an appropriate maximum number of rounds for group chats
- **Conversation History**: Save conversation history for important interactions
- **Error Handling**: Implement error handling for conversation failures

### Tool Development

- **Clear Descriptions**: Provide clear descriptions for tools
- **Parameter Validation**: Validate tool parameters to prevent errors
- **Error Handling**: Implement error handling for tool failures
- **Documentation**: Document tool usage and examples

## Troubleshooting

### Common Issues

#### Agent Creation Errors

- **Issue**: Error creating an agent
- **Solution**: Check the agent type and parameters, ensure the LLM configuration is correct

#### Memory Database Errors

- **Issue**: Error accessing the memory database
- **Solution**: Check the database path, ensure the directory exists and is writable

#### Tool Execution Errors

- **Issue**: Error executing a tool
- **Solution**: Check the tool parameters, ensure the tool function is properly implemented

#### MCP Integration Errors

- **Issue**: Error connecting to MCP server
- **Solution**: Check the API key and URL, ensure the server is accessible

### Debugging

- **Enable Debug Logging**: Set `LOG_LEVEL=DEBUG` for detailed logs
- **Check Logs**: Review the log file for error messages
- **Use Verbose Mode**: Use the `--verbose` flag with CLI commands
- **Test Components**: Test individual components to isolate issues

## Future Roadmap

The Autogen Agents Framework is under active development, with several planned enhancements:

### Short-term Goals

- **Enhanced Memory System**: Improved memory retrieval and organization
- **Additional MCP Integrations**: Support for more MCP servers
- **Expanded Tool Library**: More built-in tools for common tasks
- **Improved Documentation**: More examples and tutorials

### Medium-term Goals

- **Web Interface**: A web-based interface for managing agents and conversations
- **Agent Marketplace**: A marketplace for sharing and discovering agents
- **Performance Optimization**: Improved performance for large-scale deployments
- **Advanced Analytics**: Analytics for agent performance and conversation metrics

### Long-term Goals

- **Multi-modal Agents**: Support for agents that can process and generate images, audio, and video
- **Agent Learning**: Agents that can learn and improve over time
- **Collaborative Agent Networks**: Networks of agents that can collaborate across organizations
- **Autonomous Agent Systems**: Systems of agents that can operate autonomously

## Contributing

Contributions to the Autogen Agents Framework are welcome! Here's how you can contribute:

### Getting Started

1. **Fork the Repository**: Fork the repository on GitHub
2. **Clone Your Fork**: Clone your fork to your local machine
3. **Create a Branch**: Create a branch for your changes
4. **Make Changes**: Make your changes to the codebase
5. **Run Tests**: Run the tests to ensure your changes don't break anything
6. **Submit a Pull Request**: Submit a pull request with your changes

### Contribution Guidelines

- **Code Style**: Follow the project's code style (PEP 8 for Python)
- **Documentation**: Document your changes with docstrings and comments
- **Tests**: Write tests for new features and bug fixes
- **Commit Messages**: Write clear, descriptive commit messages

### Code of Conduct

The Autogen Agents Framework project adheres to a code of conduct that promotes a welcoming and inclusive community. Please read and follow the code of conduct when participating in the project.

## License

The Autogen Agents Framework is released under the MIT License:

```
MIT License

Copyright (c) 2023 Your Name or Organization

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
