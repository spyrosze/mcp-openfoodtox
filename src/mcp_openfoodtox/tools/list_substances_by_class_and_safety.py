from typing import Literal, Optional
from src.mcp_openfoodtox.database.multi_sub_queries import query_substances_by_class_and_safety


def list_substances_by_class_and_safety(
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
):
    """
    Retrieves substances from the EFSA OpenFoodTox database filtered by safety assessment
    criteria (mutagenicity, genotoxicity, carcinogenicity) and substance classification.
    This tool enables discovery of substances based on their safety profile and regulatory
    category, useful for comparative safety analysis and regulatory compliance queries.

    ## Example questions it can answer:
    ### Classification + Safety Status Queries
    By category:
    * "What food additives are genotoxic?"
    * "List pesticides that are carcinogenic"
    * "Show me flavourings that are mutagenic"
    * "What sensory additives have positive genotoxicity results?"
    ### Safety screening:
    "Which substances are both mutagenic and genotoxic?"
    * "Find substances that are positive for carcinogenicity"
    * "What additives have ambiguous safety data?"
    * "List substances with no mutagenicity data"
    ### Combined filters:
    * "What food additives are not genotoxic?" (Negative)
    * "Show pesticides that are not carcinogenic"
    * "List flavourings with ambiguous genotoxicity results"
    ### Regulatory & Compliance Queries
    "Which food additives have positive mutagenicity assessments?"
    * "What pesticides are flagged as genotoxic?"
    * "List substances in the 'Food additives' category with safety concerns"
    * "Show me technological additives that are not mutagenic"
    ### Research & Analysis Queries
    * "What substances have 'reproductive' in their study remarks?"
    * "Find additives with 'chronic' mentioned in remarks"
    * "List substances with 'developmental' toxicity in remarks"
    * "Show me substances where remarks contain 'neurotoxicity'"
    ### Comparative Safety Queries
    * "Compare all food additives by their genotoxicity status"
    * "Which category has the most substances with positive carcinogenicity?"
    "List all substances with positive results in any safety category"
    ### Data Quality Queries
    * "What substances have 'No data' for mutagenicity?"
    * "Show me substances with 'Not determined' safety assessments"
    * "List additives with incomplete safety data"

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
        JSON string containing a DataFrame with substance records. Each record includes
        substance identification, classification, and alternative names/E-numbers.
        The function also returns a total_count indicating how many substances match
        the criteria before the limit is applied.

    The returned data includes:
    - Substance identification: SUB_COM_ID (unique identifier)
    - Chemical details: COM_NAME (chemical name), COM_TYPE (single/mixture/botanical/synthetic)
    - Classification: SUB_TYPE (substance type qualifier)
    - Alternative names: DESCRIPTION (comma-separated synonyms, E-numbers, trade names)

    Joins: STUDY → COMPONENT (by SUB_COM_ID) → SYNONYM (by SUB_COM_ID)
    Returns unique substances (DISTINCT by SUB_COM_ID).

    Note: Multiple synonyms per substance are aggregated into a comma-separated list.
    Use the search_substance tool to get detailed information about specific substances
    from the results.
    """
    result = query_substances_by_class_and_safety(
        sub_class=sub_class,
        is_mutagenic=is_mutagenic,
        is_genotoxic=is_genotoxic,
        is_carcinogenic=is_carcinogenic,
        remarks_contains=remarks_contains,
        limit=limit,
    )
    return result["results"].to_json()
