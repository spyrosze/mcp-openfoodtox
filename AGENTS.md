# EFSA OpenFoodTox MCP Server - Project Instructions

## Project Overview
Python MCP (Model Context Protocol) server providing LLM access to EFSA food safety toxicology data (~138,000 entries in 9 tables, 8K Chemical substance details). Enables natural language queries about food additives, pesticides, and chemical safety assessments.

## Dataset Structure

### Core Tables (SQLite)
- **Opinion** (2,437) - EFSA published opinions/documents
- **Synonym** (45,582) - Alternative names, E-numbers, trade names
- **Component** (8,006) - Chemical substance details (CAS, formulas, IUPAC)
- **Study** (54,621) - Fact table linking substances to studies
- **Genotox** (246) - Genotoxicity study details
- **Endpoint_study** (11,698) - Toxicity endpoints (NOAEL, LD50, etc.)
- **Chem_assess** (11,357) - Risk assessments (ADI, TDI, safety factors)
- **Question** (5,296) - Opinion-related questions
- **Dictionary** (204) - Metadata/column descriptions

### Key Relationships
```
SYNONYM (45,582 names/codes)
  ↓ SUB_COM_ID
COMPONENT (8,006 substances)
  ↓ SUB_COM_ID
STUDY (54,621 study records)
  ↓ branches to three study types:
  ├─ GENOTOX_ID → GENOTOX (246 studies)
  ├─ TOX_ID → ENDPOINT_STUDY (11,698 studies)
  └─ HAZARD_ID → CHEM_ASSESS (11,357 assessments)
  ↓ OP_ID
OPINION (2,437 opinions)
  ↓ OP_ID
QUESTION (5,296 questions)
```

### Important Fields
- **TRX_ID**: Transaction ID (published transmission identifier)
- **OP_ID**: Opinion identifier
- **SUB_COM_ID**: Substance-component link
- **COM_TYPE**: Chemical complexity (single/mixture/botanical/synthetic)
- **SUB_OP_CLASS**: Usage category (food additive/pesticide/flavoring)
- **REGULATION_CODE**: EU regulation (1333/2008=additives, 1107/2009=pesticides)

## Database Schema Reference
<details>
<summary>Detailed column metadata (197 columns across 9 tables)</summary>

*Reference only - use when needed for column names, types, and nullability*

