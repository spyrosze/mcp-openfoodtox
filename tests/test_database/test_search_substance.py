import pytest
import logging
from src.mcp_openfoodtox.database.queries import query_search_substance

# Configure logging to see output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_search_substance_log_output():
    """Test search_substance and log results for review.
    run with:
    `uv run pytest tests/test_database/test_search_substance.py::test_search_substance_log_output -v -s`
    """
    search_term = "123477-69-0"

    logging.info(f"=" * 80)
    logging.info(f"Testing search_substance with: '{search_term}'")
    logging.info(f"=" * 80)

    results = query_search_substance(search_term)

    if results is None:
        logging.info("No results found (returned None)")
        return

    logging.info(f"\nFound {len(results)} entries")
    logging.info(f"\n" + "-" * 80)

    for idx, entry in enumerate(results, 1):
        logging.info(f"\nEntry {idx}:")
        logging.info(f"  SUB_COM_ID: {entry.get('SUB_COM_ID')}")
        logging.info(f"  COM_NAME: {entry.get('COM_NAME')}")
        logging.info(f"  COM_TYPE: {entry.get('COM_TYPE')}")
        logging.info(f"  MOLECULARFORMULA: {entry.get('MOLECULARFORMULA')}")
        logging.info(f"  SUB_DESCRIPTION: {entry.get('SUB_DESCRIPTION')}")

        # Display arrays nicely
        sub_op_class = entry.get("SUB_OP_CLASS")
        if sub_op_class:
            logging.info(f"  SUB_OP_CLASS: {sub_op_class} (count: {len(sub_op_class)})")
        else:
            logging.info(f"  SUB_OP_CLASS: None")

        remarks = entry.get("REMARKS")
        if remarks:
            logging.info(f"  REMARKS: {len(remarks)} remark(s)")
            for i, remark in enumerate(remarks[:3], 1):  # Show first 3
                logging.info(f"    [{i}] {remark[:200]}{'...' if len(remark) > 100 else ''}")
            if len(remarks) > 3:
                logging.info(f"    ... and {len(remarks) - 3} more")
        else:
            logging.info(f"  REMARKS: None")

        genotox_id = entry.get("GENOTOX_ID")
        if genotox_id:
            logging.info(f"  GENOTOX_ID: {genotox_id} (count: {len(genotox_id)})")
        else:
            logging.info(f"  GENOTOX_ID: None")

        tox_id = entry.get("TOX_ID")
        if tox_id:
            logging.info(f"  TOX_ID: {tox_id} (count: {len(tox_id)})")
        else:
            logging.info(f"  TOX_ID: None")

        hazard_id = entry.get("HAZARD_ID")
        if hazard_id:
            logging.info(f"  HAZARD_ID: {hazard_id} (count: {len(hazard_id)})")
        else:
            logging.info(f"  HAZARD_ID: None")

        op_id = entry.get("OP_ID")
        if op_id:
            logging.info(f"  OP_ID: {op_id} (count: {len(op_id)})")
        else:
            logging.info(f"  OP_ID: None")

    logging.info(f"\n" + "=" * 80)
    logging.info(f"Test complete. Total entries: {len(results)}")
    logging.info(f"=" * 80)
