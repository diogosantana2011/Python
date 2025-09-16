import os
from robot.api.deco import keyword
from selenium import webdriver
from browsermobproxy import Server
import logging


class SeleniumHTTPInterceptor:
    """
    Robot Framework library to intercept HTTP requests in Selenium tests
    using BrowserMob Proxy.
    \nReference: Github - [BrowserMob Proxy](https://github.com/lightbody/browsermob-proxy/releases)

    This library provides comprehensive HTTP traffic capture and analysis capabilities
    for automated testing. It captures both request payloads and response bodies,
    allowing detailed validation of API interactions during browser-based tests.

    Features:
    - Capture HTTP/HTTPS requests and responses during Selenium tests
    - Extract request payloads (JSON, form data, query parameters)
    - Extract response bodies with automatic JSON parsing
    - Filter captured traffic by URL patterns, exact matches, or substrings
    - Support for both proxy-based capture and direct HTTP requests
    - Automatic content type detection and parsing

    Setup:
    1. Download BrowserMob Proxy from: https://github.com/lightbody/browsermob-proxy/releases
    2. Extract and note the path to the browsermob-proxy executable
    3. Set environment variable BROWSERMOB_PROXY_PATH:
       export BROWSERMOB_PROXY_PATH=/path/to/browsermob-proxy/bin/browsermob-proxy

    Basic Usage:
    1. Import this library in Robot Framework:
       `Library    project_lib/services/robot/SeleniumHTTPInterceptor.py`
    
    2. Start capturing with content enabled:
       `Start Capture    test_capture    capture_content=${True}`
    
    3. Perform browser actions that trigger HTTP requests
    
    4. Extract captured data:
       ```
       ${requests}=           Get Requests
       ${response_bodies}=    Get Response Bodies By Url Contains    /api/endpoint
       ${request_payloads}=   Get Request Payloads By Url Contains    /api/endpoint
       ${complete_data}=      Get Request And Response Data    url_contains=/api/endpoint
       ```
    
    5. Clean up:
       `Stop Browser`

    ### *Available Keywords*
    
    Browser Management:
    - Start Proxy Server
    - Start Browser With Proxy
    - Stop Browser
    
    Traffic Capture:
    - Start Capture
    - Get Requests
    
    Response Body Extraction:
    - Get Response Bodies
    - Get Response Bodies By Url Exact
    - Get Response Bodies By Url Contains
    - Get Response Bodies By Endpoint
    
    Request Payload Extraction:
    - Get Request Payloads
    - Get Request Payloads By Url Exact
    - Get Request Payloads By Url Contains
    - Get Request Payloads By Endpoint
    
    Combined Data:
    - Get Request And Response Data
    - Get Request And Response Data By Path Exact
    
    Direct HTTP Requests:
    - Fetch Response Body Directly

    ### *Example Robot Framework Test*
    \n*** Settings ***
    \n`Library    project_lib/services/robot/SeleniumHTTPInterceptor.py`
    
    \n*** Test Cases ***
    \nTest API Validation
        ##### Start capturing HTTP requests
        `Start Capture    test_capture    ${True}`
        
        ##### Extract API data
        `${login_data}=    Get Request And Response Data    url_contains=/api/login`
        
        ##### Validate request payload
        `Should Be Equal    ${login_data[0]['request']['json']['username']}    testuser`
        
        ##### Validate response
        `Should Be Equal    ${login_data[0]['response']['status']}    ${200}`
        `Should Be True     ${login_data[0]['response']['json']['success']}`
        
        ##### Clean up
        `Clean up`

    \n### *Troubleshooting*:
    - If proxy fails to start, ensure BROWSERMOB_PROXY_PATH is correct
    - If response bodies are empty, ensure capture_content=${True} is set
    - If Java errors occur, the library automatically handles Java 9+ compatibility
    - For HTTPS sites, the proxy automatically handles SSL certificate issues
    """
    ##########################
    # INITIALIZATION
    ##########################
    def __init__(self, log_directory=None):
        # Primary local path
        self.bmp_path = os.getenv("BROWSERMOB_PROXY_PATH")
        # Fallback path inside the pod/container
        pod_default_path = "/srv/browsermob/browsermob-proxy"

        if not self.bmp_path or not os.path.isfile(self.bmp_path):
            if os.path.isfile(pod_default_path):
                self.bmp_path = pod_default_path
                logging.info(f"Using BrowserMob Proxy from pod path: {self.bmp_path}")
            else:
                raise FileNotFoundError(
                    "BrowserMob Proxy binary not found. "
                    "Set BROWSERMOB_PROXY_PATH to the correct path or ensure it exists in the pod."
                )
        self.server = None
        self.proxy = None
        self.driver = None
        # Set up log directory
        if log_directory:
            self.log_directory = os.path.abspath(log_directory)
        else:
            self.log_directory = os.path.join(os.getcwd(), "logs", "browsermob")
        os.makedirs(self.log_directory, exist_ok=True)

    ##########################
    # BROWSER & PROXY CONTROL
    ##########################
    @keyword
    def start_proxy_server(self):
        """Start only the BrowserMob Proxy server and return proxy URL for use with SeleniumLibrary."""
        logging.info(f"Starting BrowserMob Proxy using binary: {self.bmp_path}")
        if not self.bmp_path or not os.path.isfile(self.bmp_path):
            raise FileNotFoundError(
                f"BrowserMob Proxy binary not found. "
                f"Set BROWSERMOB_PROXY_PATH to the correct path."
            )
        # Start BrowserMob Proxy server with Java module access fix
        # Set JAVA_OPTS environment variable for Java 9+ compatibility
        original_java_opts = os.environ.get('JAVA_OPTS', '')
        java_module_opens = [
            '--add-opens java.base/java.lang=ALL-UNNAMED',
            '--add-opens java.base/java.nio=ALL-UNNAMED',
            '--add-opens java.base/java.util=ALL-UNNAMED',
            '--add-opens java.base/sun.nio.ch=ALL-UNNAMED',
            '--add-opens java.base/java.lang.reflect=ALL-UNNAMED'
        ]
        os.environ['JAVA_OPTS'] = original_java_opts + ' ' + ' '.join(java_module_opens)
        try:
            # Save current directory
            original_cwd = os.getcwd()
            # Change to log directory so BMP creates logs there
            os.chdir(self.log_directory)
            try:
                # Configure server options
                server_options = {
                    "port": 9090,
                    "log_level": "INFO"
                }
                self.server = Server(self.bmp_path, options=server_options)
                self.server.start()
                self.proxy = self.server.create_proxy()
                logging.info(f"DEBUG: BrowserMob Proxy logs will be written to: {self.log_directory}")
            finally:
                # Restore original working directory
                os.chdir(original_cwd)
        finally:
            # Restore original JAVA_OPTS
            if original_java_opts:
                os.environ['JAVA_OPTS'] = original_java_opts
            else:
                os.environ.pop('JAVA_OPTS', None)
        if not self.proxy:
            raise RuntimeError("Failed to create proxy instance")
        proxy_url = self.proxy.proxy
        logging.info(f"DEBUG: Created proxy with URL: {proxy_url}")
        return proxy_url

    @keyword
    def start_browser_with_proxy(self, browser="chrome", headless=False, chrome_options=None):
        """Start Chrome routed through BrowserMob Proxy."""
        logging.info(f"Starting BrowserMob Proxy (for browser) using binary: {self.bmp_path}")
        if not self.bmp_path or not os.path.isfile(self.bmp_path):
            raise FileNotFoundError(
                f"BrowserMob Proxy binary not found. "
                f"Set BROWSERMOB_PROXY_PATH to the correct path."
            )
        # Start BrowserMob Proxy server with Java module access fix
        # Set JAVA_OPTS environment variable for Java 9+ compatibility
        original_java_opts = os.environ.get('JAVA_OPTS', '')
        java_module_opens = [
            '--add-opens java.base/java.lang=ALL-UNNAMED',
            '--add-opens java.base/java.nio=ALL-UNNAMED',
            '--add-opens java.base/java.util=ALL-UNNAMED',
            '--add-opens java.base/sun.nio.ch=ALL-UNNAMED',
            '--add-opens java.base/java.lang.reflect=ALL-UNNAMED'
        ]
        os.environ['JAVA_OPTS'] = original_java_opts + ' ' + ' '.join(java_module_opens)
        try:
            # Save current directory
            original_cwd = os.getcwd()
            # Change to log directory so BMP creates logs there
            os.chdir(self.log_directory)
            try:
                # Configure server options
                server_options = {
                    "port": 9090,
                    "log_level": "INFO"
                }
                self.server = Server(self.bmp_path, options=server_options)
                self.server.start()
                logging.info(f"DEBUG: BrowserMob Proxy logs will be written to: {self.log_directory}")
            finally:
                # Restore original working directory
                os.chdir(original_cwd)
        finally:
            # Restore original JAVA_OPTS
            if original_java_opts:
                os.environ['JAVA_OPTS'] = original_java_opts
            else:
                os.environ.pop('JAVA_OPTS', None)
        self.proxy = self.server.create_proxy()
        # Setup Chrome options
        if chrome_options is not None:
            options = chrome_options
        else:
            options = webdriver.ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument(f"--proxy-server={self.proxy.proxy}")
        if browser.lower() == "chrome":
            self.driver = webdriver.Chrome(options=options)
        else:
            raise ValueError(f"Browser '{browser}' not supported yet.")
        return self.driver

    @keyword
    def stop_browser(self):
        """Stop the Selenium browser and BrowserMob Proxy server."""
        if self.driver:
            self.driver.quit()
            self.driver = None
        if self.server:
            self.server.stop()
            self.server = None

    ##########################
    # TRAFFIC CAPTURE
    ##########################
    @keyword
    def start_capture(self, label="test_capture", capture_content=True, capture_headers=True, capture_binary_content=False):
        """
        \nStart capturing HTTP requests in the BrowserMob Proxy HAR.
        \n*Args*:
            -`label`: Label for the HAR capture
            -`capture_content`: Whether to capture response content (default: True)
            -`capture_headers`: Whether to capture headers (default: True) 
            -`capture_binary_content`: Whether to capture binary content (default: False)
        """
        if not self.proxy:
            raise RuntimeError("Proxy not initialized. Call Start Browser With Proxy first.")
        # Configure what to capture
        options = {}
        if capture_content:
            options['captureContent'] = True
        if capture_headers:
            options['captureHeaders'] = True
        if capture_binary_content:
            options['captureBinaryContent'] = True
        self.proxy.new_har(label, options)

    @keyword
    def get_requests(self):
        """Return all captured HTTP requests as a HAR dictionary."""
        if not self.proxy:
            raise RuntimeError("Proxy not initialized. Call Start Browser With Proxy first.")
        return self.proxy.har

    ##########################
    # RESPONSE EXTRACTION
    ##########################   
    @keyword
    def get_response_bodies(self, url_pattern=None, exact_match=False, url_contains=None):
        """
        Extract response bodies from captured requests.\n
        \n*Args*:\n
            \n-`url_pattern`: Optional regex pattern to filter URLs (default behavior)
            \n-`exact_match`: If True with url_pattern, requires exact URL match
            \n-`url_contains`: Simple substring match for URLs (alternative to regex)
        \n*Returns*:
            List of dictionaries with URL, status, and response body
        """
        import re
        import json
        import base64
        if not self.proxy:
            raise RuntimeError("Proxy not initialized. Call Start Browser With Proxy first.")
        har_data = self.proxy.har
        response_bodies = []
        for entry in har_data.get('log', {}).get('entries', []):
            url = entry['request']['url']
            # Filter by URL pattern/match if provided
            should_include = True
            if url_contains:
                # Simple substring match
                should_include = url_contains in url
            elif url_pattern:
                if exact_match:
                    # Exact match
                    should_include = url == url_pattern
                else:
                    # Regex pattern match (original behavior)
                    should_include = bool(re.search(url_pattern, url))
            if not should_include:
                continue
            response = entry['response']
            content = response.get('content', {})
            body_data = {
                'url': url,
                'method': entry['request']['method'],
                'status': response['status'],
                'mimeType': content.get('mimeType', ''),
                'size': content.get('size', 0),
                'body': None
            }
            # Extract body content if available
            if 'text' in content:
                body_text = content['text']
                encoding = content.get('encoding', '')
                if encoding == 'base64':
                    try:
                        body_data['body'] = base64.b64decode(body_text).decode('utf-8')
                    except Exception as e:
                        body_data['body'] = f"Error decoding base64: {e}"
                else:
                    body_data['body'] = body_text
                # Try to parse JSON if content type suggests it
                if 'application/json' in body_data['mimeType'] and body_data['body']:
                    try:
                        body_data['json'] = json.loads(body_data['body'])
                    except json.JSONDecodeError:
                        pass
            response_bodies.append(body_data)
        return response_bodies

    @keyword
    def get_response_bodies_by_url_exact(self, exact_url):
        """Get response bodies for requests matching the exact URL."""
        return self.get_response_bodies(url_pattern=exact_url, exact_match=True)
    
    @keyword
    def get_response_bodies_by_url_contains(self, url_substring):
        """Get response bodies for requests where URL contains the substring."""
        return self.get_response_bodies(url_contains=url_substring)
    
    @keyword
    def get_response_bodies_by_endpoint(self, endpoint_path):
        """Get response bodies for requests ending with the specified endpoint path.
        
        For example: endpoint_path='/validatePassword' will match any URL ending with that path
        """
        import re
        return self.get_response_bodies(url_pattern=f"{re.escape(endpoint_path)}$")

    ##########################
    # REQUEST EXTRACTION
    ##########################
    @keyword
    def get_request_payloads(self, url_pattern=None, exact_match=False, url_contains=None):
        """
        Extract request payloads/bodies from captured requests.\n
        \n*Args*:\n
            \n-`url_pattern`: Optional regex pattern to filter URLs
            \n-`exact_match`: If True with url_pattern, requires exact URL match
            \n-`url_contains`: Simple substring match for URLs
        \n*Returns*:
            List of dictionaries with URL, method, headers, and request payload
        """
        import re
        import json
        from urllib.parse import parse_qs, unquote_plus
        if not self.proxy:
            raise RuntimeError("Proxy not initialized. Call Start Browser With Proxy first.")
        har_data = self.proxy.har
        request_payloads = []
        for entry in har_data.get('log', {}).get('entries', []):
            url = entry['request']['url']
            # Filter by URL pattern/match if provided
            should_include = True
            if url_contains:
                # Simple substring match
                should_include = url_contains in url
            elif url_pattern:
                if exact_match:
                    # Exact match
                    should_include = url == url_pattern
                else:
                    # Regex pattern match
                    should_include = bool(re.search(url_pattern, url))
            if not should_include:
                continue
            request = entry['request']
            # Extract headers as dict
            headers = {}
            for header in request.get('headers', []):
                headers[header['name']] = header['value']
            # Extract query parameters
            query_params = {}
            for param in request.get('queryString', []):
                query_params[param['name']] = param['value']
            payload_data = {
                'url': url,
                'method': request['method'],
                'headers': headers,
                'query_params': query_params,
                'content_type': headers.get('Content-Type', ''),
                'payload': None,
                'payload_size': request.get('bodySize', 0)
            }
            # Extract request payload if available
            post_data = request.get('postData', {})
            if post_data:
                mime_type = post_data.get('mimeType', '')
                payload_data['content_type'] = mime_type
                # Handle different payload types
                if 'text' in post_data:
                    payload_text = post_data['text']
                    payload_data['payload'] = payload_text
                    # Try to parse JSON if content type suggests it
                    if 'application/json' in mime_type and payload_text:
                        try:
                            payload_data['json'] = json.loads(payload_text)
                        except json.JSONDecodeError:
                            pass
                    # Try to parse form data
                    elif 'application/x-www-form-urlencoded' in mime_type and payload_text:
                        try:
                            payload_data['form_data'] = parse_qs(payload_text, keep_blank_values=True)
                        except Exception:
                            pass
                # Handle form parameters (alternative format)
                elif 'params' in post_data:
                    form_params = {}
                    for param in post_data['params']:
                        form_params[param['name']] = param['value']
                    payload_data['form_data'] = form_params
                    payload_data['payload'] = '&'.join([f"{k}={v}" for k, v in form_params.items()])
            request_payloads.append(payload_data)
        return request_payloads

    @keyword
    def get_request_payloads_by_url_exact(self, exact_url):
        """Get request payloads for requests matching the exact URL."""
        return self.get_request_payloads(url_pattern=exact_url, exact_match=True)

    @keyword
    def get_request_payloads_by_url_contains(self, url_substring):
        """Get request payloads for requests where URL contains the substring."""
        return self.get_request_payloads(url_contains=url_substring)

    @keyword
    def get_request_payloads_by_endpoint(self, endpoint_path):
        """Get request payloads for requests ending with the specified endpoint path."""
        import re
        return self.get_request_payloads(url_pattern=f"{re.escape(endpoint_path)}$")

    ##########################
    # COMBINED DATA
    ##########################
    @keyword
    def get_request_and_response_data(self, url_pattern=None, exact_match=False, url_contains=None):
        """
        Get both request payloads and response bodies for matching URLs.\n
        \n*Args*:\n
            \n-`url_pattern`: Optional regex pattern to filter URLs (default behavior)
            \n-`exact_match`: If True with url_pattern, requires exact URL match
            \n-`url_contains`: Simple substring match for URLs (alternative to regex)
        \n*Returns*:
            List of dictionaries with both request and response data
        \n*Usage Examples*:
            \n#### Regex match (default) - matches URLs containing the pattern
            \n`${data}=    Get Request And Response Data    url_pattern=/registration`
            \n#### Exact URL match
            \n`${data}=    Get Request And Response Data    url_pattern=https://example.com/registration    exact_match=${True}`
            \n#### Simple substring match  
            \n`${data}=    Get Request And Response Data    url_contains=/registration`
        """
        request_payloads = self.get_request_payloads(url_pattern, exact_match, url_contains)
        response_bodies = self.get_response_bodies(url_pattern, exact_match, url_contains)
        # Merge request and response data by URL and timestamp
        combined_data = []
        for req in request_payloads:
            # Find matching response
            matching_response = None
            for resp in response_bodies:
                if resp['url'] == req['url'] and resp['method'] == req['method']:
                    matching_response = resp
                    break
            combined_entry = {
                'url': req['url'],
                'method': req['method'],
                'request': req,
                'response': matching_response
            }
            combined_data.append(combined_entry)
        return combined_data
    
    @keyword
    def get_request_and_response_data_by_path_exact(self, exact_path):
        """
        Get request and response data for URLs ending exactly with the specified path.
        \nThis matches URLs that end with exactly the path, not followed by additional path segments.
        \nFor example: exact_path='/ams/service/public/registration' will match:
        \n- https://domain.com/ams/service/public/registration
        \n- https://domain.com/ams/service/public/registration?param=value
        \nBut NOT:
        \n- https://domain.com/ams/service/public/registration/validatePassword
        \n*Usage Examples*:
        \n`${register_request_bodies}=    Get Request And Response Data By Path Exact    /ams/service/public/registration`
        \n`Log    ${register_request_bodies[0]['request']['json']}`
        \n`Log    ${register_request_bodies[0]['response']['json']}`
        \nWill return:
        \n`{'username': 'PlayerKqfI3', 'password': 'Password1!', 'email': '3etqa@ns90.ie', 'firstName': 'First8658', 'lastName': 'Last9223', 'dateOfBirth': '2004-04-08', 'contactNumber': '18094713794', 'addressLine1': 'test', 'addressLine2': None, 'city': '', 'state': 'test', 'postCode': 'test', 'country': '95', 'currency': 1, 'gRecaptchaResponse': '', 'heardAboutUs': 'Gx4h%^s456', 'consentToMarketing': True, 'promoCode': '', 'language': 'en', 'affiliateType': ''}`
        """
        import re
        # Create a regex that matches the exact path followed by end of path or query params
        escaped_path = re.escape(exact_path)
        pattern = f"{escaped_path}(?:\\?.*)?$"  # Match path followed by optional query params and end of string
        return self.get_request_and_response_data(url_pattern=pattern)

    ##########################
    # DIRECT HTTP REQUESTS
    ##########################
    @keyword
    def fetch_response_body_directly(self, url, method="GET", headers=None, cookies=None, data=None):
        """
        Make a direct HTTP request to fetch response body. \nThis is useful when HAR capture doesn't include response bodies.
        \n*Args*:
            \n-`url`: The URL to request
            \n-`method`: HTTP method (default: GET)
            \n-`headers`: Optional headers dictionary
            \n-`cookies`: Optional cookies dictionary  
            \n-`data`: Optional request body data
        \n*Returns*:
            Dictionary with status, headers, and response body
        """
        import requests
        import json
        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=headers or {},
                cookies=cookies or {},
                data=data,
                timeout=30
            )
            result = {
                'url': url,
                'status': response.status_code,
                'headers': dict(response.headers),
                'body': response.text,
                'size': len(response.content)
            }
            # Try to parse JSON if content type suggests it
            content_type = response.headers.get('content-type', '')
            if 'application/json' in content_type:
                try:
                    result['json'] = response.json()
                except json.JSONDecodeError:
                    pass
            return result
        except Exception as e:
            return {
                'url': url,
                'error': str(e),
                'status': None,
                'body': None
            }

    #################
    # LOGS HELPERS  #
    #################
    @keyword
    def set_log_directory(self, log_directory):
        """
        Set the directory where BrowserMob Proxy logs will be written.
        \n*Args*:
            `log_directory`: Absolute or relative path to the log directory
        """
        self.log_directory = os.path.abspath(log_directory)
        os.makedirs(self.log_directory, exist_ok=True)
        logging.info(f"DEBUG: Log directory set to: {self.log_directory}")
    
    @keyword
    def get_log_directory(self):
        """Get the current log directory path."""
        return self.log_directory
    
    @keyword
    def clean_log_directory(self):
        """Clean (remove all files from) the log directory."""
        import glob
        log_files = glob.glob(os.path.join(self.log_directory, "*.log"))
        for log_file in log_files:
            try:
                os.remove(log_file)
                logging.info(f"DEBUG: Removed log file: {log_file}")
            except Exception as e:
                logging.info(f"WARNING: Could not remove log file {log_file}: {e}")
    
    @keyword
    def list_log_files(self):
        """List all log files in the log directory."""
        import glob
        log_files = glob.glob(os.path.join(self.log_directory, "*.log"))
        if log_files:
            logging.info(f"DEBUG: Log files found in {self.log_directory}:")
            for log_file in log_files:
                file_size = os.path.getsize(log_file)
                logging.info(f"  - {os.path.basename(log_file)} ({file_size} bytes)")
        else:
            logging.info(f"DEBUG: No log files found in {self.log_directory}")
        return log_files
