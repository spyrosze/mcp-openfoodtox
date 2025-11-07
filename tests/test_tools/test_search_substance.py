# tests/test_tools/test_search_substance.py
import pytest
import logging
from src.mcp_openfoodtox.tools.search_substance import search_substance
from src.mcp_openfoodtox.tools.substance_safety_assessment import substance_safety_assessment
from pandas import DataFrame


def test_search_substance_tool():
    """Test the MCP tool wrapper function directly.
    
    uv run pytest -s tests/test_tools/test_search_substance.py::test_search_substance_tool
    """
    # Test with a known substance
    result = search_substance("aspartame")
    
    # Verify it returns a list or None
    assert result is None or isinstance(result, list)
    
    if result:
        logging.info(f"Result: {result}")
        # Verify structure of first entry
        entry = result[0]
        assert "SUB_COM_ID" in entry
        assert "COM_NAME" in entry
        assert "COM_TYPE" in entry
        # ... verify other expected fields

def test_search_substance_tool_e_number():
    """Test E-number normalization."""
    result = search_substance("E951")
    assert result is not None or isinstance(result, list)
    
def test_substance_safety_assessment_tool():
    """Test the substance safety assessment tool."""
    result = substance_safety_assessment(478)
    assert result is not None or isinstance(result, DataFrame)
    logging.info(f"Result: {result}")