```
Dictionary table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 204 entries, 0 to 203
Data columns (total 8 columns):
 #   Column                    Non-Null Count  Dtype 
---  ------                    --------------  ----- 
 0   Table_name                197 non-null    object
 1   Name                      197 non-null    object
 2   Type                      197 non-null    object
 3   Description               197 non-null    object
 4   isNullable                197 non-null    object
 5   isRecordUniqueIdentifier  197 non-null    object
 6   Catalogue Code            33 non-null     object
 7   Last update               190 non-null    object
dtypes: object(8)
memory usage: 12.9+ KB
None
----------
Synonym table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 45582 entries, 0 to 45581
Data columns (total 5 columns):
 #   Column       Non-Null Count  Dtype 
---  ------       --------------  ----- 
 0   SYNONYM_ID   45582 non-null  int64 
 1   SUB_COM_ID   45582 non-null  int64 
 2   TRX_ID       45582 non-null  int64 
 3   TYPE         45582 non-null  object
 4   DESCRIPTION  45582 non-null  object
dtypes: int64(3), object(2)
memory usage: 1.7+ MB
None
----------
Opinion table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 2437 entries, 0 to 2436
Data columns (total 20 columns):
 #   Column              Non-Null Count  Dtype         
---  ------              --------------  -----         
 0   DOCUMENT_ID         2437 non-null   int64         
 1   OP_ID               2437 non-null   int64         
 2   TRX_ID              2437 non-null   int64         
 3   DOCTYPE_ID          2437 non-null   int64         
 4   DOCTYPE_CODE        2437 non-null   object        
 5   DOCTYPE             2437 non-null   object        
 6   AUTHOR              2436 non-null   object        
 7   TITLE               2437 non-null   object        
 8   ADOPTION_DATE       2437 non-null   int64         
 9   ADOPTIONDATE        2437 non-null   datetime64[ns]
 10  PUBLICATION_DATE    2437 non-null   int64         
 11  PUBLICATIONDATE     2437 non-null   datetime64[ns]
 12  PUBLICATIONYEAR     2437 non-null   int64         
 13  DOI                 2437 non-null   object        
 14  URL                 2437 non-null   object        
 15  REGULATION_ID       2422 non-null   float64       
 16  REGULATION_CODE     2422 non-null   object        
 17  REGULATION          2422 non-null   object        
 18  REGULATIONFULLTEXT  2422 non-null   object        
 19  OWNER               2437 non-null   object        
dtypes: datetime64[ns](2), float64(1), int64(7), object(10)
memory usage: 380.9+ KB
None
----------
Component table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 8006 entries, 0 to 8005
Data columns (total 31 columns):
 #   Column                   Non-Null Count  Dtype  
---  ------                   --------------  -----  
 0   SUBSTANCECOMPONENT_ID    8006 non-null   int64  
 1   SUB_COM_ID               8006 non-null   int64  
 2   SUB_ID                   8006 non-null   int64  
 3   COM_ID                   8006 non-null   int64  
 4   TRX_ID                   8006 non-null   int64  
 5   SUB_NAME                 8006 non-null   object 
 6   SUB_ECSUBINVENTENTRYREF  3111 non-null   object 
 7   SUB_CASNUMBER            4263 non-null   object 
 8   SUB_DESCRIPTION          4398 non-null   object 
 9   SUBPARAM_ID              8006 non-null   int64  
 10  SUBPARAM_CODE            8006 non-null   object 
 11  SUBPARAMNAME             8006 non-null   object 
 12  SUB_TYPE                 8006 non-null   object 
 13  QUALIFIER_ID             8006 non-null   int64  
 14  QUALIFIER_CODE           8006 non-null   object 
 15  QUALIFIER                8006 non-null   object 
 16  COMP_VALUE               340 non-null    float64
 17  COM_NAME                 8006 non-null   object 
 18  COM_ECSUBINVENTENTRYREF  4705 non-null   object 
 19  COM_CASNUMBER            6713 non-null   object 
 20  IUPACNAME                6563 non-null   object 
 21  COMPARAM_ID              8006 non-null   int64  
 22  COMPARAM_CODE            8006 non-null   object 
 23  COMPARAMNAME             8006 non-null   object 
 24  MOLECULARFORMULA         6670 non-null   object 
 25  SMILESNOTATION           6695 non-null   object 
 26  INCHI                    6743 non-null   object 
 27  COM_TYPE                 8006 non-null   object 
 28  COM_STRUCTURESHOWN       0 non-null      float64
 29  SMILESNOTATIONSOURCE     0 non-null      float64
 30  INCHI_NOTATIONSOURCE     0 non-null      float64
dtypes: float64(4), int64(8), object(19)
memory usage: 1.9+ MB
None
----------
Study table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 54621 entries, 0 to 54620
Data columns (total 14 columns):
 #   Column           Non-Null Count  Dtype  
---  ------           --------------  -----  
 0   FACTSTUDY_ID     54621 non-null  int64  
 1   STUDY_ID         54621 non-null  int64  
 2   SUB_COM_ID       54621 non-null  int64  
 3   OP_ID            54621 non-null  int64  
 4   GENOTOX_ID       1452 non-null   float64
 5   TOX_ID           30192 non-null  float64
 6   HAZARD_ID        42475 non-null  float64
 7   TRX_ID           54621 non-null  int64  
 8   SUB_OP_CLASS     54621 non-null  object 
 9   IS_MUTAGENIC     54621 non-null  object 
 10  IS_GENOTOXIC     54621 non-null  object 
 11  IS_CARCINOGENIC  54621 non-null  object 
 12  REMARKS_STUDY    54590 non-null  object 
 13  TOXREF_ID        84 non-null     float64
dtypes: float64(4), int64(5), object(5)
memory usage: 5.8+ MB
None
----------
Chem_assess table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 11357 entries, 0 to 11356
Data columns (total 24 columns):
 #   Column               Non-Null Count  Dtype  
---  ------               --------------  -----  
 0   CHEMASSESS_ID        11357 non-null  int64  
 1   HAZARD_ID            11357 non-null  int64  
 2   TRX_ID               11357 non-null  int64  
 3   ASSESSMENTTYPE_ID    11357 non-null  int64  
 4   ASSESSMENTTYPE_CODE  11357 non-null  object 
 5   ASSESSMENTTYPE       11357 non-null  object 
 6   RISKQUALIFIER_ID     10492 non-null  float64
 7   RISKQUALIFIER_CODE   10492 non-null  object 
 8   RISKQUALIFIER        10492 non-null  object 
 9   RISKVALUE            10492 non-null  float64
 10  RISKUNIT_ID          10492 non-null  float64
 11  RISKUNIT_CODE        10492 non-null  object 
 12  RISKUNIT             10486 non-null  object 
 13  RISKUNITFULLTEXT     10492 non-null  object 
 14  RISKVALUE_MILLI      10492 non-null  float64
 15  RISKUNIT_MILLI       10492 non-null  object 
 16  SAFETY_FACTOR        4440 non-null   float64
 17  ID_POPULATION        11328 non-null  object 
 18  POPULATIONTEXT       11328 non-null  object 
 19  REMARKS              9075 non-null   object 
 20  ASSESS               1305 non-null   object 
 21  COM_GROUP_ID         340 non-null    float64
 22  GROUP_UNIT           340 non-null    object 
 23  GROUP_REMARKS        16 non-null     object 
dtypes: float64(6), int64(4), object(14)
memory usage: 2.1+ MB
None
----------
Question table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 5296 entries, 0 to 5295
Data columns (total 4 columns):
 #   Column       Non-Null Count  Dtype 
---  ------       --------------  ----- 
 0   QUESTION_ID  5296 non-null   int64 
 1   OP_ID        5296 non-null   int64 
 2   TRX_ID       5296 non-null   int64 
 3   QUESTION     5296 non-null   object
dtypes: int64(3), object(1)
memory usage: 165.6+ KB
None
----------
Genotox table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 246 entries, 0 to 245
Data columns (total 32 columns):
 #   Column                   Non-Null Count  Dtype  
---  ------                   --------------  -----  
 0   GENOTOXICITY_ID          246 non-null    int64  
 1   GENOTOX_ID               246 non-null    int64  
 2   TRX_ID                   246 non-null    int64  
 3   STUDY_CATEGORY           246 non-null    object 
 4   GUIDELINE_QUALIFIER      246 non-null    object 
 5   GENOTOXGUIDELINE_ID      31 non-null     float64
 6   GENOTOXGUIDELINE_CODE    31 non-null     object 
 7   GENOTOXGUIDELINE         246 non-null    object 
 8   GENOTOXGUIDELINEFULLTXT  246 non-null    object 
 9   DEVIATION                20 non-null     object 
 10  GLP_COMPL                32 non-null     object 
 11  SPECIES_CODE_ID          246 non-null    int64  
 12  SPECIES_CODE             246 non-null    object 
 13  SPECIES                  246 non-null    object 
 14  STRAIN_ID                104 non-null    float64
 15  STRAIN_CODE              104 non-null    object 
 16  STRAIN                   104 non-null    object 
 17  SEX                      42 non-null     object 
 18  MET_INDICATOR            75 non-null     object 
 19  ROUTE_ID                 61 non-null     float64
 20  ROUTE_CODE               61 non-null     object 
 21  ROUTE                    246 non-null    object 
 22  EXP_PERIOD               35 non-null     float64
 23  EXPPERIODUNIT_ID         35 non-null     float64
 24  EXPPERIODUNIT_CODE       35 non-null     object 
 25  EXPPERIODUNIT            35 non-null     object 
 26  EXPPERIODUNITFULLTXT     35 non-null     object 
 27  EXPPERIOD_DAY            35 non-null     float64
 28  NUMBER_INDIVIDUALS       13 non-null     float64
 29  CONTROL                  40 non-null     object 
 30  IS_GENOTOXIC             246 non-null    object 
 31  REMARKS                  231 non-null    object 
dtypes: float64(7), int64(4), object(21)
memory usage: 61.6+ KB
None
----------
Endpoint_study table
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 11698 entries, 0 to 11697
Data columns (total 60 columns):
 #   Column               Non-Null Count  Dtype  
---  ------               --------------  -----  
 0   ENDPOINTSTUDY_ID     11698 non-null  int64  
 1   TOX_ID               11698 non-null  int64  
 2   TRX_ID               11698 non-null  int64  
 3   STUDY_CATEGORY       11698 non-null  object 
 4   TESTSUBSTANCE        1931 non-null   object 
 5   TESTTYPE_ID          11698 non-null  int64  
 6   TESTTYPE_CODE        11698 non-null  object 
 7   TESTTYPE             11698 non-null  object 
 8   LIMITTEST            1174 non-null   object 
 9   GUIDELINE_QUALIFIER  11698 non-null  object 
 10  GUIDELINE_ID         1362 non-null   float64
 11  GUIDELINE_CODE       1362 non-null   object 
 12  GUIDELINE            11698 non-null  object 
 13  GUIDELINEFULLTXT     11698 non-null  object 
 14  DEVIATION            11698 non-null  object 
 15  GLP_COMPL            11698 non-null  object 
 16  SPECIES_ID           11646 non-null  float64
 17  SPECIES_CODE         11698 non-null  object 
 18  SPECIES              11698 non-null  object 
 19  STRAIN_ID            2 non-null      float64
 20  STRAIN_CODE          458 non-null    object 
 21  STRAIN               458 non-null    object 
 22  SEX                  1042 non-null   object 
 23  ROUTE_ID             4310 non-null   float64
 24  ROUTE_CODE           4310 non-null   object 
 25  ROUTE                11698 non-null  object 
 26  EXP_DURATION         6304 non-null   float64
 27  DURATIONUNIT_ID      6304 non-null   float64
 28  DURATIONUNIT_CODE    6304 non-null   object 
 29  DURATIONUNIT         6304 non-null   object 
 30  EXP_DURATION_DAYS    6304 non-null   float64
 31  NUMBER_INDIVIDUALS   647 non-null    float64
 32  CONTROL              731 non-null    object 
 33  ENDPOINT_ID          11698 non-null  int64  
 34  ENDPOINT_CODE        11698 non-null  object 
 35  ENDPOINT             11698 non-null  object 
 36  QUALIFIER_ID         11698 non-null  int64  
 37  QUALIFIER_CODE       11698 non-null  object 
 38  QUALIFIER            11698 non-null  object 
 39  VALUE                11698 non-null  float64
 40  DOSEUNIT_ID          11698 non-null  int64  
 41  DOSEUNIT_CODE        11698 non-null  object 
 42  DOSEUNIT             11691 non-null  object 
 43  DOSEUNITFULLTEXT     11698 non-null  object 
 44  VALUE_MILLI          11698 non-null  float64
 45  UNIT_MILLI           11698 non-null  object 
 46  BASIS_ID             11698 non-null  int64  
 47  BASIS_CODE           11698 non-null  object 
 48  BASIS                11698 non-null  object 
 49  TOXICITY_ID          5253 non-null   float64
 50  TOXICITY_CODE        5253 non-null   object 
 51  TOXICITY             5253 non-null   object 
 52  TARGETTISSUE_ID      674 non-null    float64
 53  TARGETTISSUE_CODE    674 non-null    object 
 54  TARGETTISSUE         657 non-null    object 
 55  EFFECT_DESC          3567 non-null   object 
 56  REMARKS              5363 non-null   object 
 57  GROUP_UNIT           236 non-null    object 
 58  COMGROUP_ID          236 non-null    float64
 59  GROUP_REMARKS        26 non-null     object 
```

