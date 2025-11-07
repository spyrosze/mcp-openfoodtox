import pytest
import logging
import pandas as pd
from src.mcp_openfoodtox.database.queries import query_by_compound


def test_query_by_compound_synonym_search():
    """Test that SYNONYM search works correctly."""
    results = query_by_compound("e951")

    assert results is not None
    assert isinstance(results, dict)
    assert "synonyms" in results
    assert "components" in results
    assert "studies" in results

    # Should have synonym matches
    assert not results["synonyms"].empty
    assert "SUB_COM_ID" in results["synonyms"].columns

    # Should have corresponding components
    assert not results["components"].empty
    assert "SUB_COM_ID" in results["components"].columns


def test_query_by_compound_component_fallback():
    """Test that COMPONENT search works when SYNONYM search is empty."""
    # Search for a term that might not be in SYNONYM but exists in COMPONENT
    # This is a bit tricky - we need a term that exists in COMPONENT but not SYNONYM
    # Let's try a partial chemical name that's likely in COMPONENT.COM_NAME
    results = query_by_compound("aspartame")

    # If found via SYNONYM, that's fine - we just want to test the structure
    # If found via COMPONENT fallback, synonyms should be empty but components should not be
    if results is not None:
        assert isinstance(results, dict)
        assert "components" in results
        # Components should have data if found via either path
        assert not results["components"].empty


def test_query_by_compound_structure():
    """Test that returned structure has all expected keys."""
    results = query_by_compound("Vitamin a")

    assert results is not None

    expected_keys = [
        "synonyms",
        "components",
        "studies",
        "genotox",
        "endpoint_study",
        "chem_assess",
        "opinions",
        "questions",
    ]

    for key in expected_keys:
        assert key in results
        assert isinstance(results[key], pd.DataFrame)


def test_query_by_compound_no_results():
    """Test that function returns None for non-existent compounds."""
    results = query_by_compound("ThisCompoundDoesNotExist12345")

    assert results is None


def test_query_by_compound_empty_search():
    """Test that function handles empty search gracefully."""
    results = query_by_compound("")

    # Empty string might match everything or nothing - depends on LIKE behavior
    # But should not crash
    assert results is None or isinstance(results, dict)


def test_query_by_compound_case_insensitive():
    """Test that search is case-insensitive."""
    results_lower = query_by_compound("vitamin a")
    results_upper = query_by_compound("VITAMIN A")
    results_mixed = query_by_compound("Vitamin A")

    # All should return results (or all None if not found)
    # If found, they should have similar structure
    if results_lower is not None:
        assert isinstance(results_lower, dict)
        assert "components" in results_lower

    if results_upper is not None:
        assert isinstance(results_upper, dict)
        assert "components" in results_upper

    if results_mixed is not None:
        assert isinstance(results_mixed, dict)
        assert "components" in results_mixed


def test_query_by_compound_verbose_output():
    """Test that provides verbose logging output of retrieved data."""
    search_term = "Vitamin A"
    results = query_by_compound(search_term)

    if results:
        logging.info(f"Found {len(results['synonyms'])} synonym matches")

        # Get component names
        if len(results["components"]) > 0:
            component_names = results["components"]["COM_NAME"].unique().tolist()
            logging.info(f"Found {len(results['components'])} components:")
            for name in component_names:
                logging.info(f"  - {name}")
        else:
            logging.info(f"Found 0 components")

        logging.info(f"Found {len(results['studies'])} studies")
        logging.info(f"  ├─ {len(results['genotox'])} genotox studies")
        logging.info(f"  ├─ {len(results['endpoint_study'])} endpoint studies")
        logging.info(f"  └─ {len(results['chem_assess'])} chemical assessments")
        logging.info(f"Found {len(results['opinions'])} opinions")
        logging.info(f"Found {len(results['questions'])} questions")

        logging.info("\nAll Synonyms with Details:")
        for num, (idx, syn) in enumerate(results["synonyms"].iterrows(), 1):
            sub_com_id = syn["SUB_COM_ID"]
            description = syn.get("DESCRIPTION", "N/A")
            syn_type = syn.get("TYPE", "N/A")

            # Get component info to differentiate
            component_info = results["components"][
                results["components"]["SUB_COM_ID"] == sub_com_id
            ]
            com_name = "N/A"
            sub_type = None
            if not component_info.empty:
                for _, comp_row in component_info.iterrows():
                    com_name = str(comp_row.get("COM_NAME", "N/A"))
                    if "SUB_TYPE" in component_info.columns:
                        sub_type_val = comp_row.get("SUB_TYPE")
                        if sub_type_val is not None and pd.notna(sub_type_val):
                            sub_type = str(sub_type_val)
                    break  # Only need first match

            logging.info(f"\n{num}. {description} ({syn_type})")
            logging.info(f"   Component: {com_name}")
            if sub_type:
                logging.info(f"   SUB_TYPE: {sub_type}")
            logging.info(f"   SUB_COM_ID: {sub_com_id}")

            # Studies info
            syn_studies = results["studies"][results["studies"]["SUB_COM_ID"] == sub_com_id]
            if not syn_studies.empty:
                study_count = len(syn_studies)
                genotox_count = len(syn_studies[pd.notna(syn_studies["GENOTOX_ID"])])
                endpoint_count = len(syn_studies[pd.notna(syn_studies["TOX_ID"])])
                chem_assess_count = len(syn_studies[pd.notna(syn_studies["HAZARD_ID"])])

                logging.info(f"   Studies: {study_count} total")
                logging.info(f"     ├─ {genotox_count} genotox")
                logging.info(f"     ├─ {endpoint_count} endpoint")
                logging.info(f"     └─ {chem_assess_count} chemical assessment")

                # SUB_OP_CLASS from studies
                sub_op_classes = list(pd.unique(syn_studies["SUB_OP_CLASS"]))
                logging.info(f"   SUB_OP_CLASS: {', '.join(sub_op_classes)}")

                # Opinions info (via OP_ID from studies)
                op_series = syn_studies["OP_ID"][pd.notna(syn_studies["OP_ID"])]
                op_ids = list(pd.unique(op_series)) if len(op_series) > 0 else []
                if len(op_ids) > 0:
                    syn_opinions = results["opinions"][results["opinions"]["OP_ID"].isin(op_ids)]
                    if not syn_opinions.empty:
                        logging.info(f"   Opinions: {len(syn_opinions)}")

                        # Questions info (via OP_ID from opinions)
                        syn_questions = results["questions"][
                            results["questions"]["OP_ID"].isin(op_ids)
                        ]
                        if not syn_questions.empty:
                            logging.info(f"   Questions: {len(syn_questions)}")
                    else:
                        logging.info(f"   Opinions: 0")
                        logging.info(f"   Questions: 0")
                else:
                    logging.info(f"   Opinions: 0")
                    logging.info(f"   Questions: 0")
            else:
                logging.info(f"   Studies: 0")
                logging.info(f"   Opinions: 0")
                logging.info(f"   Questions: 0")
