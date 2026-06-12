from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_response(user_message: str, context_str: str, chat_history: list) -> str:
    messages = [
        {
            "role": "system",
            "content": context_str
        }
    ]

    for msg in chat_history[-6:]:
        messages.append({"role": msg["role"], "content": msg["content"]})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",  
        messages=messages,
        max_tokens=300,
        temperature=0.3,
    )
    return response.choices[0].message.content