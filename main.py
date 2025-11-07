import pandas as pd
from src.mcp_openfoodtox.database.connection import get_connection
from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from src.mcp_openfoodtox.tools.search_substance import search_substance
from src.mcp_openfoodtox.tools.get_risk_assessments import get_risk_assessments
from src.mcp_openfoodtox.tools.get_toxicity_endpoints import get_toxicity_endpoints
from src.mcp_openfoodtox.tools.get_genotox_details import get_genotox_details
from src.mcp_openfoodtox.tools.get_opinions import get_opinions
from src.mcp_openfoodtox.tools.substance_safety_assessment import get_substance_safety_assessment
from src.mcp_openfoodtox.tools.list_substances_by_class_and_safety import (
    list_substances_by_class_and_safety,
)
from src.mcp_openfoodtox.tools.list_hazard_ids_by_assessment import list_hazard_ids_by_assessment
from src.mcp_openfoodtox.tools.list_substances_by_assessment import list_substances_by_assessment

# Initialize FastMCP server
mcp = FastMCP("mcp-openfoodtox")

# Add tools to the server
mcp.add_tool(search_substance)
mcp.add_tool(get_risk_assessments)
mcp.add_tool(get_toxicity_endpoints)
mcp.add_tool(get_genotox_details)
mcp.add_tool(get_opinions)
mcp.add_tool(get_substance_safety_assessment)
mcp.add_tool(list_substances_by_class_and_safety)
mcp.add_tool(list_hazard_ids_by_assessment)
mcp.add_tool(list_substances_by_assessment)


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
