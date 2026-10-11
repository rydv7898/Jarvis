
from ai.gemini_ai import ask_gemini

print("Testing SAMSHIV with Gemini AI...")

question = "Explain IoT in simple words with one example."

answer = ask_gemini(question)

print("\nSAMSHIV's AI answer:")
print(answer)