*Add full schema export here when available*

</details>

## MCP Tools Implemented

### 1. `search_substance`
**Input:** `description_search: str` (substance name, E-number, or description)
**Returns:** List of unique substances (by SUB_COM_ID) with aggregated study data (GENOTOX_ID, TOX_ID, HAZARD_ID, OP_ID arrays)
**Method:** `query_search_substance()` - searches SYNONYM first (DESCRIPTION field), falls back to COMPONENT (SUB_NAME, COM_NAME) if no results
**Joins:** SYNONYM → COMPONENT (by SUB_COM_ID) → STUDY (by SUB_COM_ID)
**Note:** Returns aggregated arrays of study IDs, not full study details. Use other tools with these IDs for detailed data.

### 2. `get_substance_safety_assessment`
**Input:** `sub_com_id: int` (use search_substance first to get SUB_COM_ID)
**Returns:** Safety flags (IS_MUTAGENIC, IS_GENOTOXIC, IS_CARCINOGENIC) with opinion metadata, sorted chronologically
**Method:** `query_safety_assessment()` - filters STUDY by SUB_COM_ID, joins OPINION for dates/metadata
**Joins:** STUDY (filtered by SUB_COM_ID) → OPINION (LEFT JOIN on OP_ID)
**Note:** Returns DataFrame as JSON, sorted by PUBLICATIONDATE ascending

