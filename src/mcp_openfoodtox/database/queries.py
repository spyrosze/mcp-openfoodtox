import logging
from typing import Literal, Optional, Union
import pandas as pd
from pandas import DataFrame
from src.mcp_openfoodtox.database.connection import get_connection
from src.mcp_openfoodtox.utils.formatting import normalize_e_number

logger = logging.getLogger(__name__)


def query_by_compound(description_search):
    """
    Convenience Tools (pre-composed for common patterns)
    Query the OpenFoodTox database by compound description.

    Searches both SYNONYM and COMPONENT tables:
    - First searches SYNONYM.DESCRIPTION (E-numbers, common names, trade names)
    - If no results, searches COMPONENT.SUB_NAME and COMPONENT.COM_NAME (authoritative chemical names)

    Args:
        description_search: String to search in synonym.DESCRIPTION or component names (case-insensitive)

    Returns:
        Dictionary with dataframes for each level of the hierarchy, or None if no matches found
    """
    # Normalize the search query (especially for E-numbers)
    normalized_search = normalize_e_number(description_search)
    if normalized_search != description_search:
        logger.info(f"Normalized search query: '{description_search}' -> '{normalized_search}'")

    with get_connection() as db_connection:
        # Start with SYNONYM search
        synonyms = pd.read_sql_query(
            """
            SELECT * FROM synonym 
            WHERE DESCRIPTION LIKE ?
            """,
            db_connection,
            params=[f"%{normalized_search}%"],
        )
        logger.debug(f"SYNONYM query returned {len(synonyms)} rows, shape: {synonyms.shape}")

        # If SYNONYM search is empty, try COMPONENT table
        if synonyms.empty:
            # Search COMPONENT.SUB_NAME and COMPONENT.COM_NAME
            components_from_search = pd.read_sql_query(
                """
                SELECT DISTINCT SUB_COM_ID 
                FROM component 
                WHERE SUB_NAME LIKE ? OR COM_NAME LIKE ?
                """,
                db_connection,
                params=[f"%{normalized_search}%", f"%{normalized_search}%"],
            )
            logger.debug(
                f"COMPONENT search returned {len(components_from_search)} unique SUB_COM_IDs, shape: {components_from_search.shape}"
            )

            if components_from_search.empty:
                # No matches found in either table
                return None

            # Extract SUB_COM_IDs from COMPONENT search
            sub_com_ids = [int(x) for x in components_from_search["SUB_COM_ID"].unique()]

            # Create empty synonyms DataFrame (since we found via COMPONENT, not SYNONYM)
            synonyms = pd.DataFrame()
        else:
            # Get unique SUB_COM_IDs from SYNONYM search
            sub_com_ids = [int(x) for x in synonyms["SUB_COM_ID"].unique()]

        # Join COMPONENT → get full component details
        components = pd.read_sql_query(
            f"""
            SELECT * FROM component 
            WHERE SUB_COM_ID IN ({','.join('?' * len(sub_com_ids))})
            """,
            db_connection,
            params=sub_com_ids,
        )
        logger.debug(f"COMPONENT query returned {len(components)} rows, shape: {components.shape}")

        # Join COMPONENT → STUDY
        studies = pd.read_sql_query(
            f"""
            SELECT * FROM study 
            WHERE SUB_COM_ID IN ({','.join('?' * len(sub_com_ids))})
            """,
            db_connection,
            params=sub_com_ids,
        )
        logger.debug(f"STUDY query returned {len(studies)} rows, shape: {studies.shape}")

        # Get the three study types
        genotox = pd.DataFrame()
        endpoint_study = pd.DataFrame()
        chem_assess = pd.DataFrame()
        opinions = pd.DataFrame()
        questions = pd.DataFrame()

        if not studies.empty:
            # STUDY → GENOTOX
            genotox_ids = [int(x) for x in studies["GENOTOX_ID"].dropna().unique()]
            if len(genotox_ids) > 0:
                genotox = pd.read_sql_query(
                    f"""
                    SELECT * FROM genotox 
                    WHERE GENOTOX_ID IN ({','.join('?' * len(genotox_ids))})
                    """,
                    db_connection,
                    params=genotox_ids,
                )
                logger.debug(f"GENOTOX query returned {len(genotox)} rows, shape: {genotox.shape}")

            # STUDY → ENDPOINT_STUDY
            tox_ids = [int(x) for x in studies["TOX_ID"].dropna().unique()]
            if len(tox_ids) > 0:
                endpoint_study = pd.read_sql_query(
                    f"""
                    SELECT * FROM endpoint_study 
                    WHERE TOX_ID IN ({','.join('?' * len(tox_ids))})
                    """,
                    db_connection,
                    params=tox_ids,
                )
                logger.debug(
                    f"ENDPOINT_STUDY query returned {len(endpoint_study)} rows, shape: {endpoint_study.shape}"
                )

            # STUDY → CHEM_ASSESS
            hazard_ids = [int(x) for x in studies["HAZARD_ID"].dropna().unique()]
            if len(hazard_ids) > 0:
                chem_assess = pd.read_sql_query(
                    f"""
                    SELECT * FROM chem_assess 
                    WHERE HAZARD_ID IN ({','.join('?' * len(hazard_ids))})
                    """,
                    db_connection,
                    params=hazard_ids,
                )
                logger.debug(
                    f"CHEM_ASSESS query returned {len(chem_assess)} rows, shape: {chem_assess.shape}"
                )

            # STUDY → OPINION
            op_ids = [int(x) for x in studies["OP_ID"].dropna().unique()]

            if len(op_ids) > 0:
                opinions = pd.read_sql_query(
                    f"""
                    SELECT * FROM opinion 
                    WHERE OP_ID IN ({','.join('?' * len(op_ids))})
                    """,
                    db_connection,
                    params=op_ids,
                )
                logger.debug(
                    f"OPINION query returned {len(opinions)} rows, shape: {opinions.shape}"
                )

                # OPINION → QUESTION
                questions = pd.read_sql_query(
                    f"""
                    SELECT * FROM question 
                    WHERE OP_ID IN ({','.join('?' * len(op_ids))})
                    """,
                    db_connection,
                    params=op_ids,
                )
                logger.debug(
                    f"QUESTION query returned {len(questions)} rows, shape: {questions.shape}"
                )

        result = {
            "synonyms": synonyms,
            "components": components,
            "studies": studies,
            "genotox": genotox,
            "endpoint_study": endpoint_study,
            "chem_assess": chem_assess,
            "opinions": opinions,
            "questions": questions,
        }

        # Log summary of all returned dataframes
        logger.info(
            f"Query results summary - synonyms: {len(synonyms)}, components: {len(components)}, "
            f"studies: {len(studies)}, genotox: {len(genotox)}, endpoint_study: {len(endpoint_study)}, "
            f"chem_assess: {len(chem_assess)}, opinions: {len(opinions)}, questions: {len(questions)}"
        )

        return result


