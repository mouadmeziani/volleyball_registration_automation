# Volleyball Registration Automation

A production-grade Selenium automation script that solves a real-world problem: automatically booking competitive volleyball slots that fill up within minutes of opening.

## The Problem

The university sports program releases volleyball slots every week on a first-come, first-served basis. Slots open at a specific time and are typically gone within 2-3 minutes. Manual registration requires:
- Being available at the exact release time
- Fast internet connection
- Quick typing and clicking
- Luck

This script automates the entire flow, ensuring I never miss registration.

## Features

- **Auto-date calculation** - Automatically finds and selects next Thursday's session
- **Robust error handling** - Handles timeouts, element interception, missing elements
- **Multiple click strategies** - Falls back to JavaScript click when normal clicks fail
- **Desktop notifications** - Popup alerts for success/failure (optional)
- **Headless mode** - Runs in background without opening browser window
- **Unit tested** - Comprehensive mocking-based tests for reliability
- **Selenium IDE tests** - Browser extension tests for validation

## How It Works

1. Opens the volleyball booking page in Brave browser
2. Calculates next Thursday's date automatically
3. Navigates through the booking calendar
4. Checks for available time slots
5. Fills registration form (name, email)
6. Accepts terms and conditions
7. Submits registration
8. Waits for confirmation message
9. Sends desktop notification with result

## Tech Stack

- **Python 3.x**
- **Selenium WebDriver** - Browser automation
- **ChromeDriver** - Brave browser control
- **Tkinter** - Desktop notifications
- **unittest + mock** - Testing framework

## Setup

```bash
# Install dependencies
pip install selenium

# Configure paths in volleyball_registration.py
BRAVE_PATH = r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe"
CHROMEDRIVER_PATH = r"path\to\chromedriver.exe"

# Set your registration details
FIRST_NAME = "Your Name"
LAST_NAME = "Your Last Name"
EMAIL = "your.email@example.com"
```

## Usage

**Manual run:**
```bash
python volleyball_registration.py
```

**Scheduled run (recommended):**
```bash
# Windows Task Scheduler
# Run every Thursday at 12:00 PM (when slots open)

# Linux/macOS cron
0 12 * * 4 /usr/bin/python3 /path/to/volleyball_registration.py
```

## Error Handling

The script handles multiple failure scenarios:

- **No available slots** - Detects "no times to choose from" message
- **Timeout errors** - Retries with extended wait times
- **Element click failures** - Falls back to JavaScript execution
- **Missing form fields** - Validates presence before filling
- **Network issues** - Comprehensive exception catching

## Testing

```bash
# Run unit tests
python test_volleyball_registration.py

# Selenium IDE tests
# 1. Install Selenium IDE browser extension
# 2. Import extension testing/volleyball1_regsiteration.side
# 3. Run test suite
```

**Test coverage:**
- Successful registration flow (mocked)
- Button not found scenario
- Form field validation
- Confirmation message detection

## Code Quality

**Error Handling:**
```python
try:
    continue_btn.click()
except ElementClickInterceptedException:
    driver.execute_script("arguments[0].click();", continue_btn)
```

**Explicit Waits (not implicit):**
```python
wait = WebDriverWait(driver, 20)
date_element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
```

**XPath Robustness:**
```python
xpath = (
    f"//div[contains(@class, 'date-item') and contains(@title, 'Donnerstag') "
    f"and .//div[normalize-space(text())='{target_day}']]"
)
```

## Known Limitations

- **Hardcoded to anny.co** - Currently specific to this booking platform
- **German language dependency** - XPath searches for "Donnerstag" (Thursday)
- **Single-use case** - Only handles volleyball registration flow
- **Windows path format** - Uses Windows-style paths for Brave/ChromeDriver

## Future Enhancements

Planning to generalize this into a reusable booking automation framework:

- [ ] Config-driven site definitions (YAML)
- [ ] Plugin system for different booking platforms
- [ ] Multi-language support
- [ ] Webhook notifications (Slack, Discord)
- [ ] Retry strategies (exponential backoff)
- [ ] Docker containerization
- [ ] Cloud deployment (AWS Lambda, GitHub Actions)

See [framework roadmap](https://github.com/mouadmeziani/activity-booking-automation) for detailed enhancement plan.

## Collaboration

Special thanks to **Houssem** for contributions to the test suite and helpful debugging comments throughout the code.

## Lessons Learned

**What worked well:**
- JavaScript click fallback solved 90% of element interception issues
- Explicit waits are far more reliable than implicit waits or `time.sleep()`
- Desktop notifications provide instant feedback without watching the script
- Unit testing with mocks caught edge cases before production

**What I'd do differently:**
- Extract configuration to external file (currently hardcoded)
- Add logging framework instead of print statements
- Implement retry logic at the top level (currently only retries individual steps)
- Use environment variables for sensitive data (email, name)
- Add screenshot capture on failure for debugging

## Real-World Impact

This script has successfully registered me for volleyball sessions **100% of the time** over the past 3 months, eliminating the stress of manual registration and ensuring I never miss a session due to being unavailable at release time.

---

**Status:** Production (actively used)  
**Maintenance:** Updated as booking site changes  
**License:** Personal use
