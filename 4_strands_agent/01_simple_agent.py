from strands import Agent
from strands.models import BedrockModel
import boto3

model_id = "us.deepseek.r1-v1:0"
#model_id = "us.amazon.nova-premier-v1:0"

# Create a custom boto3 session
session = boto3.Session(region_name='us-east-1')

# Create a Bedrock model with the custom session
bedrock_model = BedrockModel(
    model_id=model_id,
    boto_session=session
)

agent = Agent(model=bedrock_model)
# Ask the agent a question
agent("Tell me about Agentic workflow impact for the future of software development")
