
import re
from playwright.sync_api import Page

class BookingPage:
    def __init__(self, page: Page):
        self.page = page

        # ===== Selectors for key page elements =====
        self.language_modal_button = "text=United States - English"
        self.cookie_ack_button = 'button:has-text("I understand")'
        self.search_button = 'button:has-text("Search") >> visible=true'
        
        # #role-based locator
        # self.search_button = self.page.get_by_role("button", name=re.compile("Search", re.I)).filter(has_text="Search") # role-based locator

        
        self.error_to_field = 'div:has-text("Please enter a destination")'

    def close_language_modal(self):
        """
        Dismiss the language/location modal if it appears.
        """
        if self.page.is_visible(self.language_modal_button):
            self.page.click(self.language_modal_button)

    def accept_cookie_banner(self):
        """
        Accept the cookie consent banner if it's present at the bottom of the page.
        """
        if self.page.is_visible(self.cookie_ack_button):
            self.page.click(self.cookie_ack_button)


    def fill_from_location(self, airport_code: str, airport_full_name: str):
        """
        Opens the 'From' airport selector modal, fills in the airport code,
        and selects the correct option from the dropdown list (e.g., 'ATL Atlanta, GA').
        """
        link = self.page.get_by_role("link", name="From Departure Airport or")  # Adding a wait for the "From" element before clicking to fix headless Chrome execution
        link.wait_for(state="visible", timeout=10000)
        link.click()

        textbox = self.page.get_by_role("textbox", name="Origin City or Airport")
        textbox.wait_for()
        textbox.fill(airport_code)

        self.page.get_by_role("link", name=airport_full_name).click()

        self.page.wait_for_timeout(1000)

    
    def fill_depart_and_return_dates(self, depart: str, return_: str):
        """
        Opens the calendar, selects departure and return dates.
        More resilient version for dynamic or split buttons.
        """
        # Step 1: Look for a broader match like "Depart"
        try:
            calendar_button = self.page.get_by_role("button", name=re.compile("Depart", re.I))
            calendar_button.wait_for(state="visible", timeout=10000)
            calendar_button.click()
        except Exception as e:
            raise Exception("Unable to find or click the Depart button. Check selector or page load.") from e

        # Step 2: Wait for calendar popup
        self.page.wait_for_timeout(1000)

        # Step 3: Select dates
        try:
            self.page.get_by_role("link", name=depart).click(timeout=5000)
            self.page.get_by_role("link", name=return_).click(timeout=5000)
        except Exception as e:
            raise Exception(f"Could not select one or both dates: {depart}, {return_}") from e

        # Step 4: Click "Done" or "Confirm"
        try:
            self.page.get_by_role("button", name=re.compile("Done|Apply", re.I)).click(timeout=5000)
        except Exception as e:
            raise Exception("Unable to find or click the 'Done' button after selecting dates.") from e




    def click_search(self):
        """
        Click the 'Search' button to submit the flight search form.
        Waits until the button is visible and interactable.
        """
        button = self.page.locator(self.search_button).first
        button.wait_for(state="visible", timeout=10000)
        button.wait_for(state="attached", timeout=10000)
        button.click()


    def is_to_field_error_visible(self) -> bool:
        """
        Check for a validation error related to the missing 'To' (destination) field.
        Used in TS6 to confirm UI-level input validation is triggered.
        """
        return self.page.is_visible(self.error_to_field)
