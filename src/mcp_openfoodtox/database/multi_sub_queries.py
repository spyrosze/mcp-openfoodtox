import logging
from typing import Literal, Optional, Union
import pandas as pd
from pandas import DataFrame
from src.mcp_openfoodtox.database.connection import get_connection

logger = logging.getLogger(__name__)


def query_substances_by_class_and_safety(
    sub_class: Optional[str] = None,
    is_mutagenic: Optional[
        Literal[
            "Positive",
            "Negative",
            "Ambiguous",
            "No data",
            "Not applicable",
            "Not determined",
            "Other",
        ]
    ] = None,
    is_genotoxic: Optional[
        Literal[
            "Positive",
            "Negative",
            "Ambiguous",
            "No data",
            "Not applicable",
            "Not determined",
            "Other",
        ]
    ] = None,
    is_carcinogenic: Optional[
        Literal[
            "Positive",
            "Negative",
            "Ambiguous",
            "No data",
            "Not applicable",
            "Not determined",
            "Other",
        ]
    ] = None,
    remarks_contains: Optional[str] = None,
    limit: int = 10,
) -> dict:
    """
    Filter substances by STUDY criteria and join to COMPONENT and SYNONYM tables.

    Filters the STUDY table by optional criteria (SUB_OP_CLASS, IS_MUTAGENIC, IS_GENOTOXIC,
    IS_CARCINOGENIC, REMARKS_STUDY), then joins to COMPONENT to get substance details and
    to SYNONYM to get alternative names/E-numbers.

    Args:
        sub_class: Optional SUB_OP_CLASS filter. Accepts partial matches (case-insensitive LIKE).
                   Examples:
                   - "additives" matches "Food additives", "Nutritional additives", "Sensory additives", etc.
                   - "food" matches "Food additives", "Food contact materials"
                   - "pesticides" matches "Pesticides"
                   - "Food additives" (exact match also works)
                   Valid full values (all possible SUB_OP_CLASS values):
                   - "No category"
                   - "Cocciodiostats/Hormones/Histomonostats"
                   - "Persistent organic pollutants"
                   - "Natural plant product contaminants"
                   - "Mycotoxins"
                   - "Melamine"
                   - "Processing contaminants"
                   - "Marine biotoxins"
                   - "Heavy metal ions and metalloids"
                   - "Nutritional additives"
                   - "Sensory additives"
                   - "Technological additives"
                   - "Zootechnical additives"
                   - "Feed intended for particular nutritional purposes"
                   - "Food additives"
                   - "Food contact materials"
                   - "Processing aids"
                   - "Nutrient sources"
                   - "Pesticides"
                   - "Flavourings"
        is_mutagenic: Optional IS_MUTAGENIC filter (exact match: "Positive", "Negative", "Ambiguous", etc.)
        is_genotoxic: Optional IS_GENOTOXIC filter (exact match: "Positive", "Negative", "Ambiguous", etc.)
        is_carcinogenic: Optional IS_CARCINOGENIC filter (exact match: "Positive", "Negative", "Ambiguous", etc.)
        remarks_contains: Optional text search in REMARKS_STUDY (case-insensitive LIKE, substring match)
        limit: Maximum number of results to return (default: 10)

    Returns:
        Dictionary with:
        - 'results': DataFrame with columns: SUB_COM_ID, COM_NAME, COM_TYPE, SUB_TYPE, DESCRIPTION (synonym)
        - 'total_count': Total number of matching substances (before limit)

    Joins: STUDY → COMPONENT (by SUB_COM_ID) → SYNONYM (by SUB_COM_ID)
    Returns unique substances (DISTINCT by SUB_COM_ID).
    """
    with get_connection() as db_connection:
        # Build WHERE clause dynamically based on provided filters
        where_conditions = []
        params = []

        if sub_class is not None:
            # Use flexible LIKE matching (case-insensitive) for partial matches
            # Allows "additives" to match "Food additives", "Nutritional additives", etc.
            where_conditions.append("LOWER(s.SUB_OP_CLASS) LIKE ?")
            params.append(f"%{sub_class.lower()}%")

        if is_mutagenic is not None:
            where_conditions.append("s.IS_MUTAGENIC = ?")
            params.append(is_mutagenic)

        if is_genotoxic is not None:
            where_conditions.append("s.IS_GENOTOXIC = ?")
            params.append(is_genotoxic)

        if is_carcinogenic is not None:
            where_conditions.append("s.IS_CARCINOGENIC = ?")
            params.append(is_carcinogenic)

        if remarks_contains is not None:
            # Handle NULL values and use case-insensitive search
            # Lowercase both the column and the search term for reliable case-insensitive matching
            where_conditions.append("s.REMARKS_STUDY IS NOT NULL AND LOWER(s.REMARKS_STUDY) LIKE ?")
            params.append(f"%{remarks_contains.lower()}%")

        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

        # Log the query for debugging
        logger.debug(f"WHERE clause: {where_clause}")
        logger.debug(f"Query params: {params}")

        # First, get total count (before limit)
        count_query = f"""
            SELECT COUNT(DISTINCT s.SUB_COM_ID) as total_count
            FROM study s
            WHERE {where_clause}
        """
        total_count_df = pd.read_sql_query(count_query, db_connection, params=params)
        total_count = int(total_count_df.iloc[0]["total_count"])

        # Then get the limited results with joins
        # Use GROUP BY to handle multiple synonyms per substance
        # We'll aggregate synonyms into a comma-separated list
        # Note: GROUP_CONCAT(DISTINCT ...) doesn't support separator argument in SQLite
        # So we use DISTINCT without separator (defaults to comma)
        query = f"""
            SELECT
                s.SUB_COM_ID,
                c.COM_NAME,
                c.COM_TYPE,
                c.SUB_TYPE,
                GROUP_CONCAT(DISTINCT syn.DESCRIPTION) as DESCRIPTION
            FROM study s
            INNER JOIN component c ON s.SUB_COM_ID = c.SUB_COM_ID
            LEFT JOIN synonym syn ON s.SUB_COM_ID = syn.SUB_COM_ID
            WHERE {where_clause}
            GROUP BY s.SUB_COM_ID, c.COM_NAME, c.COM_TYPE, c.SUB_TYPE
            LIMIT ?
        """
        params_with_limit = params + [limit]

        result_df = pd.read_sql_query(query, db_connection, params=params_with_limit)

        logger.debug(
            f"list_substances_by_criteria returned {len(result_df)} rows "
            f"(total matching: {total_count})"
        )

        return {"results": result_df, "total_count": total_count}


