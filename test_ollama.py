
from langchain_ollama import ChatOllama


# Initialize the local Qwen model
llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0
)


def main():
    question = "Explain artificial intelligence in three sentences."

    print("========== OLLAMA TEST ==========")
    print(f"Question: {question}\n")

    response = llm.invoke(question)

    print("Model Response:")
    print(response.content)


if __name__ == "__main__":
    main()