def query_search_substance(description_search) -> Optional[list[dict]]:
    """
    Atomic query function.
    Database-agnostic search function.

    Returns unique substance/es (by SUB_COM_ID) with all study data aggregated into arrays.
    """
    normalized_search = normalize_e_number(description_search)

    with get_connection() as db_connection:
        # Step 1: Find SUB_COM_IDs (database-agnostic via pandas)
        synonyms = pd.read_sql_query(
            "SELECT DISTINCT SUB_COM_ID FROM synonym WHERE DESCRIPTION LIKE ?",
            db_connection,
            params=[f"%{normalized_search}%"],
        )

        sub_com_ids = synonyms["SUB_COM_ID"].unique().tolist()

        if not sub_com_ids:
            # Try component search...
            components = pd.read_sql_query(
                "SELECT DISTINCT SUB_COM_ID FROM component WHERE SUB_NAME LIKE ? OR COM_NAME LIKE ?",
                db_connection,
                params=[f"%{normalized_search}%", f"%{normalized_search}%"],
            )
            if components.empty:
                return None
            sub_com_ids = components["SUB_COM_ID"].unique().tolist()

        # Step 2: Get unique component info (one row per SUB_COM_ID)
        placeholders = ",".join("?" * len(sub_com_ids))
        component_query = f"""
            SELECT DISTINCT
                SUB_COM_ID,
                COM_NAME,
                COM_TYPE,
                MOLECULARFORMULA,
                SUB_DESCRIPTION
            FROM component
            WHERE SUB_COM_ID IN ({placeholders})
        """
        components_df = pd.read_sql_query(component_query, db_connection, params=sub_com_ids)

        # Step 3: Get all studies for these SUB_COM_IDs
        study_query = f"""
            SELECT 
                SUB_COM_ID,
                SUB_OP_CLASS,
                REMARKS_STUDY,
                GENOTOX_ID,
                TOX_ID,
                HAZARD_ID,
                OP_ID
            FROM study
            WHERE SUB_COM_ID IN ({placeholders})
        """
        studies_df = pd.read_sql_query(study_query, db_connection, params=sub_com_ids)

        # Step 4: Group studies by SUB_COM_ID and aggregate into arrays
        result = []

        for _, component_row in components_df.iterrows():
            sub_com_id = component_row["SUB_COM_ID"]

            # Get all studies for this component
            component_studies = studies_df[studies_df["SUB_COM_ID"] == sub_com_id]

            # Helper function to convert to array, filtering out None/NaN
            def to_array_or_none(series):
                """Convert pandas series to list of non-null values, or None if empty."""
                values = series.dropna().unique().tolist()
                # Convert numpy types to native Python types
                cleaned = []
                for val in values:
                    if pd.notna(val):
                        if hasattr(val, "item"):
                            cleaned.append(val.item())
                        else:
                            cleaned.append(val)
                return cleaned if cleaned else None

            # Helper function for string arrays (like SUB_OP_CLASS, REMARKS)
            def to_string_array_or_none(series):
                """Convert pandas series to list of non-null strings, or None if empty."""
                values = series.dropna().unique().tolist()
                cleaned = [str(v) for v in values if pd.notna(v) and str(v).strip()]
                return cleaned if cleaned else None

            # Helper to safely get value or None
            def safe_get(val):
                """Get value if not null, else None."""
                try:
                    if pd.isna(val):
                        return None
                    if hasattr(val, "item"):
                        return val.item()
                    return val
                except (TypeError, ValueError):
                    return None

            # Build result entry
            entry = {
                "SUB_COM_ID": int(sub_com_id),
                "COM_NAME": safe_get(component_row["COM_NAME"]),
                "COM_TYPE": safe_get(component_row["COM_TYPE"]),
                "MOLECULARFORMULA": safe_get(component_row["MOLECULARFORMULA"]),
                "SUB_DESCRIPTION": safe_get(component_row["SUB_DESCRIPTION"]),
            }

            if not component_studies.empty:
                # Aggregate study fields into arrays
                entry["SUB_OP_CLASS"] = to_string_array_or_none(component_studies["SUB_OP_CLASS"])
                entry["REMARKS"] = to_string_array_or_none(component_studies["REMARKS_STUDY"])
                entry["GENOTOX_ID"] = to_array_or_none(component_studies["GENOTOX_ID"])
                entry["TOX_ID"] = to_array_or_none(component_studies["TOX_ID"])
                entry["HAZARD_ID"] = to_array_or_none(component_studies["HAZARD_ID"])
                entry["OP_ID"] = to_array_or_none(component_studies["OP_ID"])
            else:
                # No studies found for this component
                entry["SUB_OP_CLASS"] = None
                entry["REMARKS"] = None
                entry["GENOTOX_ID"] = None
                entry["TOX_ID"] = None
                entry["HAZARD_ID"] = None
                entry["OP_ID"] = None

            result.append(entry)

        return result


