import os
from groq import Groq

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)

# Initial user message
user_message = "Explain the importance of ethereum vs. solana. take a stance."

# Step 1: DeepSeek replies to user message
deepseek_response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": user_message,
        }
    ],
    model="deepseek-r1-distill-llama-70b",  # DeepSeek model
)

deepseek_reply = deepseek_response.choices[0].message.content
print(f"DeepSeek's response: {deepseek_reply}\n")

# Step 2: Llama3 replies to DeepSeek's response
llama3_response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": deepseek_reply,
        }
    ],
    model="llama-3.3-70b-versatile",  # Llama3 model
)

llama3_reply = llama3_response.choices[0].message.content
print(f"Llama3's response: {llama3_reply}\n")

# Step 3: DeepSeek replies to Llama3's response
deepseek_response_2 = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": llama3_reply,
        }
    ],
    model="deepseek-r1-distill-llama-70b",  # DeepSeek model
)

deepseek_reply_2 = deepseek_response_2.choices[0].message.content
print(f"DeepSeek's second response: {deepseek_reply_2}\n")

# Step 4: Llama3 replies to DeepSeek's second response
llama3_response_2 = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": deepseek_reply_2,
        }
    ],
    model="llama-3.3-70b-versatile",  # Llama3 model
)

llama3_reply_2 = llama3_response_2.choices[0].message.content
print(f"Llama3's second response: {llama3_reply_2}\n")