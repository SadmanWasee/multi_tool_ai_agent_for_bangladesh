
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun


# Initialize the DuckDuckGo search engine
search_engine = DuckDuckGoSearchRun()


@tool
def web_search_tool(query: str) -> str:
    """
    Search the web for general knowledge and information
    that is not available in the Bangladesh datasets.

    Use this tool for topics such as technology, science,
    current affairs, international information, and general questions.
    """
    try:
        result = search_engine.run(query)
        return result

    except Exception as error:
        return f"Web search failed: {str(error)}"
