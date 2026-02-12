"""
Test fixtures for full row normalization.
"""

# Sample inbound row - before normalization
# Note: "Type" is document type (IM/Teaser), not property type
# "Use" is the property type field
SAMPLE_INBOUND_RAW = {
    "Date received": "15 januari 2024",
    "Type": "IM",
    "Project Name": "Test Project Alpha",
    "Country": "Sweden",
    "Location": "Stockholm",
    "Use": "office building",
    "Leasable area, sqm": "15 000",
    "NOI, CCY": "2.5M",
    "Yield": "4.5%",
    "Economic occupancy rate, %": "95%",
    "Comment": "Test comment",
}

# Expected output after normalization
SAMPLE_INBOUND_EXPECTED = {
    "Date received": "2024/01/15",
    "Type": "IM",  # Document type passes through unchanged
    "Project Name": "Test Project Alpha",
    "Country": "Sweden",
    "Location": "Stockholm",
    "Use": "Office",  # Property type gets normalized
    "Leasable area, sqm": 15000,
    "NOI, CCY": 2500000,
    "Yield": 4.5,
    "Economic occupancy rate, %": 95,
    "Comment": "Test comment",
}

# Sample transactions row - before normalization
# Note: Price is now extracted in millions (e.g., 150 = 150 million)
# The renderer routes it to the correct country-specific column
SAMPLE_TRANSACTIONS_RAW = {
    "Country": "Sweden",
    "Date": "2024-01-15",
    "Buyer": "Buyer Corp",
    "Seller": "Seller AB",
    "Location": "Gothenburg",
    "Property type": "lager",
    "Area, m2": "25,000",
    "Price": 150,  # Price in millions (LLM extracts as number)
    "Yield": "5.25%",
    "Comments": "Industrial warehouse acquisition",
    "Source": "https://example.com/article",
}

# Expected output after normalization
SAMPLE_TRANSACTIONS_EXPECTED = {
    "Country": "Sweden",
    "Date": "2024/01/15",
    "Buyer": "Buyer Corp",
    "Seller": "Seller AB",
    "Location": "Gothenburg",
    "Property type": "Logistics",
    "Area, m2": 25000,
    "Price": 150,  # Price stays in millions
    "Yield": 5.25,
    "Comments": "Industrial warehouse acquisition",
    "Source": "https://example.com/article",
}
