from src.mcp_openfoodtox.database.queries import query_search_substance


def search_substance(description_search):
    """
    MCP tool to search the OpenFoodTox database for substances by name, E-number, or description.

    Searches the database using a two-step approach:
    1. First searches SYNONYM table (E-numbers, common names, trade names, alternative names)
    2. If no results, searches COMPONENT table (SUB_NAME and COM_NAME fields)

    The search is case-insensitive and supports partial matches. E-numbers are automatically
    normalized (e.g., "E 951" or "E-951" becomes "E951").

    Returns a list of unique substances (one dictionary per SUB_COM_ID) with all study data
    aggregated into arrays. Each substance may have multiple studies, opinions, and assessments,
    which are grouped together by SUB_COM_ID.

    Args:
        description_search: Search term (substance or component name e.g. "aspartame", OR E-number e.g. "E 951") or any of the following CAS name, Council of Europe number, E number, E.C enzyme number, EC name, EU Flavour Information System number, EUgroup-no, Flavour and Extract Manufacturers Association number, Joint FAO/WHO Expert Committee on Food Additives number, Name, OECD Toolbox Classification, Pharmalogical class, Swiss Prot no., Trade name

    Returns:
        List of dictionaries, where each dictionary represents a unique substance with:
        - Basic component information (name, type, formula, description)
        - Aggregated study identifiers (arrays of IDs linking to related tables)
        - Study classifications and remarks (arrays of unique values from all studies)

        Returns None if no matches are found.

    <dictionary_descriptions>
    <name>SUB_COM_ID</name>
    <description>Unique identifier for the substance-component link. Primary key for grouping results. Multiple studies, opinions, and assessments may reference the same SUB_COM_ID.</description>
    <name>COM_NAME</name>
    <description>Component name as derived in the opinions. If more than one name is reported in the opinion (excluding IUPAC name), then the most common/most specific name is reported as component name.</description>
    <name>COM_TYPE</name>
    <description>High level classification of component type (e.g., single, mixture, botanical, synthetic).</description>
    <name>MOLECULARFORMULA</name>
    <description>Molecular formula of the chemical component.</description>
    <name>SUB_DESCRIPTION</name>
    <description>Summary of the substance description as derived from opinions. This includes also the group description.</description>
    <name>SUB_OP_CLASS</name>
    <description>Array of unique values indicating the class of the substance and the corresponding opinion as provided by EFSA (e.g., "food additive", "pesticide", "flavoring"). Aggregated from all studies for this substance.</description>
    <name>REMARKS</name>
    <description>Array of unique remarks from all studies. Indicates the objective of the opinion and reports any general remarks as retrieved from the opinion. Aggregated from REMARKS_STUDY field.</description>
    <name>GENOTOX_ID</name>
    <description>Array of unique identifiers linking to the GENOTOX table. Each ID represents a genotoxicity study associated with this substance. May be None if no genotoxicity studies exist.</description>
    <name>TOX_ID</name>
    <description>Array of unique identifiers linking to the ENDPOINT_STUDY table. Each ID represents a toxicity endpoint study (e.g., NOAEL, LD50). May be None if no endpoint studies exist.</description>
    <name>HAZARD_ID</name>
    <description>Array of unique identifiers linking to the CHEM_ASSESS table. Each ID represents a chemical risk assessment (e.g., ADI, TDI values). May be None if no assessments exist.</description>
    <name>OP_ID</name>
    <description>Array of unique identifiers linking to the OPINION table. Each ID represents an EFSA published opinion/document associated with this substance. May be None if no opinions exist.</description>
    </dictionary_descriptions>
    """
    results = query_search_substance(description_search)
    return results
