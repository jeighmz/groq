import os

from groq import Groq

input = input("Enter your message: ")

models = ["mixtral-8x7b-32768", "deepseek-r1-distill-llama-70b", "llama-3.3-70b-versatile"]

client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)
for i in range(3):
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": input,
            }
        ],
        model= models[i],
    )
    print(f"Model: {models[i]}")
    print(chat_completion.choices[0].message.content)
