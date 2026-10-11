
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

api_token = os.getenv("LLM7_API_TOKEN")

if not api_token:
    raise ValueError(
        "LLM7_API_TOKEN was not found. Check your .env file."
    )

client = OpenAI(
    api_key=api_token,
    base_url="https://api.llm7.io/v1"
)


def ask_llm(question, history=None):
    """Send a question and recent conversation to LLM7."""

    messages = [
        {
            "role": "system",
            "content": (
                "You are SAMSHIV, a helpful personal AI assistant. "
                "Give clear, concise, beginner-friendly answers. "
                "Use previous messages to understand follow-up questions."
            )
        }
    ]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": question
    })

    response = client.chat.completions.create(
        model="DeepSeek-V4-Flash-0731",
        messages=messages,
        temperature=0.7
    )

    return response.choices[0].message.content
