from typing import Union
from src.mcp_openfoodtox.database.queries import query_by_id


def get_toxicity_endpoints(tox_id: Union[int, list[int]]):
    """
    Get toxicity endpoint study data from ENDPOINT_STUDY table by TOX_ID.

    Retrieves detailed toxicity endpoint records including NOAEL, LD50, and other
    toxicity measurements from animal and in vitro studies. This tool provides the
    experimental data used to assess the toxicological effects of food substances.

    Args:
        tox_id: Single TOX_ID (int) or list of TOX_IDs (list[int]) to query.
               Use search_substance tool first to find TOX_IDs through the STUDY table.

    Returns:
        JSON string containing a DataFrame with toxicity endpoint records. Each record
        includes endpoint type, toxicity values, study conditions, and target organs.

    The returned data includes:
    - Endpoint information: ENDPOINT, ENDPOINT_CODE (e.g., NOAEL, LD50, LOAEL)
    - Toxicity values: VALUE, VALUE_MILLI, DOSEUNIT, DOSEUNITFULLTEXT
    - Qualifier: QUALIFIER (e.g., "greater than", "less than")
    - Study conditions: SPECIES, STRAIN, SEX, ROUTE, EXP_DURATION, DURATIONUNIT
    - Target information: TARGETTISSUE, EFFECT_DESC
    - Toxicity classification: TOXICITY (e.g., "acute", "chronic")
    - Study details: TESTTYPE, GUIDELINE, GLP_COMPL, REMARKS

    Note: Multiple records may be returned if multiple TOX_IDs are provided or if
    a single study has multiple endpoints measured.

    <dictionary_descriptions>
    <name>STUDY_CATEGORY</name>
    <description>Indicates the reason for testing Human health, Exotoxicology, Animal health (target) or Animal health (non target)</description>
    <name>TESTSUBSTANCE</name>
    <description>Description of the test material used in the toxocological study</description>
    <name>TESTTYPE_CODE</name>
    <description>Transmission code for the type of toxicological test</description>
    <name>SPECIES_ID</name>
    <description>Internal unique identifier of organism/cell culture used in the toxicological study</description>
    <name>SPECIES</name>
    <description>Description of the organism/cell culture used in the toxicological study</description>
    <name>SEX</name>
    <description>Indicates the sex of tested animals</description>
    <name>NUMBER_INDIVIDUALS</name>
    <description>Number of organisms dosed at each dose level of the toxicological study</description>
    <name>CONTROL</name>
    <description>Indicates whether and what type of concurrent control groups were used</description>
    <name>EFFECT_DESC</name>
    <description>Description of the effects observed in the toxicological study</description>
    <name>REMARKS</name>
    <description>Additional remarks on toxicological study. Free text on hazard assessment including (if necessary): 1) short explanation on how the study has been carried on; 2) any conclusions on the hazard identication (for example, explanation on why an hazard could not be identified)</description>
    </dictionary_descriptions>
    """
    df = query_by_id(tox_id, "endpoint_study")
    return df.to_json()
