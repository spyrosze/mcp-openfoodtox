import pytest
import logging
import pandas as pd
from src.mcp_openfoodtox.database.multi_sub_queries import query_substances_by_class_and_safety

# Configure logging to see output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_list_substances_by_criteria_log_output():
    """Test list_substances_by_criteria and log results for review.
    run with:
    `uv run pytest tests/test_database/test_list_substances_by_criteria.py::test_list_substances_by_criteria_log_output -v -s`

    Modify the variables below to test different filter combinations:
    """
    # ===== MANUAL INPUT - MODIFY THESE VALUES =====
    sub_class = "food additives"  # or None, "Pesticides", "Flavourings", etc.
    is_mutagenic = None  # or "Positive", "Negative", "No data", etc.
    is_genotoxic = None  # or "Positive", "Negative", "No data", etc.
    is_carcinogenic = "Ambiguous"  # or "Positive", "Negative", "No data", etc.
    remarks_contains = None  # or any text string to search in REMARKS_STUDY
    limit = 5  # Number of results to return
    # ===============================================

    logging.info(f"=" * 80)
    logging.info(f"Testing list_substances_by_criteria")
    logging.info(f"=" * 80)
    logging.info(f"Filters:")
    logging.info(f"  sub_class: {sub_class}")
    logging.info(f"  is_mutagenic: {is_mutagenic}")
    logging.info(f"  is_genotoxic: {is_genotoxic}")
    logging.info(f"  is_carcinogenic: {is_carcinogenic}")
    logging.info(f"  remarks_contains: {remarks_contains}")
    logging.info(f"  limit: {limit}")
    logging.info(f"=" * 80)

    try:
        result = query_substances_by_class_and_safety(
            sub_class=sub_class,
            is_mutagenic=is_mutagenic,
            is_genotoxic=is_genotoxic,
            is_carcinogenic=is_carcinogenic,
            remarks_contains=remarks_contains,
            limit=limit,
        )

        results_df = result["results"]
        total_count = result["total_count"]

        logging.info(f"\nResults Summary:")
        logging.info(f"  Returned {len(results_df)} row(s) (limited from {total_count} total)")
        logging.info(f"  Total matching substances: {total_count}")

        if results_df.empty:
            logging.info("  No data found (empty DataFrame)")
        else:
            logging.info(f"  Shape: {results_df.shape}")
            logging.info(f"  Columns: {list(results_df.columns)}")

            # Show all rows (since limit is small by default)
            logging.info(f"\n  All {len(results_df)} result(s):")
            for idx, row in results_df.iterrows():
                logging.info(f"\n    Row {idx}:")
                logging.info(f"      SUB_COM_ID: {row.get('SUB_COM_ID')}")
                logging.info(f"      COM_NAME: {row.get('COM_NAME')}")
                logging.info(f"      COM_TYPE: {row.get('COM_TYPE')}")
                logging.info(f"      SUB_TYPE: {row.get('SUB_TYPE')}")

                description = row.get("DESCRIPTION")
                if description is not None and pd.notna(description):
                    # DESCRIPTION might be a long comma-separated list
                    desc_str = str(description)
                    if len(desc_str) > 200:
                        logging.info(f"      DESCRIPTION: {desc_str[:200]}... (truncated)")
                        logging.info(f"        ... (total length: {len(desc_str)} chars)")
                    else:
                        logging.info(f"      DESCRIPTION: {desc_str}")
                else:
                    logging.info(f"      DESCRIPTION: None")

        logging.info(f"\n" + "=" * 80)
        logging.info(f"Test complete")
        logging.info(f"=" * 80)

    except Exception as e:
        logging.error(f"Unexpected error: {type(e).__name__}: {e}")
        import traceback

        logging.error(traceback.format_exc())
        raise


def test_list_substances_by_criteria_no_filters():
    """Test with no filters (should return all substances, limited)."""
    logging.info(f"=" * 80)
    logging.info(f"Testing list_substances_by_criteria with NO FILTERS")
    logging.info(f"=" * 80)

    result = query_substances_by_class_and_safety(limit=5)
    results_df = result["results"]
    total_count = result["total_count"]

    logging.info(f"Total count (no filters): {total_count}")
    logging.info(f"Returned rows: {len(results_df)}")
    logging.info(f"=" * 80)


def test_list_substances_by_criteria_food_additives():
    """Test filtering by Food additives category."""
    logging.info(f"=" * 80)
    logging.info(f"Testing list_substances_by_criteria: Food additives only")
    logging.info(f"=" * 80)

    result = query_substances_by_class_and_safety(sub_class="Food additives", limit=5)
    results_df = result["results"]
    total_count = result["total_count"]

    logging.info(f"Total Food additives: {total_count}")
    logging.info(f"Returned rows: {len(results_df)}")

    if not results_df.empty:
        logging.info(f"\nSample results:")
        for idx, row in results_df.head(3).iterrows():
            logging.info(f"  {row.get('COM_NAME')} (SUB_COM_ID: {row.get('SUB_COM_ID')})")

    logging.info(f"=" * 80)


def test_list_substances_by_criteria_genotoxic_positive():
    """Test filtering for genotoxic substances."""
    logging.info(f"=" * 80)
    logging.info(f"Testing list_substances_by_criteria: Genotoxic = Positive")
    logging.info(f"=" * 80)

    result = query_substances_by_class_and_safety(is_genotoxic="Positive", limit=5)
    results_df = result["results"]
    total_count = result["total_count"]

    logging.info(f"Total genotoxic (Positive): {total_count}")
    logging.info(f"Returned rows: {len(results_df)}")

    if not results_df.empty:
        logging.info(f"\nSample results:")
        for idx, row in results_df.head(3).iterrows():
            logging.info(f"  {row.get('COM_NAME')} (SUB_COM_ID: {row.get('SUB_COM_ID')})")

    logging.info(f"=" * 80)


def test_list_substances_by_criteria_combined_filters():
    """Test with multiple filters combined."""
    logging.info(f"=" * 80)
    logging.info(f"Testing list_substances_by_criteria: Combined filters")
    logging.info(f"  Food additives + Not genotoxic + Not carcinogenic")
    logging.info(f"=" * 80)

    result = query_substances_by_class_and_safety(
        sub_class="Food additives", is_genotoxic="Negative", is_carcinogenic="Negative", limit=5
    )
    results_df = result["results"]
    total_count = result["total_count"]

    logging.info(f"Total matching: {total_count}")
    logging.info(f"Returned rows: {len(results_df)}")

    if not results_df.empty:
        logging.info(f"\nSample results:")
        for idx, row in results_df.head(3).iterrows():
            logging.info(f"  {row.get('COM_NAME')} (SUB_COM_ID: {row.get('SUB_COM_ID')})")

    logging.info(f"=" * 80)
