import pytest
import logging
from src.mcp_openfoodtox.database.multi_sub_queries import query_hazard_ids_by_assessment

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_query_hazard_ids_by_assessment_log_output():
    """Test query_hazard_ids_by_assessment and log results.
    run with:
    `uv run pytest tests/test_database/test_query_hazard_ids_by_assessment.py::test_query_hazard_ids_by_assessment_log_output -v -s`
    """
    # ===== MANUAL INPUT - MODIFY THESE VALUES =====
    population_text_contains = "children"  # e.g., "children", "infant", "pregnant"
    assessment_type = "TDI"  # e.g., "ADI", "TDI", "ARfD", or None for all
    risk_value_milli_max = None  # e.g., 1.0 for ADI < 1 mg/kg, or None
    risk_value_milli_min = None  # e.g., 10.0 for ADI > 10 mg/kg, or None
    has_no_risk_value = False  # True to find assessments with no quantitative limit, or None
    limit = 10  # Maximum number of HAZARD_IDs to return, or None for all
    # ===============================================

    logging.info(f"Testing query_hazard_ids_by_assessment")
    logging.info(f"  Population text contains: {population_text_contains}")
    logging.info(f"  Assessment type: {assessment_type}")
    logging.info(f"  Risk value milli max: {risk_value_milli_max}")
    logging.info(f"  Risk value milli min: {risk_value_milli_min}")
    logging.info(f"  Has no risk value: {has_no_risk_value}")
    logging.info(f"  Limit: {limit}")

    try:
        hazard_ids = query_hazard_ids_by_assessment(
            population_text_contains=population_text_contains,
            assessment_type=assessment_type,
            risk_value_milli_max=risk_value_milli_max,
            risk_value_milli_min=risk_value_milli_min,
            has_no_risk_value=has_no_risk_value,
            limit=limit,
        )

        logging.info(f"Results: {len(hazard_ids)} HAZARD_IDs found")
        if hazard_ids:
            logging.info(f"  First 10 HAZARD_IDs: {hazard_ids[:10]}")
            if len(hazard_ids) > 10:
                logging.info(f"  ... and {len(hazard_ids) - 10} more")

    except Exception as e:
        logging.error(f"Error: {type(e).__name__}: {e}")
        raise

