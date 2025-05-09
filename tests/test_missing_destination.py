"""
Test Script: test_missing_destination.py
Description:
This automated test validates negative input handling on Delta's "Book a Flight" feature.
Specifically, it verifies that submitting the booking form without a destination ("To") field
produces the expected client-side validation error.

Test Scenario:
- TC_TS6_001: Attempt to Book with Missing Destination Field

Tools:
- Python
- Chat GPT / Google Gemini
- Playwright (sync API)
- Pytest (with HTML reporting)

Data-driven from: testdata/testdata.csv

Author: Sean Tabrizi
Date: May 05, 2025
"""
import pandas as pd
import pytest
from utils.data_loader import load_test_data    #utility test data loader
from playwright.sync_api import sync_playwright
from pages.booking_page import BookingPage

# NOTE: Marking this test as a negative test case, focusing on invalid input validation
@pytest.mark.negative
def test_missing_destination_field():
    """
    Test Case ID: TC_TS6_001
    Title: Attempt to Book with Missing Destination Field
    Objective: Verify that the system displays a validation error
               when the destination ('To') field is left empty.
    """

    # Load test data values from CSV
    URL, FROM_AIRPORT, FROM_FULL_NAME, DEPART_DATE, RETURN_DATE, BROWSER, CICD = load_test_data("testdata/testdata.xlsx")



    # Start Playwright session with Chromium in headed mode for visual debugging
    with sync_playwright() as p:
        
        if BROWSER == "Chrome":
            browser = p.chromium.launch(headless=(CICD == "Yes"))
        elif BROWSER == "Edge":
            browser = p.chromium.launch(channel="msedge", headless=(CICD == "Yes"))
        else:
            browser = p.firefox.launch(headless=(CICD == "Yes"))



        # NOTE: helps with Headless view size
        # BUG: Headless Chrome/Edge not allowed on Delta
        context = browser.new_context(viewport={"width": 1280, "height": 1024})
        # context = browser.new_context()

        page = context.new_page()

        # Navigate to URL
        page.goto(URL)
        page.wait_for_timeout(2000)  # 2-second wait

        #NOTE: Dump the HTML content to a file for debugging
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(page.content())

        # Initialize BookingPage with the Playwright page object
        booking = BookingPage(page)

        # Handle initial modals (language selector, cookies)
        booking.close_language_modal()
        booking.accept_cookie_banner()

        # Fill in only the 'From' field using test data
        # Note: 'To' field is intentionally left blank for this negative test
        booking.fill_from_location(FROM_AIRPORT, FROM_FULL_NAME)

        # Select valid departure and return dates
        booking.fill_depart_and_return_dates(DEPART_DATE, RETURN_DATE)

        # Attempt to submit the flight search form
        booking.click_search()

        # Assert that a validation error is displayed for the missing destination
        assert booking.is_to_field_error_visible(), (
            "Expected validation error for missing destination field was not displayed."
        )

        # Cleanup: close the browser
        browser.close()
