import boto3
from botocore.exceptions import ClientError

# Create a Bedrock Runtime client
client = boto3.client("bedrock-runtime", region_name="us-west-2")

# Set the model ID
#model_id = "us.deepseek.r1-v1:0"
model_id = "us.amazon.nova-pro-v1:0"
# Initialize conversation history
conversation = []

# Add first user message
user_message = "Hi, what is the machine learning in 3 paragraph within 500 words"
conversation.append({
    "role": "user",
    "content": [{"text": user_message}],
})

try:
    # Send the message to the model
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 2048, "temperature": 0.5, "topP": 0.9},
    )

    # Extract and print the response text
    response_text = response["output"]["message"]["content"][0]["text"]
    print(f"Assistant: {response_text}")
    
    # Add assistant's response to conversation history
    conversation.append({
        "role": "assistant",
        "content": [{"text": response_text}],
    })

    # Add second user message
    user_message_2 = "Can you list into the bullet points as for PowerPoint presentation?"
    conversation.append({
        "role": "user",
        "content": [{"text": user_message_2}],
    })

    # Send second message with conversation history
    response = client.converse(
        modelId=model_id,
        messages=conversation,
        inferenceConfig={"maxTokens": 2048, "temperature": 0.5, "topP": 0.9},
    )

    response_text = response["output"]["message"]["content"][0]["text"]
    print(f"Assistant: {response_text}")

except (ClientError, Exception) as e:
    print(f"ERROR: Can't invoke '{model_id}'. Reason: {e}")
    exit(1)
