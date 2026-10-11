
import os
from dotenv import load_dotenv
from google import genai
from ai.llm import ask_llm

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key else None


def ask_gemini(question, history=None):
    """Try Gemini first, then LLM7, using recent conversation history."""

    history = history or []

    conversation = []

    for message in history:
        role = message.get("role", "")
        content = message.get("content", "")

        if role in ("user", "assistant") and content:
            conversation.append(f"{role}: {content}")

    conversation.append(f"user: {question}")

    prompt = (
        "You are SAMSHIV, a friendly personal AI assistant. "
        "Answer clearly and help beginners. Use conversation history "
        "to understand follow-up questions.\n\n"
        "Conversation:\n"
        + "\n".join(conversation)
        + "\n\nSAMSHIV:"
    )

    if client:
        try:
            print("JARVIS is thinking... (Gemini)")

            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt,
                config={"http_options": {"timeout": 15000}},
            )

            if response.text:
                return response.text

            print("Gemini returned an empty response.")

        except Exception as error:
            print("Gemini failed:", repr(error))

    try:
        print("JARVIS is switching to LLM7...")
        answer = ask_llm(prompt)

        if answer:
            return answer

        return "Sorry Sam, the AI providers returned an empty response."

    except Exception as error:
        print("LLM7 failed:", repr(error))
        return (
            "Sorry Sam, both Gemini and LLM7 are unavailable. "
            "Please try again later."
        )