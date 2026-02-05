"""
Test fixtures for full row normalization.
"""

# Sample inbound row - before normalization
SAMPLE_INBOUND_RAW = {
    "Date received": "15 januari 2024",
    "Type": "kontorsfastighet",
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
    "Type": "Office",
    "Project Name": "Test Project Alpha",
    "Country": "Sweden",
    "Location": "Stockholm",
    "Use": "Office",
    "Leasable area, sqm": 15000,
    "NOI, CCY": 2500000,
    "Yield": 4.5,
    "Economic occupancy rate, %": 95,
    "Comment": "Test comment",
}

# Sample transactions row - before normalization
SAMPLE_TRANSACTIONS_RAW = {
    "Date": "2024-01-15",
    "Buyer": "Buyer Corp",
    "Seller": "Seller AB",
    "Location": "Gothenburg",
    "Property type": "lager",
    "Area, m2": "25,000",
    "Price, SEK": "150 MSEK",
    "Yield": "5.25%",
    "Comments": "Industrial warehouse acquisition",
    "Source URL": "https://example.com/article",
}

# Expected output after normalization
SAMPLE_TRANSACTIONS_EXPECTED = {
    "Date": "2024/01/15",
    "Buyer": "Buyer Corp",
    "Seller": "Seller AB",
    "Location": "Gothenburg",
    "Property type": "Logistics",
    "Area, m2": 25000,
    "Price, SEK": 150000000,
    "Yield": 5.25,
    "Comments": "Industrial warehouse acquisition",
    "Source URL": "https://example.com/article",
}
