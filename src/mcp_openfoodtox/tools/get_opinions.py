from typing import Union
from src.mcp_openfoodtox.database.queries import query_by_id


def get_opinions(op_id: Union[int, list[int]]):
    """
    Get EFSA opinion documents from OPINION table by OP_ID.

    Retrieves published EFSA scientific opinions, assessments, and regulatory documents.
    This tool provides access to the original source documents that contain the full
    scientific assessment and regulatory context for food safety evaluations.

    Args:
        op_id: Single OP_ID (int) or list of OP_IDs (list[int]) to query.
              Use search_substance tool first to find OP_IDs through the STUDY table.

    Returns:
        JSON string containing a DataFrame with opinion document records. Each record
        includes publication metadata, regulatory information, and document access details.

    The returned data includes:
    - Document identification: DOCUMENT_ID, OP_ID, TRX_ID
    - Document type: DOCTYPE, DOCTYPE_CODE
    - Publication details: TITLE, AUTHOR, PUBLICATIONDATE, ADOPTIONDATE, PUBLICATIONYEAR
    - Access information: DOI, URL
    - Regulatory context: REGULATION_CODE, REGULATION, REGULATIONFULLTEXT
    - Ownership: OWNER

    Note: Multiple records may be returned if multiple OP_IDs are provided. Each opinion
    represents a published EFSA assessment document that may contain multiple substances
    or studies.

    <dictionary_descriptions>
    <name>OP_ID</name>
    <description>Unique identifier for the EFSA opinion document</description>
    <name>DOCUMENT_ID</name>
    <description>Unique document identifier</description>
    <name>DOCTYPE</name>
    <description>Type of document (e.g., "Scientific Opinion", "Statement")</description>
    <name>TITLE</name>
    <description>Title of the published opinion document</description>
    <name>AUTHOR</name>
    <description>Author(s) of the publication</description>
    <name>PUBLICATIONDATE</name>
    <description>Date when the document was published (format: yyyymmdd)</description>
    <name>ADOPTIONDATE</name>
    <description>Date when the document was adopted (format: yyyymmdd)</description>
    <name>PUBLICATIONYEAR</name>
    <description>Year of publication</description>
    <name>DOI</name>
    <description>Digital Object Identifier for the publication</description>
    <name>URL</name>
    <description>URL link to the published document</description>
    <name>REGULATION_CODE</name>
    <description>EU regulation code (e.g., "1333/2008" for food additives, "1107/2009" for pesticides)</description>
    <name>REGULATION</name>
    <description>Short name or description of the regulation</description>
    <name>REGULATIONFULLTEXT</name>
    <description>Full text description of the regulation</description>
    <name>OWNER</name>
    <description>Organization or entity that owns or published the document</description>
    </dictionary_descriptions>
    """
    df = query_by_id(op_id, "opinion")
    return df.to_json()
