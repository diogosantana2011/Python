import random
import time
import logging
import re
from typing import Callable, List, Optional, Tuple
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.remote.webelement import WebElement
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

# Constants
MAX_RETRIES = 3
CLICK_DELAY = 0.2
SCROLL_DELAY = 0.1
MIN_TEXT_LENGTH = 5
MAX_TEXT_LENGTH = 15
MIN_SCROLL_PIXELS = 100
MAX_SCROLL_PIXELS = 900

DANGEROUS_KEYWORDS = [
    'delete', 'remove', 'logout', 'sign out',
    'withdraw', 'transfer', 'pay', 'submit payment',
    'close account', 'cancel', 'sign-out', 'deactivate'
]

DEFAULT_ERROR_PATTERNS = [
    'error', 'something went wrong', 'unexpected error',
    'internal server error', '500', '404', 'not found',
    'exception', 'failed', 'undefined is not a function',
    'cannot read property', 'null is not an object'
]

class MonkeyTestLibrary:
    """
    MonkeyTestLibrary for Robot Framework.

    This library provides automated "monkey testing" for web applications, 
    performing randomized UI interactions to uncover stability issues, 
    JavaScript errors, and unexpected behaviors.

    Key Features:
    - Randomized interactions: clicks, typing, scrolling, dropdown selection, and toggles.
    - Safety checks: avoids destructive actions like delete, logout, or payment triggers.
    - Error detection:
        - Scans page source for HTTP errors, JavaScript exceptions, and common error phrases.
        - Captures screenshots on critical errors.
        - Optionally checks browser console logs for severe and warning-level messages.
    - Monitoring:
        - Can inject a JavaScript listener to capture runtime errors during testing.
    - Configurable:
        - Duration, action frequency, and custom error patterns can be specified.
    - Retry logic:
        - Actions on dynamic elements use retries to handle transient DOM changes.

    Intended Usage:
    - Perform automated exploratory testing to catch regressions or page breakages.
    - Combine with Robot Framework test suites for continuous monitoring.
    - Use `run_monkey_test_with_monitoring` for a comprehensive test that reports JS errors.

    Example:
        | Run Monkey Test With Monitoring | 60 | 2 |
    """    
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self) -> None:
        """Initialize the library."""
        self.builtin = BuiltIn()
        self._setup_logging()

    def _setup_logging(self) -> None:
        """Configure logging format."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )

    def _get_selenium_library(self):
        """
        Run randomized UI interactions (monkey testing).
        \n`duration_seconds`: total runtime in seconds
        \n`actions_per_second`: number of random actions per second
        \nActions include clicking, typing, scrolling, and dropdown selection.
        \nErrors during actions are caught and logged.
        """
        return self.builtin.get_library_instance('SeleniumLibrary')

    @keyword
    def run_monkey_test(self, duration_seconds: int = 60, actions_per_second: int = 2) -> None:
        """
        Run randomized UI interactions (monkey testing).
        \n*Args*:
            - `duration_seconds`: Total runtime in seconds (default: 60)
            - `actions_per_second`: Number of random actions per second (default: 2)
        \nActions include clicking, typing, scrolling, dropdown selection, and toggling.
        \nErrors during actions are caught and logged but don't stop the test.
        \n*Example*:
            | Run Monkey Test | 30 | 3 |
        """
        if duration_seconds <= 0:
            raise ValueError(f"duration_seconds must be positive, got {duration_seconds}")
        if actions_per_second <= 0:
            raise ValueError(f"actions_per_second must be positive, got {actions_per_second}")
        end_time = time.time() + duration_seconds
        base_sleep_time = 1.0 / actions_per_second
        
        action_count = 0
        logging.info(f"Starting monkey test: {duration_seconds}s @ {actions_per_second} actions/sec")

        while time.time() < end_time:
            try:
                self._perform_random_action()
                action_count += 1
            except Exception as err:
                logging.debug(f"Action failed: {str(err)}")
            # Add randomness to sleep time (80-120% of base)
            sleep_time = max(0.1, base_sleep_time * random.uniform(0.8, 1.2))
            time.sleep(sleep_time)
        logging.info(f"Monkey test completed: {action_count} actions performed")

    @keyword
    def verify_no_errors_on_page(self, *expected_errors: str) -> None:
        """
        Scan page source for error messages.
        \nPass custom error strings as arguments, or defaults are used.
        \nCaptures screenshot and fails if critical errors are found.
        \nLogs warnings if minor error-like strings are detected.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        page_source = driver.page_source.lower()
        error_patterns = list(expected_errors) if expected_errors else DEFAULT_ERROR_PATTERNS
        lines = page_source.splitlines()  # Split once, not in loop
        # Precompile all regex patterns for performance
        compiled_patterns = [
            (error_text, re.compile(r'\b' + re.escape(error_text.lower()) + r'\b', re.IGNORECASE))
            for error_text in error_patterns
        ]
        found_errors = []
        for error_text, pattern in compiled_patterns:
            # Quick check: does pattern exist at all?
            if not pattern.search(page_source):
                continue
            # Find matching lines with context
            for line in lines:
                match = pattern.search(line)
                if match:
                    # Extract context around the match (100 chars before, 200 after)
                    context = self._extract_context_around_match(line, match.start(), match.end())
                    found_errors.append(f"'{error_text}' found in: {context}")
                    # Only report first occurrence per pattern
                    break
        if found_errors:
            selenium.capture_page_screenshot()
            error_msg = f"Found {len(found_errors)} error(s) on page:\n  • " + "\n  • ".join(found_errors)
            logging.error(error_msg)
            raise AssertionError(error_msg)
        logging.info(f"No errors found (checked {len(error_patterns)} patterns)")

    def _extract_context_around_match(self, text: str, match_start: int, match_end: int) -> str:
        """
        Extract context around a matched string for better error reporting.
        \n*Args*:
            `text`: Full text containing the match
            `match_start`: Start index of the match
            `match_end`: End index of the match
        \n*Returns*:
            String with context before and after the match, with ellipsis if truncated
        \nShows 100 chars before match and 200 chars after for context.
        """
        CONTEXT_BEFORE = 100
        CONTEXT_AFTER = 200
        MAX_TOTAL_LENGTH = 400
        # Calculate context boundaries
        context_start = max(0, match_start - CONTEXT_BEFORE)
        context_end = min(len(text), match_end + CONTEXT_AFTER)
        # Extract the context
        before = text[context_start:match_start]
        matched = text[match_start:match_end]
        after = text[match_end:context_end]
        # Build result with ellipsis indicators
        result = ""
        if context_start > 0:
            result += "..."
        result += before + matched + after
        if context_end < len(text):
            result += "..."
        # Final safety truncation if still too long (show both ends)
        if len(result) > MAX_TOTAL_LENGTH:
            half = MAX_TOTAL_LENGTH // 2
            result = result[:half] + " [...] " + result[-half:]
        # Clean up whitespace for readability
        result = ' '.join(result.split())
        return result

    @keyword
    def verify_no_console_errors(self) -> None:
        """
        Check browser console logs for JavaScript errors.
        \nCaptures screenshot and fails if severe console errors are present.
        \nLogs warnings if available.
        \nFalls back gracefully if logs are unavailable.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        try:
            logs = driver.get_log('browser')
            severe_logs = [log for log in logs if log['level'] == 'SEVERE']
            warning_logs = [log for log in logs if log['level'] == 'WARNING']

            if severe_logs:
                messages = [log['message'] for log in severe_logs]
                selenium.capture_page_screenshot()
                error_msg = f"Console errors found ({len(severe_logs)}):\n  • " + "\n  • ".join(messages[:5])
                logging.error(error_msg)
                raise AssertionError(error_msg)
            
            if warning_logs:
                logging.warning(f"Console warnings found ({len(warning_logs)})")
                for log in warning_logs[:3]:  # Log first 3
                    logging.warning(f"  • {log['message']}")
            logging.info("No severe console errors found")
        except Exception as err:
            logging.warning(f"Could not check console logs: {str(err)}")

    @keyword
    def verify_page_health(self, *custom_error_messages: str) -> None:
        """
        Combined health check for a page.
        \nRuns verify_no_errors_on_page and verify_no_console_errors.
        \nOptionally pass custom error strings to override defaults.
        \nUseful as a quick stability check after navigation or action.
        """
        logging.info("Running page health check...")

        if custom_error_messages:
            self.verify_no_errors_on_page(*custom_error_messages)
        else:
            self.verify_no_errors_on_page()

        self.verify_no_console_errors()
        logging.info("Page health check passed")

    def _perform_random_action(self) -> None:
        """
        Select and perform a random UI action.
        \nAvailable actions weighted by likelihood:
        - Click (2x weight)
        - Type
        - Scroll
        - Select dropdown
        - Toggle
        """
        actions = [
            # 2x weight for clicks
            self._random_click,
            self._random_click,
            self._random_type,
            self._random_scroll,
            self._random_select,
            self._random_toggle
        ]
        random_action = random.choice(actions)
        random_action()
        logging.info(f"Random action: {random_action.__name__}")

    def _safe_element_action(
        self, 
        action_func: Callable[[], None], 
        description: str, 
        max_retries: int = MAX_RETRIES
    ) -> bool:
        """
        Execute an action with retry logic.
        \n*Args*:
            `action_func`: Function to execute
            `description`: Description for logging
            `max_retries`: Maximum number of retry attempts
        \n*Returns*:
            True if action succeeded, False otherwise
        """
        for attempt in range(max_retries):
            try:
                action_func()
                logging.debug(f"Description: {description}")
                return True
            except (StaleElementReferenceException, NoSuchElementException) as err:
                if attempt == max_retries - 1:
                    logging.debug(f"Description: {description} failed after {max_retries} attempts")
                else:
                    logging.debug(f"Retry {attempt + 1}/{max_retries} for {description}")
                time.sleep(0.1)
            except Exception as err:
                logging.debug(f"Description: {description} failed: {type(err).__name__}")
                break
        return False

    def _random_click(self) -> None:
        """
        Click a random safe clickable element.
        \nTargets buttons, links, inputs, and common custom button elements.
        \nFilters out dangerous elements (delete, logout, etc.).
        \nSkips hidden or disabled elements.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        clickable = driver.find_elements(
            'xpath',
            '//button'
            ' | //a[@href]'
            ' | //input[@type="button" or @type="submit" or @type="reset"]'
            ' | //*[@role="button"]'
            ' | //*[@onclick]'
            ' | //div[contains(@class, "btn") or contains(@class, "button")]'
            ' | //span[contains(@class, "btn") or contains(@class, "button")]'
        )
        # Filter for safe, visible, enabled elements
        safe_elements = [
            el for el in clickable
            if el.is_displayed()
            and el.is_enabled()
            and not self._is_dangerous_element(el)
        ]
        if not safe_elements:
            logging.debug("No safe clickable elements found")
            return
        element = random.choice(safe_elements)
        element_desc = self._get_element_description(element)
        def click_action():
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(CLICK_DELAY)
            element.click()
            time.sleep(CLICK_DELAY)
        if self._safe_element_action(click_action, f"Click: {element_desc}"):
            logging.info(f"Clicked: {element_desc}")

    def _random_type(self) -> None:
        """
        Type random alphanumeric text into an input or textarea.
        \nClears field before typing.
        \nTarget fields include text, email, search, password, tel, number, url, and textarea.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        inputs = driver.find_elements(
            'xpath',
            '//input[@type="text" or @type="email" or @type="search" '
            'or @type="password" or @type="tel" or @type="number" or @type="url"] '
            '| //textarea'
        )
        safe_inputs = [
            el for el in inputs
            if el.is_displayed() 
            and el.is_enabled() 
            and not el.get_attribute('readonly')
        ]
        if not safe_inputs:
            logging.debug("No input fields found for typing")
            return
        element = random.choice(safe_inputs)
        input_type = element.get_attribute('type') or 'text'
        text_length = random.randint(MIN_TEXT_LENGTH, MAX_TEXT_LENGTH)
        # Generate appropriate text based on input type
        if input_type in ['number', 'tel']:
            random_text = ''.join(random.choices('0123456789', k=text_length))
        elif input_type == 'email':
            random_text = f"test{random.randint(1000, 9999)}@example.com"
        else:
            chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
            random_text = ''.join(random.choices(chars, k=text_length))
        def type_action():
            element.clear()
            element.send_keys(random_text)
        if self._safe_element_action(type_action, f"Type into {input_type} field"):
            logging.info(f"Typed '{random_text}' into {input_type} field")

    def _random_scroll(self, min_pixels: int = MIN_SCROLL_PIXELS, max_pixels: int = MAX_SCROLL_PIXELS) -> None:
        """
        Scroll the page randomly.
        \n*Args*:
            `min_pixels`: Minimum scroll distance (default: 100)
            `max_pixels`: Maximum scroll distance (default: 900)
        \nDirection is randomly up or down.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        direction = random.choice([-1, 1])
        pixels = random.randint(min_pixels, max_pixels)
        try:
            driver.execute_script(f"window.scrollBy(0, {direction * pixels})")
            direction_text = 'down' if direction > 0 else 'up'
            logging.info(f"Scrolled {direction_text} by {pixels}px")
            time.sleep(SCROLL_DELAY)
        except Exception as err:
            logging.debug(f"Scroll failed: {str(err)}")

    def _random_select(self) -> None:
        """
        Select a random option from a dropdown.
        \nHandles both native <select> elements and custom dropdowns.
        \nSkips first option (usually placeholder) and hidden items.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        # Try native select first
        selects = driver.find_elements('tag name', 'select')
        if selects:
            select_element = random.choice(selects)
            options = [o for o in select_element.find_elements('tag name', 'option') if o.is_displayed()]
            if len(options) > 1:
                def select_action():
                    # Skip first (placeholder)
                    chosen = random.choice(options[1:])
                    chosen.click()
                if self._safe_element_action(select_action, "Select dropdown option"):
                    logging.info(f"Selected option from native dropdown")
            return
        # Try custom dropdowns
        dropdowns = driver.find_elements(
            'xpath',
            '//*[contains(@class,"dropdown") and (contains(@class,"select") or @role="listbox")]'
        )
        safe_dropdowns = [dd for dd in dropdowns if dd.is_displayed()]
        if safe_dropdowns:
            dropdown = random.choice(safe_dropdowns)
            def custom_select_action():
                dropdown.click()
                time.sleep(0.3)
                options = dropdown.find_elements('xpath', './/li[not(contains(@class, "disabled"))]')
                if options:
                    random.choice(options).click()
            if self._safe_element_action(custom_select_action, "Select custom dropdown"):
                logging.info(f"Selected option from custom dropdown")
        else:
            logging.debug("No dropdown elements found")

    def _random_toggle(self) -> None:
        """
        Click random toggle elements if present.
        \nTargets any element with a class containing 'toggle'.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver

        toggles = driver.find_elements('xpath', '//*[contains(@class,"toggle")]')
        safe_toggles = [t for t in toggles if t.is_displayed() and t.is_enabled()]

        if not safe_toggles:
            logging.debug("No toggle elements found")
            return
        
        toggle = random.choice(safe_toggles)
        
        def toggle_action():
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
            time.sleep(0.1)
            toggle.click()
        
        if self._safe_element_action(toggle_action, "Toggle element"):
            classes = toggle.get_attribute('class')
            logging.info(f"Toggled element with classes: {classes}")

    def _is_dangerous_element(self, element: WebElement) -> bool:
        """
        Detect if element is potentially destructive.
        \n*Args*:
            `element`: WebElement to check
        \n*Returns*:
            True if element matches dangerous keywords, False otherwise
        \nMatches keywords like delete, logout, withdraw, cancel, etc.
        """
        try:
            text = (element.text or '').lower()
            elem_id = (element.get_attribute('id') or '').lower()
            elem_class = (element.get_attribute('class') or '').lower()
            combined = f"{text} {elem_id} {elem_class}"
            return any(keyword in combined for keyword in DANGEROUS_KEYWORDS)
        except Exception:
            return False

    def _get_element_description(self, element: WebElement) -> str:
        """
        Get a human-readable description of an element.
        \n*Args*:
            - `element`: WebElement to describe
        \n*Returns*:
            String description of the element
        """
        try:
            tag = element.tag_name
            text = (element.text or '').strip()[:30]
            elem_id = element.get_attribute('id') or ''
            
            if text:
                return f"{tag}[{text}]"
            elif elem_id:
                return f"{tag}#{elem_id}"
            else:
                return tag
        except Exception:
            return "unknown element"

    @keyword
    def run_monkey_test_with_monitoring(self, duration_seconds: int = 60, actions_per_second: int = 2) -> None:
        """
        Run monkey testing with JavaScript error monitoring.
        \n*Args*:
            - `duration_seconds`: Total runtime in seconds (default: 60)
            - `actions_per_second`: Number of random actions per second (default: 2)
        \nInjects error listener into browser to capture runtime errors.
        \nAfter test run, collected errors are checked.
        \nFails with screenshot if JavaScript errors were found.
        \n*Example*:
            | Run Monkey Test With Monitoring | 45 | 3 |
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        # Inject error monitoring script
        driver.execute_script("""
            window.monkeyTestErrors = [];
            window.addEventListener('error', function(e) {
                window.monkeyTestErrors.push({
                    message: e.message,
                    source: e.filename,
                    line: e.lineno
                });
            });
            console.log('Monkey test error monitoring initialized');
        """)
        # Run the test
        self.run_monkey_test(duration_seconds, actions_per_second)
        # Check for errors
        js_errors = driver.execute_script("return window.monkeyTestErrors || []")
        if js_errors:
            error_summary = [f"{err.get('message', 'Unknown error')}" for err in js_errors]
            selenium.capture_page_screenshot()
            error_msg = f"Monkey test found {len(js_errors)} JavaScript error(s):\n  • " + "\n  • ".join(error_summary[:5])
            logging.error(error_msg)
            raise AssertionError(error_msg)
        logging.info("Monkey test completed with no JavaScript errors")
