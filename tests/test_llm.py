from ai.llm import ask_llm


def main():

    print("JARVIS LLM7 Test")
    print("------------------")

    question = input("Ask JARVIS: ")

    print("\nThinking...\n")

    answer = ask_llm(question)

    print("JARVIS:")
    print(answer)


if __name__ == "__main__":
    main()
