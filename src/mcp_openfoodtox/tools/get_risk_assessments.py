from typing import Union
from src.mcp_openfoodtox.database.queries import query_by_id


def get_risk_assessments(hazard_id: Union[int, list[int]]):
    """
    Get risk assessment data from CHEM_ASSESS table by HAZARD_ID.

    Retrieves comprehensive risk assessment records including ADI (Acceptable Daily Intake),
    TDI (Tolerable Daily Intake), and other safety limit values. This tool provides the
    quantitative safety assessments used by EFSA to establish safe intake levels for
    food substances.

    Args:
        hazard_id: Single HAZARD_ID (int) or list of HAZARD_IDs (list[int]) to query.
                  Use search_substance tool first to find HAZARD_IDs through the STUDY table.

    Returns:
        JSON string containing a DataFrame with risk assessment records. Each record
        includes assessment type, risk values, units, safety factors, and population
        information.

    The returned data includes:
    - Assessment type: ASSESSMENTTYPE (e.g., ADI, TDI, ARfD)
    - Risk values: RISKVALUE, RISKVALUE_MILLI, RISKUNIT, RISKUNIT_MILLI
    - Risk qualifier: RISKQUALIFIER (e.g., "not specified", "group")
    - Safety factors: SAFETY_FACTOR
    - Population: ID_POPULATION, POPULATIONTEXT
    - Assessment details: ASSESS, REMARKS
    - Group assessments: COM_GROUP_ID, GROUP_UNIT, GROUP_REMARKS

    Note: Multiple records may be returned if multiple HAZARD_IDs are provided or if
    a single hazard has multiple assessment types (e.g., both ADI and TDI).

    <dictionary_descriptions>
    <name>RISKQUALIFIER</name>
    <description>Description of the qualifier for the reference value</description>
    <name>RISKVALUE</name>
    <description>Quantification of the reference value</description>
    <name>RISKUNIT</name>
    <description>Short description of the units of the reference value</description>
    <name>RISKUNITFULLTEXT</name>
    <description>Full description of the units of the reference value</description>
    <name>RISKVALUE_MILLI</name>
    <description>Full description of the units of the reference value when converted to milligrams</description>
    <name>RISKUNIT_MILLI</name>
    <description>Quantification of the reference value when converted to milligrams</description>
    <name>SAFETY_FACTOR</name>
    <description>Safety factor/Uncertainty factor used to derive the reference value</description>
    <name>POPULATIONTEXT</name>
    <description>Description of the population the reference value applies to</description>
    <name>REMARKS</name>
    <description>General comments</description>
    <name>ASSESS</name>
    <description>Assessment summarised where no reference value is set</description>
    </dictionary_descriptions>
    """
    df = query_by_id(hazard_id, "chem_assess")
    return df.to_json()