### 3. `get_toxicity_endpoints`

**Input:** `tox_id: Union[int, list[int]]` (use search_substance to get TOX_IDs from STUDY table)
**Returns:** Toxicity endpoint study data (NOAEL, LD50, target organs, study conditions)
**Method:** `query_by_id()` - direct query to ENDPOINT_STUDY table
**Joins:** None (direct table query by TOX_ID)
**Note:** Returns all columns from ENDPOINT_STUDY table as JSON

### 4. `get_risk_assessments`

**Input:** `hazard_id: Union[int, list[int]]` (use search_substance to get HAZARD_IDs from STUDY table)
**Returns:** Risk assessment data (ADI/TDI values, RISKVALUE_MILLI, SAFETY_FACTOR, POPULATIONTEXT)
**Method:** `query_by_id()` - direct query to CHEM_ASSESS table
**Joins:** None (direct table query by HAZARD_ID)
**Note:** Returns all columns from CHEM_ASSESS table as JSON. Use this for safe intake limits (ADI/TDI).

### 5. `get_genotox_details`

**Input:** `genotox_id: Union[int, list[int]]` (use search_substance to get GENOTOX_IDs from STUDY table)
**Returns:** Genotoxicity study details (test guidelines, species, exposure conditions, IS_GENOTOXIC result)
**Method:** `query_by_id()` - direct query to GENOTOX table
**Joins:** None (direct table query by GENOTOX_ID)

