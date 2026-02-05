"""
Test fixtures for date normalization.
Each tuple: (input, expected_output, expected_confidence)
"""

DATE_TEST_CASES = [
    # Already correct format
    ("2024/01/15", "2024/01/15", "high"),
    ("2024/1/5", "2024/01/05", "high"),

    # ISO format
    ("2024-01-15", "2024/01/15", "high"),
    ("2024-1-5", "2024/01/05", "high"),

    # European with slashes (dd/mm/yyyy)
    ("15/01/2024", "2024/01/15", "high"),
    ("5/1/2024", "2024/01/05", "high"),

    # European with dots (dd.mm.yyyy)
    ("15.01.2024", "2024/01/15", "high"),
    ("5.1.2024", "2024/01/05", "high"),

    # European with dashes (dd-mm-yyyy)
    ("15-01-2024", "2024/01/15", "high"),

    # Text format - English
    ("January 15, 2024", "2024/01/15", "high"),
    ("15 January 2024", "2024/01/15", "high"),
    ("Jan 15, 2024", "2024/01/15", "high"),
    ("15 Jan 2024", "2024/01/15", "high"),

    # Text format - Swedish
    ("15 januari 2024", "2024/01/15", "high"),
    ("15 februari 2024", "2024/02/15", "high"),
    ("15 mars 2024", "2024/03/15", "high"),
    ("15 maj 2024", "2024/05/15", "high"),

    # Edge cases - empty/null
    ("", "", "low"),
    (None, "", "low"),
    ("   ", "", "low"),

    # Invalid dates
    ("not a date", "", "low"),
    ("32/01/2024", "", "low"),  # Invalid day
]
