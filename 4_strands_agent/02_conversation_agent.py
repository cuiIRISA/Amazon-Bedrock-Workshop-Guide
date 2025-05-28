from strands import Agent
from strands.models import BedrockModel
import boto3


# Create a custom boto3 session
session = boto3.Session(region_name='us-east-1')
#model_id = "us.deepseek.r1-v1:0"
model_id = "us.amazon.nova-premier-v1:0"

# Create a Bedrock model with the custom session
bedrock_model = BedrockModel(
    model_id=model_id,
    boto_session=session
)

agent = Agent(model=bedrock_model,
              system_prompt="You are a helpful assistant."
              )

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
        #print(agent.messages)
except KeyboardInterrupt:
    print("\nInterrupted by user. Exiting...")