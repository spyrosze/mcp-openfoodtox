from typing import Union
from src.mcp_openfoodtox.database.queries import query_by_id


def get_genotox_details(genotox_id: Union[int, list[int]]):
    """
    Get genotoxicity study details from GENOTOX table by GENOTOX_ID.

    Retrieves detailed genotoxicity study records including test methods, guidelines,
    and results. This tool provides the experimental data used to assess whether
    substances have genotoxic or mutagenic properties that could cause DNA damage.

    Args:
        genotox_id: Single GENOTOX_ID (int) or list of GENOTOX_IDs (list[int]) to query.
                   Use search_substance tool first to find GENOTOX_IDs through the STUDY table.

    Returns:
        JSON string containing a DataFrame with genotoxicity study records. Each record
        includes study category, test guidelines, species, exposure conditions, and
        genotoxicity results.

    The returned data includes:
    - Study category: STUDY_CATEGORY
    - Test guidelines: GENOTOXGUIDELINE, GENOTOXGUIDELINEFULLTXT
    - Test conditions: SPECIES, STRAIN, SEX, ROUTE, EXP_PERIOD, EXPPERIODUNIT
    - Genotoxicity result: IS_GENOTOXIC
    - Study quality: GLP_COMPL, DEVIATION
    - Study details: NUMBER_INDIVIDUALS, CONTROL, MET_INDICATOR, REMARKS

    Note: Multiple records may be returned if multiple GENOTOX_IDs are provided.
    Genotoxicity studies are critical for assessing cancer risk and mutagenic potential.

    <dictionary_descriptions>
    <name>STUDY_CATEGORY</name>
    <description>Mutagenicity or genotoxicity study</description>
    <name>SPECIES</name>
    <description>Description of the organism/cell culture tested</description>
    <name>SEX</name>
    <description>Sex of the tested animals in vivo genotoxicity study</description>
    <name>ROUTE</name>
    <description>Description of the route of administration</description>
    <name>NUMBER_INDIVIDUALS</name>
    <description>Number of organisms dosed at each dose level of the in vivo genotoxicty study</description>
    <name>CONTROL</name>
    <description>Indicates whether and what type of concurrent control groups were used in in vivo genotoxicity study</description>
    <name>IS_GENOTOXIC</name>
    <description>Positive or negative result</description>
    <name>REMARKS</name>
    <description>Remarks on genotoxicity study</description>
    </dictionary_descriptions>
    """
    df = query_by_id(genotox_id, "genotox")
    return df.to_json()