def query_safety_assessment(sub_com_id) -> DataFrame:
    """
    Get the safety assessment for a given SUB_COM_ID.
    Returns safety assessment fields from the STUDY table, joined with OPINION for dates and metadata.
    Results are sorted chronologically by PUBLICATIONDATE.
    """
    with get_connection() as db_connection:
        safety_assessment = pd.read_sql_query(
            """
            SELECT 
                s.SUB_OP_CLASS,
                s.IS_MUTAGENIC,
                s.IS_GENOTOXIC,
                s.IS_CARCINOGENIC,
                s.REMARKS_STUDY,
                s.TOXREF_ID,
                s.OP_ID,
                o.ADOPTIONDATE,
                o.PUBLICATIONDATE,
                o.AUTHOR,
                o.TITLE
            FROM study s
            LEFT JOIN opinion o ON s.OP_ID = o.OP_ID
            WHERE s.SUB_COM_ID = ?
            ORDER BY o.PUBLICATIONDATE ASC
            """,
            db_connection,
            params=[sub_com_id],
        )
        return safety_assessment


def query_by_id(id_value: Union[int, list[int]], table_name: str) -> DataFrame:
    """
    Generic query function that retrieves records from a table by unique ID(s).

    Only works with tables where the ID column is unique (one row per ID).
    Tables with non-unique IDs (synonym, study, question) are not supported.

    Args:
        id_value: Single ID (int) or list of IDs (list[int]) to query.
                 IDs correspond to: TOX_ID, GENOTOX_ID, HAZARD_ID, OP_ID, SUB_COM_ID
        table_name: The target table name (case-insensitive). Supported:
            - endpoint_study (TOX_ID)
            - genotox (GENOTOX_ID)
            - chem_assess (HAZARD_ID)
            - opinion (OP_ID)
            - component (SUB_COM_ID)

    Returns:
        DataFrame with matching records, all data (columns) (0 to N rows, where N = number of IDs provided),
        or empty DataFrame if no matches
    """
    table_name_lower = table_name.lower()

    # Tables that are not supported (non-unique IDs)
    unsupported_tables = {
        "synonym": "SYNONYM has multiple rows per SUB_COM_ID (one substance can have many synonyms).",
        "study": "STUDY has multiple rows per SUB_COM_ID (one substance can have many studies).",
        "question": "QUESTION has multiple rows per OP_ID (one opinion can have many questions).",
    }

    if table_name_lower in unsupported_tables:
        error_msg = (
            f"Table '{table_name}' is not supported by query_by_id(). "
            f"{unsupported_tables[table_name_lower]}"
        )
        logger.warning(error_msg)
        raise ValueError(error_msg)

    # Map table names to their ID columns (only tables with unique IDs)
    id_column_map = {
        "endpoint_study": "TOX_ID",
        "genotox": "GENOTOX_ID",
        "chem_assess": "HAZARD_ID",
        "opinion": "OP_ID",
        "component": "SUB_COM_ID",
    }

    if table_name_lower not in id_column_map:
        error_msg = (
            f"Unknown table name: {table_name}. "
            f"Supported tables: {', '.join(sorted(id_column_map.keys()))}"
        )
        logger.warning(error_msg)
        raise ValueError(error_msg)

    id_column = id_column_map[table_name_lower]

    # Normalize to list
    if isinstance(id_value, int):
        id_list = [id_value]
    elif isinstance(id_value, list):
        if not id_value:
            logger.warning("Empty ID list provided, returning empty DataFrame")
            return pd.DataFrame()
        id_list = id_value
    else:
        raise TypeError(f"id_value must be int or list[int], got {type(id_value)}")

    with get_connection() as db_connection:
        try:
            # Use IN clause for multiple IDs, = for single ID
            if len(id_list) == 1:
                query = f"SELECT * FROM {table_name_lower} WHERE {id_column} = ?"
                params = [id_list[0]]
            else:
                placeholders = ",".join("?" * len(id_list))
                query = f"SELECT * FROM {table_name_lower} WHERE {id_column} IN ({placeholders})"
                params = id_list

            result = pd.read_sql_query(query, db_connection, params=params)
            logger.debug(f"query_by_id({id_value}, {table_name}) returned {len(result)} rows")
            return result
        except Exception as e:
            logger.error(f"Error querying {table_name} by {id_column}={id_value}: {e}")
            return pd.DataFrame()


