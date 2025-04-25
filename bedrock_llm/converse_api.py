import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client in the AWS Region you want to use.
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the model ID, e.g., DeepSeek-R1 Model.
#model_id = "us.deepseek.r1-v1:0"
model_id = "us.amazon.nova-pro-v1:0"

# Start a conversation with the user message.
user_message = "Hi"
conversation = [
    {
        "role": "user",
        "content": [{"text": user_message}],
    }
]

try:
    # Send the message to the model, using a basic inference configuration.
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 512, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print both reasoning and final response
    for content_block in response["output"]["message"]["content"]:
        if "reasoningContent" in content_block:
            print("\nREASONING:")
            print(content_block["reasoningContent"]["reasoningText"]["text"])
        elif "text" in content_block:
            print("\nFINAL ANSWER:")
            print(content_block["text"])
except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)

print(response)
