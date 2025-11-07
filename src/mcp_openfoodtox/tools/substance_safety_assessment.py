from src.mcp_openfoodtox.database.queries import query_safety_assessment


def get_substance_safety_assessment(sub_com_id):
    """
    Get comprehensive safety assessment data for a substance by SUB_COM_ID.

    Retrieves safety flags (mutagenic, genotoxic, carcinogenic) and assessment metadata
    from EFSA opinions, sorted chronologically by publication date. This tool provides
    the core safety information used by EFSA to evaluate food safety risks.

    Args:
        sub_com_id (int): The SUB_COM_ID identifier for the substance component.
                          Use search_substance tool first to find the SUB_COM_ID for a
                          given substance name or E-number.

    Returns:
        JSON string containing a DataFrame with safety assessment records. Each record
        includes safety flags, classification, opinion metadata, and publication dates.
        Results are sorted chronologically (oldest to newest) by PUBLICATIONDATE.

    The returned data includes:
    - Safety flags: IS_MUTAGENIC, IS_GENOTOXIC, IS_CARCINOGENIC
    - Classification: SUB_OP_CLASS (e.g., food additive, pesticide, flavoring)
    - Study details: REMARKS_STUDY, TOXREF_ID
    - Opinion metadata: OP_ID, AUTHOR, TITLE, ADOPTIONDATE, PUBLICATIONDATE

    Note: Multiple records may be returned if the substance has been assessed in
    multiple EFSA opinions over time. Review the chronological order to see how
    safety assessments have evolved.

    <dictionary_descriptions>
    <name>OP_ID</name>
    <description>Unique identifier links to the OPINION table</description>
    <name>IS_GENOTOXIC</name>
    <description>Indicates whether the substance is genotoxic or not according to the assessment provided in the opinion. The Not applicable notation is used in case of group substances</description>
    <name>SUB_OP_CLASS</name>
    <description>Indicates the class of the substance and the corresponding opinion as provided by EFSA</description>
    <name>IS_MUTAGENIC</name>
    <description>Indicates whether the substance is mutagenic or not according to the assessment provided in the opinion.  The "Not applicable" notation is used in case of group substances</description>
    <name>IS_CARCINOGENIC</name>
    <description>Indicates whether the substance is carcinogenic or not according to the assessment provided in the opinion. The Not applicable notation is used in case of group substances</description>
    <name>REMARKS_STUDY</name>
    <description>Indicates the objective of the opinion and report any general remark as retrieved from the opinion</description>
    <name>TOXREF_ID</name>
    <description>Unique identifier links to the ENDPOINTSTUDY table for groups</description>
    <name>AUTHOR</name>
    <description>Indicates the author/s of the publication</description>
    <name>TITLE</name>
    <description>Indicates the title of the publication</description>
    <name>ADOPTIONDATE</name>
    <description>Complete date of the adoption of the document in the format yyyymmdd</description>
    <name>PUBLICATIONDATE</name>
    <description>Complete date of the publication of the document in the format yyyymmdd</description>
    </dictionary_descriptions>
    """
    df = query_safety_assessment(sub_com_id)
    return df.to_json()