### 6. `get_opinions`

**Input:** `op_id: Union[int, list[int]]` (use search_substance to get OP_IDs from STUDY table)
**Returns:** EFSA opinion documents (title, author, publication date, DOI, URL, regulation info)
**Method:** `query_by_id()` - direct query to OPINION table
**Joins:** None (direct table query by OP_ID)

### 7. `list_substances_by_class_and_safety`

**Input:** Optional filters: `sub_class: str`, `is_mutagenic: str`, `is_genotoxic: str`, `is_carcinogenic: str`, `remarks_contains: str`, `limit: int`
**Returns:** Filtered substance list with synonyms aggregated (SUB_COM_ID, COM_NAME, COM_TYPE, SUB_TYPE, DESCRIPTION)
**Method:** `query_substances_by_class_and_safety()` - filters STUDY by safety criteria, joins to COMPONENT and SYNONYM
**Joins:** STUDY (filtered by safety criteria) → COMPONENT (INNER JOIN on SUB_COM_ID) → SYNONYM (LEFT JOIN on SUB_COM_ID)
**Note:** Returns unique substances (GROUP BY SUB_COM_ID) with synonyms aggregated as comma-separated list

### 8. `list_hazard_ids_by_assessment`

**Input:** Optional filters: `population_text_contains: str`, `assessment_type: str`, `risk_value_milli_max: float`, `risk_value_milli_min: float`, `has_no_risk_value: bool`, `limit: int`
**Returns:** List of HAZARD_IDs (as JSON array) matching assessment criteria
**Method:** `query_hazard_ids_by_assessment()` - filters CHEM_ASSESS table directly
**Joins:** None (direct query to CHEM_ASSESS table)
**Note:** Building block tool - use returned HAZARD_IDs with `list_substances_by_study` (via `list_substances_by_assessment`)

### 9. `list_substances_by_assessment`

**Input:** Optional filters: `population_text_contains: str`, `assessment_type: str`, `risk_value_milli_max: float`, `risk_value_milli_min: float`, `has_no_risk_value: bool`, `limit: int`
**Returns:** Filtered substance list with synonyms aggregated (SUB_COM_ID, COM_NAME, COM_TYPE, SUB_TYPE, DESCRIPTION)
**Method:** Two-step: `query_hazard_ids_by_assessment()` → `query_substances_by_study(study_type="hazard")`
**Joins:** CHEM_ASSESS (filtered by assessment criteria) → STUDY (by HAZARD_ID) → COMPONENT (by SUB_COM_ID) → SYNONYM (by SUB_COM_ID)
**Note:** Combines assessment filtering with substance retrieval in one tool