# Dictionary mapping study types to their ID column names in STUDY table
STUDY_TYPE_TO_ID_COLUMN = {
    "genotox": "GENOTOX_ID",
    "tox": "TOX_ID",
    "endpoint_study": "TOX_ID",
    "hazard": "HAZARD_ID",
    "chem_assess": "HAZARD_ID",
    "opinion": "OP_ID",
}


def query_substances_by_study(
    ids: list[int],
    study_type: str,
    limit: int = 10,
) -> dict:
    """
    Filter substances by study IDs (GENOTOX_ID, TOX_ID, HAZARD_ID, or OP_ID) and join to COMPONENT and SYNONYM tables.

    Filters the STUDY table by the specified study type and ID array, then joins to COMPONENT to get
    substance details and to SYNONYM to get alternative names/E-numbers.

    Args:
        ids: Array of study IDs to filter by (e.g., [1, 2, 3] for GENOTOX_ID values)
        study_type: Type of study ID to filter by. Valid values:
                   - "genotox" → filters by GENOTOX_ID
                   - "tox" or "endpoint_study" → filters by TOX_ID
                   - "hazard" or "chem_assess" → filters by HAZARD_ID
                   - "opinion" → filters by OP_ID
        limit: Maximum number of results to return (default: 10)

    Returns:
        Dictionary with:
        - 'results': DataFrame with columns: SUB_COM_ID, COM_NAME, COM_TYPE, SUB_TYPE, DESCRIPTION (synonym)
        - 'total_count': Total number of matching substances (before limit)

    Joins: STUDY → COMPONENT (by SUB_COM_ID) → SYNONYM (by SUB_COM_ID)
    Returns unique substances (DISTINCT by SUB_COM_ID).

    Example:
        # Get substances from genotoxicity study IDs [1, 2, 3]
        result = list_substances_by_study(ids=[1, 2, 3], study_type="genotox")
    """
    if not ids:
        return {"results": pd.DataFrame(), "total_count": 0}

    # Look up the ID column name for the study type
    id_column = STUDY_TYPE_TO_ID_COLUMN.get(study_type.lower())
    if id_column is None:
        raise ValueError(
            f"Invalid study_type: {study_type}. "
            f"Valid values: {list(STUDY_TYPE_TO_ID_COLUMN.keys())}"
        )

    with get_connection() as db_connection:
        # Build WHERE clause: filter by the ID column with IN clause
        # Also need to check that the ID column is NOT NULL
        placeholders = ",".join("?" * len(ids))
        where_clause = f"s.{id_column} IS NOT NULL AND s.{id_column} IN ({placeholders})"

        # Log the query for debugging
        logger.debug(f"WHERE clause: {where_clause}")
        logger.debug(f"Query params: {ids}")

        # First, get total count (before limit)
        count_query = f"""
            SELECT COUNT(DISTINCT s.SUB_COM_ID) as total_count
            FROM study s
            WHERE {where_clause}
        """
        total_count_df = pd.read_sql_query(count_query, db_connection, params=ids)
        total_count = int(total_count_df.iloc[0]["total_count"])

        # Then get the limited results with joins
        # Use GROUP BY to handle multiple synonyms per substance
        # We'll aggregate synonyms into a comma-separated list
        query = f"""
            SELECT
                s.SUB_COM_ID,
                c.COM_NAME,
                c.COM_TYPE,
                c.SUB_TYPE,
                GROUP_CONCAT(DISTINCT syn.DESCRIPTION) as DESCRIPTION
            FROM study s
            INNER JOIN component c ON s.SUB_COM_ID = c.SUB_COM_ID
            LEFT JOIN synonym syn ON s.SUB_COM_ID = syn.SUB_COM_ID
            WHERE {where_clause}
            GROUP BY s.SUB_COM_ID, c.COM_NAME, c.COM_TYPE, c.SUB_TYPE
            LIMIT ?
        """
        params_with_limit = ids + [limit]

        result_df = pd.read_sql_query(query, db_connection, params=params_with_limit)

        logger.debug(
            f"list_substances_by_study returned {len(result_df)} rows "
            f"(total matching: {total_count}, study_type: {study_type}, id_column: {id_column})"
        )

        return {"results": result_df, "total_count": total_count}


