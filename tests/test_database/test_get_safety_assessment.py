import pytest
import logging
import pandas as pd
import json
from pprint import pprint
from src.mcp_openfoodtox.database.queries import query_safety_assessment, query_search_substance

# Configure logging to see output
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)8s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def test_get_safety_assessment_log_output():
    """Test get_safety_assessment and log results for review.
    run with:
    `uv run pytest tests/test_database/test_get_safety_assessment.py::test_get_safety_assessment_log_output -v -s`
    """
    # Toggle: Set to True to see raw DataFrame structure, False for detailed logging
    SHOW_RAW_STRUCTURE = True

    # First, find a substance to test with
    search_term = "aspartame"

    logging.info(f"=" * 80)
    logging.info(f"Step 1: Finding SUB_COM_ID for '{search_term}'")
    logging.info(f"=" * 80)

    search_results = query_search_substance(search_term)

    if search_results is None or len(search_results) == 0:
        logging.warning(f"No results found for '{search_term}', trying 'E951' instead")
        search_results = query_search_substance("E951")

    if search_results is None or len(search_results) == 0:
        logging.error("Could not find any substance to test with")
        pytest.skip("No test substance found")

    # Get the first SUB_COM_ID from results
    sub_com_id = search_results[0].get("SUB_COM_ID")
    substance_name = search_results[0].get("COM_NAME", "Unknown")

    logging.info(f"Found SUB_COM_ID: {sub_com_id}")
    logging.info(f"Substance: {substance_name}")
    logging.info(f"\n" + "=" * 80)

    # Now test get_safety_assessment
    logging.info(f"Step 2: Getting safety assessment for SUB_COM_ID={sub_com_id}")
    logging.info(f"=" * 80)

    results = query_safety_assessment(sub_com_id)

    if results is None or results.empty:
        logging.info("No safety assessment data found (returned empty DataFrame)")
        logging.info(f"=" * 80)
        return

    # Conditional: Show raw structure OR detailed logging
    if SHOW_RAW_STRUCTURE:
        logging.info(f"=" * 80)
        logging.info(f"RAW DATAFRAME STRUCTURE")
        logging.info(f"=" * 80)
        logging.info(f"\nDataFrame type: {type(results)}")
        logging.info(f"Shape: {results.shape}")

        # Memory size in MB
        memory_usage_bytes = results.memory_usage(deep=True).sum()
        memory_usage_mb = memory_usage_bytes / (1024 * 1024)
        logging.info(f"Memory usage: {memory_usage_mb:.4f} MB ({memory_usage_bytes:,} bytes)")

        logging.info(f"\nColumns: {list(results.columns)}")

        # Convert to dict and pretty print
        logging.info(f"\n" + "=" * 80)
        logging.info(f"DATAFRAME AS DICT (pretty printed):")
        logging.info(f"=" * 80)

        # Convert DataFrame to dict using 'records' orientation (list of dicts)
        dict_data = results.to_dict(orient="records")
        logging.info(f"\nDict representation (type: {type(dict_data)}, length: {len(dict_data)})")

        # Pretty print using json for better formatting
        logging.info(f"\nPretty printed JSON:")
        logging.info(f"\n{json.dumps(dict_data, indent=2, default=str)}")

        logging.info(f"\n" + "=" * 80)
        return

    logging.info(f"\nFound {len(results)} study record(s) with safety assessment data")
    logging.info(f"\n" + "-" * 80)

    # Log each row
    for idx, row in results.iterrows():
        record_num = int(idx) + 1 if isinstance(idx, (int, float)) else 1
        logging.info(f"\nStudy Record {record_num}:")

        # Opinion metadata (from JOIN)
        op_id = row.get("OP_ID")
        if op_id is not None and pd.notna(op_id):
            logging.info(f"  OP_ID: {op_id}")

        title = row.get("TITLE")
        if title is not None and pd.notna(title):
            title_str = str(title)
            if len(title_str) > 150:
                logging.info(f"  Opinion Title: {title_str[:150]}...")
            else:
                logging.info(f"  Opinion Title: {title_str}")

        author = row.get("AUTHOR")
        if author is not None and pd.notna(author):
            logging.info(f"  Author: {author}")

        adoption_date = row.get("ADOPTIONDATE")
        if adoption_date is not None and pd.notna(adoption_date):
            logging.info(f"  Adoption Date: {adoption_date}")

        publication_date = row.get("PUBLICATIONDATE")
        if publication_date is not None and pd.notna(publication_date):
            logging.info(f"  Publication Date: {publication_date}")

        logging.info(f"  --- Safety Assessment ---")
        logging.info(f"  SUB_OP_CLASS: {row.get('SUB_OP_CLASS', 'N/A')}")
        logging.info(f"  IS_MUTAGENIC: {row.get('IS_MUTAGENIC', 'N/A')}")
        logging.info(f"  IS_GENOTOXIC: {row.get('IS_GENOTOXIC', 'N/A')}")
        logging.info(f"  IS_CARCINOGENIC: {row.get('IS_CARCINOGENIC', 'N/A')}")

        remarks = row.get("REMARKS_STUDY")
        remarks_value = None
        if remarks is not None and pd.notna(remarks):
            remarks_value = remarks
        if remarks_value is not None and str(remarks_value).strip():
            remarks_str = str(remarks_value)
            if len(remarks_str) > 200:
                logging.info(f"  REMARKS_STUDY: {remarks_str[:200]}...")
            else:
                logging.info(f"  REMARKS_STUDY: {remarks_str}")
        else:
            logging.info(f"  REMARKS_STUDY: None")

        toxref_id = row.get("TOXREF_ID")
        toxref_value = None
        if toxref_id is not None and pd.notna(toxref_id):
            toxref_value = toxref_id
        if toxref_value is not None:
            logging.info(f"  TOXREF_ID: {toxref_value}")
        else:
            logging.info(f"  TOXREF_ID: None")

    # Summary statistics
    logging.info(f"\n" + "-" * 80)
    logging.info(f"Summary Statistics:")
    logging.info(f"  Total records: {len(results)}")

    # Opinion statistics
    if "OP_ID" in results.columns:
        unique_opinions = results["OP_ID"].dropna().unique()
        logging.info(f"  Unique opinions (OP_ID): {len(unique_opinions)}")

    if "PUBLICATIONDATE" in results.columns:
        pub_dates = results["PUBLICATIONDATE"].dropna()
        if len(pub_dates) > 0:
            earliest = pub_dates.min()
            latest = pub_dates.max()
            logging.info(f"  Publication date range: {earliest} to {latest}")

    # Count unique values
    if "SUB_OP_CLASS" in results.columns:
        unique_classes = results["SUB_OP_CLASS"].dropna().unique().tolist()
        logging.info(f"  SUB_OP_CLASS values: {', '.join(map(str, unique_classes))}")

    if "IS_MUTAGENIC" in results.columns:
        mutagenic_counts = results["IS_MUTAGENIC"].value_counts().to_dict()
        logging.info(f"  IS_MUTAGENIC distribution: {mutagenic_counts}")

    if "IS_GENOTOXIC" in results.columns:
        genotoxic_counts = results["IS_GENOTOXIC"].value_counts().to_dict()
        logging.info(f"  IS_GENOTOXIC distribution: {genotoxic_counts}")

    if "IS_CARCINOGENIC" in results.columns:
        carcinogenic_counts = results["IS_CARCINOGENIC"].value_counts().to_dict()
        logging.info(f"  IS_CARCINOGENIC distribution: {carcinogenic_counts}")

    # Count non-null values
    remarks_count = results["REMARKS_STUDY"].notna().sum()
    logging.info(f"  Records with REMARKS_STUDY: {remarks_count}/{len(results)}")

    toxref_count = results["TOXREF_ID"].notna().sum()
    logging.info(f"  Records with TOXREF_ID: {toxref_count}/{len(results)}")

    logging.info(f"\n" + "=" * 80)
    logging.info(f"Test complete. Total records: {len(results)}")
    logging.info(f"=" * 80)
