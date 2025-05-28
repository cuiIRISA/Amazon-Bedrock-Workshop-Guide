
Strands Agents is a simple yet powerful SDK that takes a model-driven approach to building and running AI agents. From simple conversational assistants to complex autonomous workflows, from local development to production deployment, Strands Agents scales with your needs.

## Feature Overview

- **Lightweight & Flexible**: Simple agent loop that just works and is fully customizable
- **Model Agnostic**: Support for Amazon Bedrock, Anthropic, LiteLLM, Llama, Ollama, OpenAI, and custom providers
- **Advanced Capabilities**: Multi-agent systems, autonomous agents, and streaming support
- **Built-in MCP**: Native support for Model Context Protocol (MCP) servers, enabling access to thousands of pre-built tools


https://github.com/strands-agents/sdk-python

## Quick Start

```bash
# Install Strands Agents
pip install strands-agents strands-agents-tools
```

Install the uvx if needed 
```bash
curl -LsSf https://astral.sh/uv/install.sh  | sh
```

```python
from strands import Agent
from strands_tools import calculator
agent = Agent(tools=[calculator])
agent("What is the square root of 1764")
```



https://github.com/strands-agents/sdk-python


#### Install Strands Agents
pip install strands-agents strands-agents-tools
