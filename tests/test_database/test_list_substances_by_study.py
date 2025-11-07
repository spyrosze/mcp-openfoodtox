import pytest
import logging
import pandas as pd
from src.mcp_openfoodtox.database.multi_sub_queries import query_substances_by_study

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_list_substances_by_study_log_output():
    """Test list_substances_by_study and log results.
    run with:
    `uv run pytest tests/test_database/test_list_substances_by_study.py::test_list_substances_by_study_log_output -v -s`
    """
    # ===== MANUAL INPUT - MODIFY THESE VALUES =====
    ids = [9335]  # Study IDs to filter by
    study_type = (
        "genotox"  # Options: "genotox", "tox", "endpoint_study", "hazard", "chem_assess", "opinion"
    )
    limit = 5
    # ===============================================

    logging.info(f"Testing list_substances_by_study")
    logging.info(f"  IDs: {ids}")
    logging.info(f"  Study type: {study_type}")
    logging.info(f"  Limit: {limit}")

    try:
        result = query_substances_by_study(ids=ids, study_type=study_type, limit=limit)

        results_df = result["results"]
        total_count = result["total_count"]

        logging.info(f"Results: {len(results_df)} rows (total: {total_count})")

        if not results_df.empty:
            for idx, row in results_df.iterrows():
                logging.info(f"  {row.get('COM_NAME')} (SUB_COM_ID: {row.get('SUB_COM_ID')})")

    except Exception as e:
        logging.error(f"Error: {type(e).__name__}: {e}")
        raise
