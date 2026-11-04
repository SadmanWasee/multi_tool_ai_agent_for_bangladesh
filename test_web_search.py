
from tools.web_search_tool import web_search_tool

def main():
    query = "What is artificial intelligence?"

    print("\n========== WEB SEARCH TEST ==========")

    result = web_search_tool.invoke({
        "query": query
    })

    print(f"Search Query: {query}")
    print("\nSearch Results:")
    print(result)


if __name__ == "__main__":
    main()