def query_hazard_ids_by_assessment(
    population_text_contains: Optional[str] = None,
    assessment_type: Optional[str] = None,
    risk_value_milli_max: Optional[float] = None,
    risk_value_milli_min: Optional[float] = None,
    has_no_risk_value: Optional[bool] = None,
    limit: Optional[int] = None,
) -> list[int]:
    """
    Filter CHEM_ASSESS table by population, assessment type, and dosage thresholds.
    Returns list of HAZARD_IDs that match the criteria.

    This is a building block function - use the returned HAZARD_IDs with
    query_substances_by_study() to get the actual substances.

    Args:
        population_text_contains: Optional text search in POPULATIONTEXT (case-insensitive LIKE).
                                 Examples:
                                 - "children" matches "children under 3", "children 3-10", etc.
                                 - "pregnant" matches "pregnant women"
                                 - "infant" matches "infants"
        assessment_type: Optional ASSESSMENTTYPE filter (case-insensitive LIKE, partial match).
                         Examples: "ADI", "TDI", "ARfD", "group"
        risk_value_milli_max: Optional maximum RISKVALUE_MILLI (inclusive, <=).
                             Use for "low safe limits" queries.
        risk_value_milli_min: Optional minimum RISKVALUE_MILLI (inclusive, >=).
                             Use for "high safe limits" queries.
        has_no_risk_value: If True, only return HAZARD_IDs where RISKVALUE IS NULL.
                          Use to find assessments with no quantitative limit set.
        limit: Optional maximum number of HAZARD_IDs to return.

    Returns:
        List of HAZARD_IDs (integers) matching the criteria.

    Example:
        # Find all assessments for children with ADI < 1 mg/kg
        hazard_ids = query_hazard_ids_by_assessment(
            population_text_contains="children",
            assessment_type="ADI",
            risk_value_milli_max=1.0
        )
        # Then get substances:
        substances = query_substances_by_study(hazard_ids, study_type="hazard")
    """
    with get_connection() as db_connection:
        # Build WHERE clause dynamically based on provided filters
        where_conditions = []
        params = []

        if population_text_contains is not None:
            # Case-insensitive LIKE search in POPULATIONTEXT
            where_conditions.append("POPULATIONTEXT IS NOT NULL AND LOWER(POPULATIONTEXT) LIKE ?")
            params.append(f"%{population_text_contains.lower()}%")

        if assessment_type is not None:
            # Case-insensitive LIKE search in ASSESSMENTTYPE (allows partial matches)
            where_conditions.append("LOWER(ASSESSMENTTYPE) LIKE ?")
            params.append(f"%{assessment_type.lower()}%")

        if risk_value_milli_max is not None:
            # Maximum RISKVALUE_MILLI (inclusive)
            where_conditions.append("RISKVALUE_MILLI IS NOT NULL AND RISKVALUE_MILLI <= ?")
            params.append(risk_value_milli_max)

        if risk_value_milli_min is not None:
            # Minimum RISKVALUE_MILLI (inclusive)
            where_conditions.append("RISKVALUE_MILLI IS NOT NULL AND RISKVALUE_MILLI >= ?")
            params.append(risk_value_milli_min)

        if has_no_risk_value is True:
            # Only assessments with no quantitative risk value
            where_conditions.append("RISKVALUE IS NULL")

        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"

        # Log the query for debugging
        logger.debug(f"WHERE clause: {where_clause}")
        logger.debug(f"Query params: {params}")

        # Build query to get distinct HAZARD_IDs
        query = f"""
            SELECT DISTINCT HAZARD_ID
            FROM chem_assess
            WHERE {where_clause}
        """

        if limit is not None:
            query += f" LIMIT ?"
            params.append(limit)

        result_df = pd.read_sql_query(query, db_connection, params=params)

        # Extract HAZARD_IDs as list of integers
        hazard_ids = result_df["HAZARD_ID"].astype(int).tolist()

        logger.debug(f"query_hazard_ids_by_assessment returned {len(hazard_ids)} HAZARD_IDs")

        return hazard_ids
