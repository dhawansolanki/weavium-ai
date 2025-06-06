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
