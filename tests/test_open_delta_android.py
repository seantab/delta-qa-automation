"""
Test Script: test_open_delta_android.py
Description:
Automates opening www.delta.com on a real Android device's Chrome browser using Appium.
This script connects to a locally running Appium server and uses test data from an Excel file.

Author: Sean Tabrizi
Date: April 2025
"""

import pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
import openpyxl

# === Utility to load test data from XLSX file ===
def load_test_data(filepath):
    """
    Loads the URL to open from a given Excel file.

    Args:
        filepath (str): Path to the test data Excel file.

    Returns:
        str: The URL to be loaded in the mobile browser.
    """
    workbook = openpyxl.load_workbook(filepath)
    sheet = workbook.active
    url = sheet['A2'].value  # Assume A1 is header, A2 is the value
    return url

@pytest.mark.mobile
def test_open_delta_android():
    """
    Test: Open www.delta.com on real Android device using Chrome browser.
    """

    # === Load test data ===
    URL = load_test_data("testdata/testdata.xlsx")

    # === Define Appium options (using UiAutomator2Options) ===
    options = UiAutomator2Options()
    options.platform_name = "Android"                    # Target mobile platform
    options.device_name = "Android Device"                # Name shown under adb devices
    options.browser_name = "Chrome"                       # Open Chrome browser on device
    options.automation_name = "UiAutomator2"              # Native Android automation driver
    options.chromedriver_executable = "Drivers/chromedriver_ver136.0.7103.92.exe"  
    # Relative path to specific Chromedriver executable matching the Chrome version on device
    # (Placed under Playwright/Drivers/ directory for easier GitHub tracking)


    # === Connect to Appium server running on localhost ===
    driver = webdriver.Remote(command_executor='http://127.0.0.1:4723', options=options)

    try:
        # === Navigate to Delta's homepage ===
        driver.get(URL)

        # === Validate Delta page title ===
        assert "Delta" in driver.title or "delta" in driver.title, "Delta site did not open properly."

    finally:
        # === Always close the session ===
        driver.quit()
