import unittest
from unittest.mock import patch, MagicMock
from selenium.common.exceptions import TimeoutException
import datetime

# Import the functions to be tested.
import volleyball_registration

#hi Houssem was here
#s
#already
class TestVolleyballRegistration(unittest.TestCase):
    @patch('volleyball_registration.notify_user')
    @patch('volleyball_registration.webdriver.Chrome')
    @patch('volleyball_registration.WebDriverWait')
    def test_registration_success(self, mock_wait, mock_chrome, mock_notify):
        """Simulate a successful registration scenario."""
        # Create a mock driver and wait instance.
        mock_driver = MagicMock()
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance

        # Create mock elements for each call:
        date_element = MagicMock()  # For selecting date in select_registration_date
        continue_button = MagicMock()  # For clicking "Continue"
        first_name_field = MagicMock()  # For first name field (via wait.until)
        submit_button = MagicMock()  # For the submit button
        confirmation_element = MagicMock()  # For confirmation message

        # Set up the sequence for wait.until:
        # 1. Date element (select_registration_date)
        # 2. "Continue" button
        # 3. First name field (registration form)
        # 4. Submit button
        # 5. Confirmation element
        mock_wait_instance.until.side_effect = [
            date_element,
            continue_button,
            first_name_field,
            submit_button,
            confirmation_element
        ]

        # Create mocks for driver.find_element calls:
        last_name_field = MagicMock()
        email_field = MagicMock()
        agree_checkbox = MagicMock()
        # Let’s say the checkbox is already selected (or you can set is_selected.return_value = False if you want to test the click)
        agree_checkbox.is_selected.return_value = True
        # Now, the sequence for find_element should be:
        # 1. Last name field
        # 2. Email field
        # 3. Agree checkbox
        mock_driver.find_element.side_effect = [last_name_field, email_field, agree_checkbox]

        # Simulate that no "no times" message is found.
        mock_driver.find_elements.return_value = []

        # Ensure our patched Chrome returns our mock driver.
        mock_chrome.return_value = mock_driver

        # Call the function under test.
        result = volleyball_registration.register_volleyball()

        # Verify that registration was reported as successful.
        self.assertTrue(result)
        mock_notify.assert_any_call("Registration successful!")

    @patch('volleyball_registration.notify_user')
    @patch('volleyball_registration.webdriver.Chrome')
    @patch('volleyball_registration.WebDriverWait')
    def test_no_continue_button(self, mock_wait, mock_chrome, mock_notify):
        """Simulate a case where the 'Continue' button is not found."""
        mock_driver = MagicMock()
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance

        date_element = MagicMock()
        # First call returns date element; second call raises TimeoutException.
        mock_wait_instance.until.side_effect = [
            date_element,
            TimeoutException("Timed out for continue button")
        ]

        # Ensure our patched Chrome returns our mock driver.
        mock_chrome.return_value = mock_driver

        # Call the function.
        result = volleyball_registration.register_volleyball()

        # The registration should fail.
        self.assertFalse(result)
        mock_notify.assert_any_call("Could not find the 'Continue' button. Possibly no available times.")


if __name__ == '__main__':
    unittest.main()
