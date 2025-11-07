"""Utility functions for exploring and querying the OpenFoodTox database."""

import sys
from pathlib import Path

# Add project root to path for direct script execution
project_root = Path(__file__).parent.parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import pandas as pd
from src.mcp_openfoodtox.database.connection import get_connection


def get_dictionary_descriptions(names: list[str]) -> dict[str, str]:
    """
    Self running helper function to get descriptions of column names in the Dictionary table.
    Useful for printing descriptions to insert in MCP tool descriptions. STATICALLY.
    Query the Dictionary table for descriptions of given column names.

    Args:
        names: List of column names (strings) to look up in the Dictionary table

    Returns:
        Dictionary mapping {name: description} for found names.
        Names not found in the Dictionary table will not be included in the result.
    """
    if not names:
        return {}

    with get_connection() as db_connection:
        # Create placeholders for SQL IN clause
        placeholders = ",".join("?" * len(names))

        query = f"""
            SELECT Name, Description
            FROM Dictionary
            WHERE Name IN ({placeholders})
        """

        df = pd.read_sql_query(query, db_connection, params=names)

        # Convert to dictionary {name: description}
        result = dict(zip(df["Name"], df["Description"]))

        return result


if __name__ == "__main__":
    # Example usage
    query_search_substance_names = [
        "SUB_COM_ID",
        "COM_NAME",
        "COM_TYPE",
        "MOLECULARFORMULA",
        "SUB_DESCRIPTION",
        "SUB_OP_CLASS",
        "REMARKS_STUDY",
        "GENOTOX_ID",
        "TOX_ID",
        "HAZARD_ID",
        "OP_ID",
    ]
    query_safety_assessment_names=["SUB_OP_CLASS",
                "IS_MUTAGENIC",
                "IS_GENOTOXIC",
                "IS_CARCINOGENIC",
                "REMARKS_STUDY",
                "TOXREF_ID",
                "OP_ID",
                "ADOPTIONDATE",
                "PUBLICATIONDATE",
                "AUTHOR",
                "TITLE"]
    descriptions = get_dictionary_descriptions(query_safety_assessment_names)

    print('<?xml version="1.0" encoding="UTF-8"?>')
    print("<dictionary_descriptions>")
    for name, desc in descriptions.items():
        # print(f"  <field>")
        print(f"    <name>{name}</name>")
        print(f"    <description>{desc}</description>")
        # print(f"  </field>")
    print("</dictionary_descriptions>")
    print(f"\n<!-- Found {len(descriptions)} out of {len(query_search_substance_names)} requested names -->")