## Tools Not Yet Implemented

### `compare_substances`

**Input:** `category: str, metric: str`
**Returns:** Ranked comparison (e.g., sweeteners by ADI)
**Joins:** COMPONENT → STUDY → CHEM_ASSESS (aggregated)
**Status:** Not implemented - would require aggregation and ranking logic

## Search Strategy

### Multi-source Search
Always search both SYNONYM and COMPONENT tables:
- SYNONYM: E-numbers, common names, trade names (incomplete coverage)
- COMPONENT: SUB_NAME, COM_NAME (authoritative chemical names)

### Handle Multiple Results
- Same synonym → multiple SUB_COM_IDs (different sources/formulations)
- Differentiate using: COM_TYPE, SUB_OP_CLASS, REGULATION_CODE, SUB_DESCRIPTION

### Name Variations
Handle: "E951" vs "E 951" vs "aspartame" vs "L-aspartyl-L-phenylalanine methyl ester"

## Data Quirks

1. **Incomplete E-number coverage**: Not all E-numbers in SYNONYM (e.g., E962 missing)
2. **Duplicate synonyms**: Multiple SUB_COM_IDs share same synonym (e.g., "Provitamin A")
3. **Sparse nulls**: Many optional fields (GLP_COMPL, STRAIN, CONTROL, etc.)
4. **Regulation complexity**: 60+ regulations, key ones: 1333/2008 (additives), 1107/2009 (pesticides)

## Implementation Notes

### Query Architecture
- **Hard-code SQL joins** in tools (deterministic, reliable)
- LLM selects tool and extracts parameters
- Avoid LLM-generated SQL queries

### Response Format
Return structured JSON with:
- Primary result (chemical details/safety data)
- Context (opinion titles, study counts, regulation info)
- Citations (OP_ID, TRX_ID, DOCUMENT_ID)

### Error Handling
- Substance not found → suggest similar names
- Multiple matches → return ranked list with differentiators
- Missing data → explicitly state "no data available for X"

## Target Users
1. General public (E-number safety checks)
2. Food industry (ADI limits, specifications)
3. Regulators (genotoxicity flags, study gaps)
4. Researchers (comparative analysis, study protocols)
5. Health professionals (dietary advice, patient safety)

## Common Query Patterns
- "What is [substance]?" → `identify_substance`
- "Is [substance] safe?" → `get_safety_assessment`
- "What are side effects of [substance]?" → `get_toxicity_effects`
- "How much [substance] is safe daily?" → `get_safe_intake_limits`
- "Compare all sweeteners" → `compare_substances`
- "List natural food additives" → `list_substances_by_criteria`

## Development Priorities
1. Core search (SYNONYM + COMPONENT fuzzy matching)
2. Tool 1-4 (80% of user queries)
3. Result ranking/disambiguation
4. Tool 5-6 (advanced queries)
5. Citation formatting

## Completed Tasks
- [x] Database setup and schema understanding
- [x] Basic query function in main.py (SYNONYM → COMPONENT → STUDY joins)
- [x] Project documentation and tool specifications
- [x] MCP server structure and initialization
- [x] Core search functionality (SYNONYM + COMPONENT fuzzy matching)
- [x] Tool 1: `search_substance` - [SUB_COM_IDs] + basic info + study data aggregated into arrays
- [x] Tool 2: `get_safety_assessment` - Safety flags (mutagenic/genotoxic/carcinogenic)
- [x] Tool 3: `get_toxicity_effects` - Toxicity endpoints, target organs
- [ ] Tool 4: `get_safe_intake_limits` - ADI/TDI values, safety factors
- [ ] Tool 5: `compare_substances` - Ranked comparisons by category/metric
- [x] Tool 6: `list_substances_by_criteria` - Filtered substance lists joining STUDY, COMPONENT and SYNONYM tables
- [x] Tool 6: `list_substances_by_study` - Query by study IDs (GENOTOX_ID, TOX_ID, HAZARD_ID, or OP_ID) joining STUDY, COMPONENT and SYNONYM tables. meant for a building block that can combine a study filter eg CHEM_ASSESS filter -> list_substances_by_study -> component
- [ ] Result ranking and disambiguation logic
- [ ] Error handling and similar name suggestions
- [ ] Citation formatting