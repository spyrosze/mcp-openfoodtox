import pytest
import logging
import pandas as pd
from src.mcp_openfoodtox.database.queries import query_by_id

# Configure logging to see output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_query_by_id():
    """Test query_by_id with manual input.
    run with:
    `uv run pytest tests/test_database/test_query_by_id.py::test_query_by_id -v -s`

    Modify the variables below to test different scenarios:
    - id_value: single int or list of ints
    - table_name: table name to query
    """
    # ===== MANUAL INPUT - MODIFY THESE VALUES =====
    id_value = [19315, 15832, 15826]  # Single ID, or use [530, 531] for multiple IDs
    table_name = (
        "GENOTOX"  # Options: endpoint_study, genotox, chem_assess, opinion, component
    )
    # ===============================================

    logging.info(f"=" * 80)
    logging.info(f"Testing query_by_id")
    logging.info(f"=" * 80)
    logging.info(f"ID value: {id_value}")
    logging.info(f"Table name: {table_name}")
    logging.info(f"=" * 80)

    try:
        result = query_by_id(id_value, table_name)

        logging.info(f"\nResults:")
        logging.info(f"  Returned {len(result)} row(s)")

        if result.empty:
            logging.info("  No data found (empty DataFrame)")
        else:
            logging.info(f"  Shape: {result.shape}")
            logging.info(f"  Columns: {list(result.columns)}")

            # Show first few rows
            logging.info(f"\n  First {min(3, len(result))} row(s):")
            for idx, row in result.head(3).iterrows():
                logging.info(f"\n    Row {idx}:")
                # Show a few key columns
                for col in result.columns[:5]:  # Show first 5 columns
                    value = row.get(col)
                    if value is not None and pd.notna(value):
                        value_str = str(value)
                        if len(value_str) > 80:
                            logging.info(f"      {col}: {value_str[:80]}...")
                        else:
                            logging.info(f"      {col}: {value_str}")

        logging.info(f"\n" + "=" * 80)
        logging.info(f"Test complete")
        logging.info(f"=" * 80)

    except ValueError as e:
        logging.error(f"ValueError: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {type(e).__name__}: {e}")
        raise
