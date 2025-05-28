from strands import Agent
from strands.models import BedrockModel
import boto3
from strands.tools.mcp.mcp_client import MCPClient
from mcp.client.streamable_http import streamablehttp_client

# Create a custom boto3 session
session = boto3.Session(region_name='us-east-1')
model_id = "us.amazon.nova-premier-v1:0"

# Create a Bedrock model with the custom session
bedrock_model = BedrockModel(
    model_id=model_id,
    boto_session=session
)

# Initialize MCP client
mcp_client = MCPClient(lambda: streamablehttp_client(
    "https://d33cj********.cloudfront.net/mcp/ ",
    headers={"Authorization": "Bearer *************"},
))



# Start the MCP client context
with mcp_client:
    # Fetch available tools
    tools = mcp_client.list_tools_sync()
    print("Available tools:", tools)

    # Initialize the agent
    agent = Agent(model=bedrock_model,tools=tools)

    # Interactive loop for user input
    try:
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['exit', 'quit', 'q']:
                print("Exiting the conversation.")
                break
            if not user_input:
                continue  # Skip empty input
            response = agent(user_input)
            print("Agent:", response)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting...")