import os

from dotenv import load_dotenv
from openai import OpenAI


# Load variables from .env
load_dotenv()


# Get LLM7 API token
api_token = os.getenv("LLM7_API_TOKEN")


# Check whether the token exists
if not api_token:

    raise ValueError(
        "LLM7_API_TOKEN was not found. "
        "Check your .env file."
    )


# Create LLM7 client
client = OpenAI(
    api_key=api_token,
    base_url="https://api.llm7.io/v1"
)


def ask_llm(question):

    response = client.chat.completions.create(
        model="DeepSeek-V4-Flash-0731",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are JARVIS, a helpful personal "
                    "AI assistant. Give clear and concise "
                    "answers."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.7
    )

    answer = response.choices[0].message.content

    return answer

