
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_classic.agents import (
    AgentExecutor,
    create_tool_calling_agent
)

from tools.database_tools import (
    institutions_db_tool,
    hospitals_db_tool,
    restaurants_db_tool
)

from tools.web_search_tool import web_search_tool


# ==========================================
# 1. Initialize the local language model
# ==========================================

llm = ChatOllama(
    model="qwen2.5:3b",
    temperature=0,
    num_ctx=2048
)


# ==========================================
# 2. Register all four tools
# ==========================================

tools = [
    institutions_db_tool,
    hospitals_db_tool,
    restaurants_db_tool,
    web_search_tool
]


# ==========================================
# 3. Define the agent's system instructions
# ==========================================

system_prompt = """
You are the Bangladesh Multi-Tool AI Assistant.

Your job is to answer questions using the available Bangladesh
databases or the web search tool.

==============================
TOOL SELECTION
==============================

1. institutions_db_tool

Use for questions about:
- Schools, colleges and universities
- Madrasahs and educational institutions
- EIIN numbers
- Education levels
- Institutional locations

2. hospitals_db_tool

Use for questions about:
- Hospitals and healthcare organizations
- Healthcare organization names
- Agencies and organization types
- Healthcare organization locations

IMPORTANT:
This dataset also contains healthcare offices and public health
organizations. Do not describe every record as a hospital.

3. restaurants_db_tool

Use for questions about:
- Restaurant names
- Restaurant addresses
- Ratings and reviews
- Geographical coordinates

4. web_search_tool

Use for:
- General knowledge
- Science and technology
- Artificial intelligence
- International information
- Current affairs
- Information not available in the Bangladesh datasets

==============================
DATABASE SCHEMAS
==============================

INSTITUTIONS DATABASE

Table: institutions

Available columns:
institute_name, eiin, institute_type, division_id,
division, district_id, district, thana_id, thana,
union_id, union_name, mauza_id, mauza_name,
area_status, geogrpycal_status, address, post,
management_type, mobile, student_type, education_level,
affiliation, mpo_status

Important query instructions:
- For schools, use institute_type = 'School'.
- For colleges, use institute_type = 'College' when applicable.
- For Dhaka, filter using district = 'DHAKA'.
- Never use a column named city in this database.

HOSPITALS DATABASE

Table: hospitals

Available columns:
id, name, name_bangla, code, agency, type, division,
district, city_corporation, upazila, paurasava, union,
private

Important query instructions:
- For Dhaka, filter using the district column.
- Use name, type, agency and location fields as appropriate.
- Do not assume that every record represents a hospital.

RESTAURANTS DATABASE

Table: restaurants

Available columns:
place_id, name, latitude, longitude, rating,
number_of_reviews, affluence, address

Important query instructions:
- Use rating for rating-related questions.
- Use number_of_reviews for review-related questions.
- There is no dedicated city or district column.
- For location searches, use the address column with LIKE.
- Do not invent a city column.

==============================
SQL QUERY RULES
==============================

1. Only generate valid SQLite SELECT queries.
2. Only use the database tables and columns listed above.
3. Never invent table names or column names.
4. Use the correct database tool for each question.
5. Apply all relevant filters.

Examples:

Five schools in Dhaka:

SELECT institute_name, district, institute_type
FROM institutions
WHERE district = 'DHAKA'
AND institute_type = 'School'
LIMIT 5;

Five healthcare organizations in Dhaka:

SELECT name, type, district, agency
FROM hospitals
WHERE LOWER(district) LIKE '%dhaka%'
LIMIT 5;

Restaurants with ratings above 4.5:

SELECT name, rating, number_of_reviews, address
FROM restaurants
WHERE rating > 4.5
LIMIT 5;

Restaurants in Dhaka with ratings above 4.5:

SELECT name, rating, address
FROM restaurants
WHERE rating > 4.5
AND LOWER(address) LIKE '%dhaka%'
LIMIT 5;

Remember that restaurant location filtering depends on address
text and may not identify every restaurant in a particular city.

==============================
ANSWER GENERATION RULES
==============================

1. Always use database tools for questions about the available
   Bangladesh datasets.
2. Use web_search_tool for general knowledge questions.
3. After receiving tool results, generate a clear final answer.
4. Never invent database records or search results.
5. If no records are found, say so clearly.
6. Do not claim that the datasets contain bed capacity,
   doctor information or medical facilities data.
7. Do not invent explanations for dataset abbreviations.
8. Do not interpret MPO status beyond the actual stored value.
9. Clearly distinguish database results from web search results.
10. Keep answers concise, accurate and well organized.

"""


# ==========================================
# 4. Create the agent prompt
# ==========================================

prompt = ChatPromptTemplate.from_messages([
    ("system", system_prompt),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])


# ==========================================
# 5. Create the tool-calling agent
# ==========================================

agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


# ==========================================
# 6. Create the Agent Executor
# ==========================================

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    max_iterations=6,
    handle_parsing_errors=True,
    return_intermediate_steps=True
)


# ==========================================
# 7. Interactive command-line interface
# ==========================================

def main():

    print("\n========================================")
    print("   Bangladesh Multi-Tool AI Agent")
    print("========================================")

    print("Ask questions about Bangladesh or general topics.")
    print("Type 'exit' to quit.\n")

    while True:

        try:
            user_input = input("You: ").strip()

        except (KeyboardInterrupt, EOFError):
            print("\n\nAgent: Goodbye!")
            break

        if user_input.lower() in ["exit", "quit"]:
            print("\nAgent: Goodbye!")
            break

        if not user_input:
            continue

        try:

            response = agent_executor.invoke({
                "input": user_input
            })

            answer = response.get("output", "").strip()

            if answer:
                print("\nAgent:", answer)

            else:
                print("\nAgent: I could not generate a final answer.")

                intermediate_steps = response.get(
                    "intermediate_steps", []
                )

                if intermediate_steps:
                    print("\nTool execution details:")

                    for action, observation in intermediate_steps:
                        print(f"\nTool: {action.tool}")
                        print(f"Result: {observation}")

                else:
                    print("No tools were successfully executed.")

            print()

        except Exception as error:

            print("\nAn error occurred:")
            print(error)
            print()


if __name__ == "__main__":
    main()
