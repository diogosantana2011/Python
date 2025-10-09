import random
import time
import logging
import re
from selenium.common.exceptions import StaleElementReferenceException
from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn

class MonkeyTestLibrary:
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self) -> None:
        self.builtin = BuiltIn()

    def _get_selenium_library(self):
        """Get the existing SeleniumLibrary instance from Robot Framework"""
        return self.builtin.get_library_instance('SeleniumLibrary')

    @keyword
    def run_monkey_test(self, duration_seconds: int = 60, actions_per_second: int = 2) -> None:
        """
        Run randomized UI interactions (monkey testing).
        \n`duration_seconds`: total runtime in seconds
        \n`actions_per_second`: number of random actions per second
        \nActions include clicking, typing, scrolling, and dropdown selection.
        \nErrors during actions are caught and logged.
        """
        end_time = time.time() + int(duration_seconds)
        sleep_time = max(0.1, 1.0 / actions_per_second * random.uniform(0.8, 1.2))

        while time.time() < end_time:
            try:
                self._perform_random_action()
            except (Exception, StaleElementReferenceException) as err:
                logging.info(f"Action failed: {str(err)}")
            time.sleep(sleep_time)

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
        # Default error messages if none provided
        if not expected_errors:
            expected_errors = (
                'error',
                'something went wrong',
                'unexpected error',
                'internal server error',
                '500',
                '404',
                'not found',
                'exception',
                'failed',
                'undefined is not a function',
                'cannot read property',
                'null is not an object'
            )
        found_critical = []
        found_warning = []
        found_info = []
        for err in expected_errors:
            err_lower = err.lower()
            # Regex: match exact word or phrase
            pattern = r'\b' + re.escape(err_lower) + r'\b'
            matches = re.finditer(pattern, page_source, flags=re.IGNORECASE)
            # Only log if a match exists
            if matches:
                lines = page_source.splitlines()
                matching_lines = [line.strip() for line in lines if re.search(pattern, line, flags=re.IGNORECASE)]
                if matching_lines:
                    log_msg = f"{err} -> {' | '.join(matching_lines)}"
                    if err_lower in ('500',
                                     'internal server error',
                                     'undefined is not a function',
                                     'cannot read property',
                                     'null is not an object'):
                        found_critical.append(log_msg)
                    elif err_lower in ('400', '404', 'not found'):
                        found_warning.append(log_msg)
                    else:
                        found_info.append(log_msg)
        if found_critical:
            selenium.capture_page_screenshot()
            logging.error(f"Critical errors found: {', '.join(found_critical)}")
        if found_warning:
            logging.warning(f"Warnings found: {', '.join(found_warning)}")
        if found_info:
            logging.info(f"Info-level messages found: {', '.join(found_info)}")
        if not (found_critical or found_warning or found_info):
            logging.info(f"No errors found from list: {', '.join(expected_errors)}")

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
            severe = [log for log in logs if log['level'] == 'SEVERE']
            warnings = [log for log in logs if log['level'] == 'WARNING']

            if severe:
                messages = [log['message'] for log in severe]
                selenium.capture_page_screenshot()
                logging.error(f"Console errors found: {messages}")
            if warnings:
                logging.warning(f"Console warnings: {[log['message'] for log in warnings]}")
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
        \nAvailable actions: click, type, scroll, dropdown select.
        \nUsed internally by run_monkey_test.
        """
        actions = [
            # x2 weight for clicks
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

    def _random_click(self) -> None:
        """
        Click a random safe clickable element.
        \nIncludes buttons, links, inputs, and common custom button elements.
        \nFilters out elements with destructive actions like delete or logout.
        \nSkips hidden or disabled elements.
        \nLogs which element was clicked or why it failed.
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
        # Filter safe, visible, enabled elements
        safe_elements = [
            el for el in clickable
            if el.is_displayed()
            and el.is_enabled()
            and not self._is_dangerous_element(el)
        ]

        if safe_elements:
            element = random.choice(safe_elements)
            for attempt in range(3):
                try:
                    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                    logging.info(f"Sleeping 0.2s")
                    time.sleep(0.2)
                    element.click()
                    logging.info(f"Sleeping 0.2s")
                    time.sleep(0.2)
                    logging.info(f"Clicked element: tag={element.tag_name}, text='{element.text.strip()}'")
                    break
                except (Exception, StaleElementReferenceException) as err:
                    logging.info(f"Failed to click element: tag={element.tag_name}, text='{element.text.strip()}', error={str(err)}")
            else:
                logging.info("No safe clickable elements found.")

    def _random_scroll(self, min_pixels: int=100, max_pixels=900) -> None:
        """
        Scroll the page randomly.
        \nDirection is up or down.
        \nScroll distance is between 100-500 pixels.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver

        direction = random.choice([-1, 1])
        pixels = random.randint(min_pixels, max_pixels)
        driver.execute_script(f"window.scrollBy(0, {direction * pixels})")
        logging.info(f"Scrolled {'down' if direction > 0 else 'up'} by {pixels} pixels.")

    def _random_select(self) -> None:
        """
        Select a random option from a dropdown.
        \nCovers native <select> tags and common custom dropdowns (div/ul).
        \nSkips first placeholder option and hidden items.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver
        # 1. Native select
        selects = driver.find_elements('tag name', 'select')
        if selects:
            select_element = random.choice(selects)
            options = [o for o in select_element.find_elements('tag name', 'option') if o.is_displayed()]
            if len(options) > 1:
                for attempt in range(3):
                    try:
                        # skip first placeholder
                        chosen = random.choice(options[1:])
                        chosen.click()
                        logging.info(f"Selected native dropdown option '{chosen.text.strip()}'.")
                        break
                    except (Exception, StaleElementReferenceException) as err:
                        logging.warning(f"Failed selecting dropdown option: {str(err)}")
            return
        # 2. Custom dropdowns
        dropdowns = driver.find_elements(
            'xpath',
            '//div[contains(@class,"dropdown") or contains(@class,"select") or contains(@class,"menu")]'
        )
        safe_dropdowns = [dd for dd in dropdowns if dd.is_displayed()]
        if safe_dropdowns:
            dropdown = random.choice(safe_dropdowns)
            for attempt in range(3):
                try:
                    dropdown.click()
                    time.sleep(0.2)
                    options = dropdown.find_elements('xpath', './/li[not(contains(@class, "disabled"))]')
                    if options:
                        option = random.choice(options)
                        option.click()
                        logging.info(f"Selected custom dropdown option '{option.text.strip()}'.")
                    break
                except (Exception, StaleElementReferenceException) as err:
                    logging.warning(f"Failed interacting with custom dropdown: {str(err)}")

    def _random_toggle(self) -> None:
        """
        Click random toggle elements if present.
        Targets any element with a class containing 'toggle'.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver

        toggles = driver.find_elements('xpath', '//*[contains(@class,"toggle")]')
        safe_toggles = [t for t in toggles if t.is_displayed() and t.is_enabled()]

        if safe_toggles:
            toggle = random.choice(safe_toggles)
            try:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", toggle)
                time.sleep(0.1)
                toggle.click()
                logging.info(f"Clicked a toggle element with classes: '{toggle.get_attribute('class')}'.")
            except (Exception, StaleElementReferenceException) as err:
                logging.warning(f"Failed clicking toggle: {str(err)}")
        else:
            logging.info("No toggle elements found.")

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
            '//input[@type="text" or @type="email" or @type="search" or @type="password" or @type="tel" or @type="number" or @type="url"] | //textarea'
        )
        safe_inputs = [
            el for el in inputs
            if el.is_displayed() and el.is_enabled() and not el.get_attribute('readonly')
        ]
        if safe_inputs:
            element = random.choice(safe_inputs)
            input_type = element.get_attribute('type') or 'text'
            random_text_length = random.randint(5, 15)
            if input_type in ['number', 'tel']:
                random_text = ''.join(random.choices('0123456789', k=random_text_length))
            else:
                # include special characters
                special_chars = '!@#$%^&*()_+-=[]{}|;:,.<>?/~'
                random_text = ''.join(random.choices(
                    'abcdefghijklmnopqrstuvwxyz0123456789' + special_chars,
                    k=random_text_length
                ))
            try:
                for attempt in range(2):
                    element.clear()
                    element.send_keys(random_text)
                    logging.info(f"Typed '{random_text}' into input field of type '{input_type}'.")
                    break
            except (Exception, StaleElementReferenceException) as err:
                logging.warning(f"Failed typing into element: {str(err)}")
        else:
            logging.info("No input fields found for typing.")

    def _is_dangerous_element(self, element) -> bool:
        """
        Detect if element is potentially destructive.
        \nMatches keywords like delete, logout, withdraw, cancel, etc.
        \nAvoids accidental destructive actions during monkey test.
        """
        keywords = [
            'delete', 'remove', 'logout', 'sign out', 
            'withdraw', 'transfer', 'pay', 'submit payment',
            'close account', 'cancel', 'sign-out'
        ]
        try:
            text = element.text.lower() if element.text else ''
            eid = element.get_attribute('id').lower() if element.get_attribute('id') else ''
            eclass = element.get_attribute('class').lower() if element.get_attribute('class') else ''
            combined = f"{text} {eid} {eclass}"
            return any(kw in combined for kw in keywords)
        except Exception:
            return False

    @keyword
    def run_monkey_test_with_monitoring(self, duration_seconds: int = 60, actions_per_second: int = 2) -> None:
        """
        Run monkey testing with JavaScript error monitoring.
        \nInjects error listener into browser to capture runtime errors.
        \nAfter test run, collected errors are checked.
        \nFails with screenshot if errors were found.
        """
        selenium = self._get_selenium_library()
        driver = selenium.driver

        driver.execute_script("""
            window.monkeyTestErrors = [];
            window.addEventListener('error', function(e) {
                window.monkeyTestErrors.push(e.message);
            });
        """)
        self.run_monkey_test(duration_seconds, actions_per_second)
        js_errors = driver.execute_script("return window.monkeyTestErrors || []")
        if js_errors:
            logging.info(f"JavaScript errors found: {js_errors}")
            selenium.capture_page_screenshot()
            raise AssertionError(f"Monkey test found {len(js_errors)} JavaScript errors: {js_errors}")
