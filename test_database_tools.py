
from tools.database_tools import (
    institutions_db_tool,
    hospitals_db_tool,
    restaurants_db_tool
)


def main():

    print("\n========== INSTITUTIONS TEST ==========")

    result = institutions_db_tool.invoke({
        "query": """
            SELECT institute_name, district, institute_type
            FROM institutions
            WHERE district LIKE '%DHAKA%'
            LIMIT 5
        """
    })

    print(result)


    print("\n========== HOSPITALS TEST ==========")

    result = hospitals_db_tool.invoke({
        "query": """
            SELECT name, division, district, agency, type
            FROM hospitals
            WHERE district LIKE '%Dhaka%'
            LIMIT 5
        """
    })

    print(result)


    print("\n========== RESTAURANTS TEST ==========")

    result = restaurants_db_tool.invoke({
        "query": """
            SELECT name, rating, address
            FROM restaurants
            WHERE rating >= 4.0
            LIMIT 5
        """
    })

    print(result)


if __name__ == "__main__":
    main()
