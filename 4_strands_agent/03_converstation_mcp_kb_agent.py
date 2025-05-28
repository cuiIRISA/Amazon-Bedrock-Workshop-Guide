from strands import Agent
from strands.models import BedrockModel
import boto3
from strands.tools.mcp.mcp_client import MCPClient
from mcp import stdio_client, StdioServerParameters


# Create a custom boto3 session
session = boto3.Session(region_name='us-east-1')
model_id = "us.amazon.nova-premier-v1:0"

# Create a Bedrock model with the custom session
bedrock_model = BedrockModel(
    model_id=model_id,
    boto_session=session
)

# Initialize MCP client
stdio_mcp_client = MCPClient(lambda: stdio_client(
    StdioServerParameters(
        command="uvx", 
        args=["awslabs.aws-documentation-mcp-server@latest"]
    )
))



# Start the MCP client context
with stdio_mcp_client:
    # Fetch available tools
    tools = stdio_mcp_client.list_tools_sync()
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