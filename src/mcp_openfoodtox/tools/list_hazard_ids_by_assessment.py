import json
from typing import Optional
from src.mcp_openfoodtox.database.multi_sub_queries import query_hazard_ids_by_assessment


def list_hazard_ids_by_assessment(
    population_text_contains: Optional[str] = None,
    assessment_type: Optional[str] = None,
    risk_value_milli_max: Optional[float] = None,
    risk_value_milli_min: Optional[float] = None,
    has_no_risk_value: Optional[bool] = None,
    limit: Optional[int] = None,
):
    """
    Find HAZARD_IDs from risk assessments (CHEM_ASSESS table) filtered by population,
    assessment type, and dosage thresholds. This tool enables discovery of substances
    that have specific safety limits or restrictions for particular populations.

    Use this tool to identify which substances have risk assessments matching your criteria,
    then use the returned HAZARD_IDs with list_substances_by_study to get the actual
    substance names and details.

    ## Example questions it can answer:

    ### Population-Specific Safety Queries
    * "Which substances have safety assessments for children under 3?"
    * "Find all assessments that apply to pregnant women"
    * "What substances have ADI limits for infants?"
    * "Show me assessments for children aged 3-10"
    * "Which substances have population-specific restrictions?"

    ### Dosage Threshold Queries
    * "Find all substances with ADI less than 1 mg/kg body weight"
    * "Which assessments have very low safe intake limits (< 0.1 mg/kg)?"
    * "Show me substances with TDI greater than 10 mg/kg"
    * "What substances have high safe intake limits (> 100 mg/kg)?"
    * "Find assessments with ADI between 0.5 and 5 mg/kg"

    ### Assessment Type Queries
    * "Which substances have ADI (Acceptable Daily Intake) assessments?"
    * "Find all TDI (Tolerable Daily Intake) assessments"
    * "Show me ARfD (Acute Reference Dose) assessments"
    * "What substances have group assessments?"

    ### Combined Population + Dosage Queries
    * "Find substances with ADI < 1 mg/kg for children"
    * "Which assessments for pregnant women have low safe limits?"
    * "Show me substances with very restrictive limits for infants (< 0.5 mg/kg)"
    * "What substances have high ADI (> 50 mg/kg) for adults?"

    ### Missing Data Queries
    * "Which assessments have no quantitative safe intake limit set?"
    * "Find substances where risk assessment exists but no ADI/TDI value is specified"
    * "Show me assessments that only have qualitative assessments (no numeric limits)"

    ### Risk Identification Queries
    * "Find all substances that indicate issues for children under 3"
    * "Which assessments suggest concerns for specific populations?"
    * "Show me substances with population-specific warnings"

    Args:
        population_text_contains: Optional text search in POPULATIONTEXT field (case-insensitive).
                                 Searches for partial matches in population descriptions.
                                 Examples:
                                 - "children" matches "Consumers - Children", "Consumers - Children 1-2 years", etc.
                                 - "pregnant" matches "Consumers - Pregnant women >= 18 years"
                                 - "infant" matches "Consumers - Infants", "Consumers - Infants 0-6 months"
                                 - "adult" matches "Consumers - Adults", "Consumers - Adults >=18 years"
                                 See "Population Text Reference" section below for complete list of accepted values.
        assessment_type: Optional filter by assessment type (case-insensitive partial match).
                        Examples:
                        - "ADI" matches "ADI" (Acceptable Daily Intake)
                        - "TDI" matches "TDI" (Tolerable Daily Intake)
                        - "ARfD" matches "ARfD" (Acute Reference Dose)
                        - "group" matches group assessments
        risk_value_milli_max: Optional maximum RISKVALUE_MILLI in mg/kg body weight (inclusive, <=).
                             Use to find substances with low safe limits.
                             Examples:
                             - 1.0 for ADI < 1 mg/kg
                             - 0.1 for very restrictive limits
                             - 10.0 for moderate limits
        risk_value_milli_min: Optional minimum RISKVALUE_MILLI in mg/kg body weight (inclusive, >=).
                             Use to find substances with high safe limits.
                             Examples:
                             - 10.0 for ADI > 10 mg/kg
                             - 100.0 for very high limits
        has_no_risk_value: If True, only return HAZARD_IDs where RISKVALUE IS NULL.
                          Use to find assessments with no quantitative limit set.
                          These may have qualitative assessments in the ASSESS field instead.
        limit: Optional maximum number of HAZARD_IDs to return. Use to limit results
              for large queries. If None, returns all matching HAZARD_IDs.

    Population Text Reference:
        The following are accepted POPULATIONTEXT values in the database. Use partial
        matches (case-insensitive) to search. For example, "children" will match
        "Consumers - Children", "Consumers - Children 1-2 years", etc.

        Consumers:
            - Consumers
            - Consumers - Children
            - Consumers - Infants
            - Consumers - Adults
            - Consumers - Adult women, pregnant
            - Consumers - Adult women, lactating
            - Consumers - Pregnant women >= 18 years
            - Consumers - Pregnant women >= 25 years
            - Consumers - Pregnant women 18-24 years
            - Consumers - Lactating women >= 18 years
            - Consumers - Lactating women >= 25 years
            - Consumers - Lactating women 18-24 years
            - Consumers - Premenopausal women
            - Consumers - Postmenopausal women
            - Consumers - Toddlers
            - Consumers - Adolescents
            - Consumers - Adults >=18 years
            - Consumers - Adults >= 25 years
            - Consumers - Adults 18-24 years
            - Consumers - Children 11-14 years
            - Consumers - Children 10-17 years
            - Consumers - Children 11-17 years
            - Consumers - Children 12-17 years
            - Consumers - Children 15-17 years
            - Consumers - Children 1-2 years
            - Consumers - Children 1-3 years
            - Consumers - Children 1-6 years
            - Consumers - Children 1-8 years
            - Consumers - Children 1-10 years
            - Consumers - Children 3 years
            - Consumers - Children 3-9 years
            - Consumers - Children 4-6 years
            - Consumers - Children 4-9 years
            - Consumers - Children 4-10 years
            - Consumers - Children 7-8 years
            - Consumers - Children 7-9 years
            - Consumers - Children 7-10 years
            - Consumers - Children 7-11 years
            - Consumers - Children 9-10 years
            - Consumers - Children 10 years
            - Consumers - Infants 0-6 months
            - Consumers - Infants 0-12 months
            - Consumers - Infants 6-12 months
            - Consumers - Infants 7-11 months

        Workers and Operators:
            - Workers
            - Worker - adults
            - Operators
            - Residents and bystanders
            - Residents and bystander - children

        Pets:
            - Dogs as pet
            - Cats as pet

        Poultry:
            - Poultry
            - Chicken for meat production
            - Chicken for egg production
            - Chicken for egg production - adults
            - Chicken for egg production, less than 1 year old
            - Chicken broilers, less than 1 year old
            - Turkeys
            - Turkeys for meat production
            - Turkeys for meat production, less than 1 year old
            - Turkey for reproduction
            - Guinea-fowl
            - Bird

        Pigs:
            - Pigs
            - Pigs - less than 1 year old
            - Pigs - for reproduction
            - Pigs for meat production
            - Pigs for meat production - adults
            - Pigs for meat production - less than 1 year old
            - Pigs for reproduction - adults

        Cattle:
            - Cattle
            - Cattle for meat production
            - Cattle for meat production - adults
            - Cattle for meat production - less than 1 year old
            - Cattle for milk production
            - Cattle for milk production - adults
            - Cattle for milk production - less than 1 year old
            - Cattle for reproduction
            - Cattle for reproduction - less than 1 year old
            - Young cattle of less than 1 year of age

        Sheep and Goats:
            - Sheep - unspecified
            - Sheep for milk production
            - Sheep for meat production
            - Goat

        Other Animals:
            - Fish
            - Salmons
            - Trouts
            - Rabbits
            - Rabbits for meat production
            - Horse
            - Equines
            - Rodents
            - Ruminants - unspecified

        Aquatic and Environmental:
            - Aquatic animal not used for food production - unspecified
            - Aquatic animal for food production - unspecified
            - Aquatic organisms
            - Aquatic Plants
            - Aquatic Invertebrates
            - Aquatic compartment
            - Terrestrial Plants
            - Soil compartment
            - Soil macroorganims - arthropods
            - Soil macroorganisms - earthworms

        Unspecified Categories:
            - Animal not used for food production - unspecified
            - Animal for food production - unspecified

    Returns:
        JSON string containing a list of HAZARD_IDs (integers) that match the criteria.
        Returns an empty list if no assessments match.

        Example return value: "[123, 456, 789]"

    Workflow:
        1. Use this tool to find HAZARD_IDs matching your criteria
        2. Use list_substances_by_study with the returned HAZARD_IDs and study_type="hazard"
           to get the actual substance names and details
        3. Optionally use get_risk_assessments with specific HAZARD_IDs for detailed
           assessment information

    Example usage:
        # Find HAZARD_IDs for children with low ADI
        hazard_ids_json = list_hazard_ids_by_assessment(
            population_text_contains="children",
            assessment_type="ADI",
            risk_value_milli_max=1.0,
            limit=20
        )
        # Parse and use with list_substances_by_study
        hazard_ids = json.loads(hazard_ids_json)
        # substances = list_substances_by_study(ids=hazard_ids, study_type="hazard")
    """
    hazard_ids = query_hazard_ids_by_assessment(
        population_text_contains=population_text_contains,
        assessment_type=assessment_type,
        risk_value_milli_max=risk_value_milli_max,
        risk_value_milli_min=risk_value_milli_min,
        has_no_risk_value=has_no_risk_value,
        limit=limit,
    )
    return json.dumps(hazard_ids)
