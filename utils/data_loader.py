# ========================================
# Data Loader Utility
# ----------------------------------------
# Purpose:
#   Reads test configuration from an Excel file (XLSX)
#   Applies default values for browser and CICD flags
#   Returns structured test inputs for use in test cases
#
# Used by:
#   test_missing_destination.py
#
# Author: Sean Tabrizi
# ========================================

import pandas as pd

# -------------------------------
# Load and parse the XLSX test data file
# -------------------------------
def load_test_data(filepath: str):
    df = pd.read_excel(filepath)
    row = df.iloc[0]  # Read the first test case row only

    # -------------------------------
    # Handle optional fields with defaults
    # -------------------------------
    browser = row.get("Browser", "Firefox") or "Firefox"  # Default to Firefox
    cicd = row.get("CICD", "No") or "No"                  # Default to headed mode (No)

    # -------------------------------
    # Return structured test inputs
    # -------------------------------
    return (
        row["url"],
        row["from_airport"],
        row["from_full_name"],
        row["depart_date"],
        row["return_date"],
        browser.strip().capitalize(),
        cicd.strip().capitalize()
    )
