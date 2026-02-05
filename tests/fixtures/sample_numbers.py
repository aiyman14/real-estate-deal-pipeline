"""
Test fixtures for number normalization.
Each tuple: (input, expected_output, expected_confidence)
"""

# Price/area tests (should return integers)
PRICE_TEST_CASES = [
    # Plain numbers
    ("1500000", 1500000, "high"),
    (1500000, 1500000, "high"),
    (1500000.0, 1500000, "high"),

    # With abbreviations
    ("1.5M", 1500000, "high"),
    ("1.5m", 1500000, "high"),
    ("500k", 500000, "high"),
    ("500K", 500000, "high"),
    ("2.3 million", 2300000, "high"),
    ("1.2 mdr", 1200000000, "high"),
    ("1.2 miljarder", 1200000000, "high"),

    # Swedish currency abbreviations
    ("150 MSEK", 150000000, "high"),
    ("150MSEK", 150000000, "high"),
    ("50 MDKK", 50000000, "high"),
    ("25 MEUR", 25000000, "high"),

    # With currency symbols (should be stripped)
    ("SEK 1500000", 1500000, "high"),
    ("€500000", 500000, "high"),
    ("$1.5M", 1500000, "high"),

    # Formatted numbers - US style (commas as thousands)
    ("1,500,000", 1500000, "high"),

    # Formatted numbers - European style (dots as thousands)
    ("1.500.000", 1500000, "high"),

    # Formatted numbers - space as thousands
    ("1 500 000", 1500000, "high"),

    # Decimals that should round to integer (Python banker's rounding)
    ("1500000.50", 1500000, "high"),  # .5 rounds to even

    # Edge cases
    ("", "", "low"),
    (None, "", "low"),
    ("N/A", "", "low"),
]

# Yield/percentage tests (should preserve decimals)
YIELD_TEST_CASES = [
    ("4.5%", 4.5, "high"),
    ("4.5", 4.5, "high"),
    ("95%", 95, "high"),
    ("4,5%", 4.5, "high"),  # European decimal
    (4.5, 4.5, "high"),
    ("", "", "low"),
    (None, "", "low"),
]

# Area tests (should return integers)
AREA_TEST_CASES = [
    ("15000", 15000, "high"),
    ("15 000", 15000, "high"),
    ("15,000", 15000, "high"),
    ("15.000", 15000, "high"),  # European thousands
    (15000.5, 15000, "high"),  # Banker's rounding: .5 rounds to even
    ("", "", "low"),
]
