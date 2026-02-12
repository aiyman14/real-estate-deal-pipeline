"""
Extraction prompts for LLM-based field extraction.

These prompts enforce:
- No hallucination: only extract explicitly stated information
- Leave unknown fields as null
- Return valid JSON
"""

TRANSACTIONS_SYSTEM_PROMPT = """You are a precise data extraction assistant for real estate transactions.

CRITICAL RULES:
1. ONLY extract information that is EXPLICITLY stated in the text
2. If a field is not clearly mentioned, return null - NEVER guess or infer
3. Return valid JSON matching the exact schema provided
4. For dates, extract as-is (normalization happens later)
5. For prices/areas, extract ONLY the number with unit (e.g., "743 mkr", "47696 kvm") - no explanatory text
6. For property type: Use "Mixed-use" if the article mentions multiple property types (office, retail, residential, industrial, etc.)
7. For location: Use "Multiple" if properties are in several different cities
8. Comments should be 1-2 factual sentences summarizing the deal - no marketing language

You extract completed real estate transactions from news articles."""

TRANSACTIONS_USER_PROMPT = """Extract the transaction details from this article text.

Return a JSON object with these fields (use null if not explicitly stated):
{{
  "Country": "<Sweden|Denmark|Finland or local name>",
  "Date": "<transaction date as written>",
  "Buyer": "<full buyer company name - only if explicitly stated>",
  "Seller": "<full seller company name - only if explicitly stated>",
  "Location": "<city name, or 'Multiple' if properties in several cities>",
  "Property type": "<property type, or 'Mixed-use' if multiple types mentioned (office+retail+residential etc.)>",
  "Area, m2": "<area as number with unit only, e.g. '47696 kvm' - no descriptive text>",
  "Price": "<primary price as number with currency, e.g. '743 mkr' or '150 MSEK' - not multiple values>",
  "Yield": "<yield as number with % or 'procent', e.g. '7.2%' or '7,2 procent'>",
  "Broker": "<broker/advisor name if stated>",
  "Project name": "<property/project name if stated>",
  "Comments": "<1-2 sentence factual summary>"
}}

ARTICLE TEXT:
{article_text}

JSON OUTPUT:"""

INBOUND_SYSTEM_PROMPT = """You are a precise data extraction assistant for real estate deal documents.

CRITICAL RULES:
1. ONLY extract information that is EXPLICITLY stated in the document
2. If a field is not clearly mentioned, return null - NEVER guess or infer
3. Return valid JSON matching the exact schema provided
4. For dates, extract as-is (normalization happens later)
5. For prices/areas/NOI, extract as-is including units (normalization happens later)
6. For property type/use, extract the description as-is (normalization happens later)
7. Comments should be 2-3 factual sentences: property description + key metrics (area, rent, NOI, yield) if stated. No marketing language.
8. For Type: Identify document type - "IM" for Investment Memorandum, "Teaser" for teaser/summary documents
9. For Address: Extract specific street address (e.g., "Storgatan 12") - different from Location (city) and Property designation (cadastral reference)
10. For NOI: Extract ONLY the total NOI amount as a single number. Do NOT combine with NOI per sqm.
11. For Base rent: Look for "bashyra", "grundhyra", "base rent", "annual rent" - the contractual rent amount per sqm
12. For Occupancy: Look for "uthyrningsgrad", "occupancy rate", "vacancy" (inverse) - express as percentage
13. For Location: Use municipality/kommun level (administrative area), NOT smaller towns. Example: "Sigtuna" NOT "Märsta".
14. For Broker: Extract brand/professional name, not full legal entity name. "Croisette" NOT "CCap Market AB (Croisette)".

You extract deal information from broker PDFs, IMs, and teasers."""

INBOUND_USER_PROMPT = """Extract the deal details from this document text.

Return a JSON object with these fields (use null if not explicitly stated):
{{
  "Type": "<'IM' if Investment Memorandum, 'Teaser' if teaser/summary document, null if unclear>",
  "Project Name": "<document/property name - not a generic title like 'Investment Memorandum'>",
  "Seller": "<seller name if stated>",
  "Broker": "<broker/advisor brand name - if format is 'Company (Brand)' or 'Company - Brand', extract the brand (e.g., 'Croisette' not 'CCap Market AB')>",
  "Country": "<Sweden|Denmark|Finland or local name>",
  "Location": "<municipality/kommun name (NOT town/locality) - e.g., 'Sigtuna' not 'Märsta', 'Stockholm' not 'Södermalm'>",
  "Portfolio": <true if multiple properties, false if single, null if unclear>,
  "Address": "<street address with number, e.g. 'Storgatan 12' - NOT city name>",
  "Postal code": "<postal code if stated>",
  "Property designation": "<property designation/fastighetsbeteckning if stated>",
  "Use": "<property type/use as described>",
  "Leasable area, sqm": "<area with units as written>",
  "Base rent": "<base rent/grundhyra/bashyra per sqm as written - look for 'hyra', 'bashyra', 'grundhyra' followed by kr/sqm or SEK/m²>",
  "NOI": "<total NOI/driftnetto as single number with currency - NOT per sqm>",
  "WAULT": "<WAULT in years as written>",
  "Occupancy": "<occupancy rate / uthyrningsgrad as percentage>",
  "Yield": "<yield percentage if stated>",
  "Deal value": "<asking price/deal value with currency as written>",
  "Comments": "<2-3 factual sentences: property description + key metrics (area, rent, NOI, yield) if available>"
}}

DOCUMENT TEXT:
{document_text}

JSON OUTPUT:"""
