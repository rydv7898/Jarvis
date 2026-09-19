from ai.llm import ask_llm


def main():

    print("SAMSHIV LLM7 Test")
    print("------------------")

    question = input("Ask SAMSHIV: ")

    print("\nThinking...\n")

    answer = ask_llm(question)

    print("SAMSHIV:")
    print(answer)


if __name__ == "__main__":
    main()