import os
import logging
import requests
import re
from robot.api.deco import keyword
from browsermobproxy import Client

class SeleniumHTTPInterceptor:
    """
    Robot Framework library to intercept HTTP requests in Selenium tests
    using BrowserMob Proxy (service-based).

    #### Reference: 
        - Github - [BrowserMob Proxy](https://github.com/lightbody/browsermob-proxy/releases)
    #### Reference: 
        - ReadTheDocs - [BrowserMob Docs](https://browsermob-proxy-py.readthedocs.io/en/stable/)

    This library provides comprehensive HTTP traffic capture and analysis capabilities
    for automated testing. It captures both request payloads and response bodies,
    allowing detailed validation of API interactions during browser-based tests.

    Features:
    - Capture HTTP/HTTPS requests and responses during Selenium tests
    - Extract request payloads (JSON, form data, query parameters)
    - Extract response bodies with automatic JSON parsing
    - Filter captured traffic by URL patterns, exact matches, or substrings
    - Support for both proxy-based capture and direct HTTP requests
    - Connect to a running BrowserMob Proxy service (no local JAR required)
    - Automatic content type detection and parsing

    Setup:
    1. Deploy BrowserMob Proxy as a service or use an existing running instance.
    2. Set environment variable BROWSERMOB_PROXY_URL to the service address:
    export BROWSERMOB_PROXY_URL=http://localhost:9090
    - Default is http://localhost:9090 if not overridden.
    3. Ensure the Selenium WebDriver can connect to the service host and port.

    Basic Usage:
    1. Import this library in Robot Framework:
    `Library project_lib/services/robot/SeleniumHTTPInterceptor.py`

    2. Start capturing HTTP requests:
    `Start Capture test_capture capture_content=${True}`

    3. Perform browser actions that trigger HTTP requests.
    4. Extract captured data:
    ```
    ${requests}= Get Requests
    ${response_bodies}= Get Response Bodies By Url Contains /api/endpoint
    ${request_payloads}= Get Request Payloads By Url Contains /api/endpoint
    ${complete_data}= Get Request And Response Data url_contains=/api/endpoint
    ```

    5. Clean up:
    `Stop Browser`

    ### *Available Keywords*

    Browser Management:
    - Start Proxy Client
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

    *** Settings ***
    `Library project_lib/services/robot/SeleniumHTTPInterceptor.py`

    *** Test Cases ***
    Test API Validation
    ##### Start capturing HTTP requests
    `Start Capture test_capture ${True}`
    ##### Extract API data
    `${login_data}= Get Request And Response Data url_contains=/api/login`
    ##### Validate request payload
    `Should Be Equal ${login_data[0]['request']['json']['username']} testuser`
    ##### Validate response
    `Should Be Equal ${login_data[0]['response']['status']} ${200}`
    `Should Be True ${login_data[0]['response']['json']['success']}`
    ##### Clean up
    `Clean up`

    ### *Troubleshooting*:
    - Ensure BROWSERMOB_PROXY_URL points to a reachable service (host:port)
    - If response bodies are empty, ensure capture_content=${True} is set
    - HTTPS requests automatically handled by the proxy's SSL certificates
    - No local JAR or binary required when using a service
    """
    ##########################
    # INITIALIZATION
    ##########################
    def __init__(self, log_directory=None):
        """
        Initialize the SeleniumHTTPInterceptor library.

        Reads the BrowserMob Proxy service URL from the environment variable
        `BROWSERMOB_PROXY_URL` (defaults to `http://localhost:9090`).
        Also prepares a directory for log storage.

        \n*Args*:
        \n`log_directory` (str, optional): Path for log storage. Defaults to
        `<cwd>/logs/browsermob` if not provided.
        """
        # Get BrowserMob Proxy URL from environment
        self.bmp_url = os.getenv("BROWSERMOB_PROXY_URL", "http://localhost:9090")
        # Validate URL format
        if not self.bmp_url.startswith(('http://', 'https://')):
            self.bmp_url = f"http://{self.bmp_url}"
        logging.info(f"Using BrowserMob Proxy service URL: {self.bmp_url}")
        # Initialize proxy and driver as None
        self.proxy = None
        self.driver = None
        # Set up log directory
        self.log_directory = (
            os.path.abspath(log_directory)
            if log_directory
            else os.path.join(os.getcwd(), "logs", "browsermob")
        )        
        try:
            os.makedirs(self.log_directory, exist_ok=True)
            logging.info(f"Log directory set to: {self.log_directory}")
        except OSError as e:
            logging.warning(f"Could not create log directory {self.log_directory}: {e}")
            # Fall back to current directory
            self.log_directory = os.getcwd()
            logging.info(f"Using fallback log directory: {self.log_directory}")

    ##########################
    # BROWSER & PROXY CONTROL
    ##########################
    @keyword
    def connect_to_proxy_client_no_chrome_proxy(self):
        """
        Connect to the BrowserMob Proxy service without routing Chrome through it.

        Useful if you only need to capture background traffic and not route
        Selenium's Chrome traffic.

        \n*Returns*:
        str: Always returns "no_proxy".

        \n*Raises*:
        RuntimeError: If the proxy service cannot be reached.
        """
        bmp_url_clean = re.sub(r'^https?://', '', self.bmp_url)
        logging.info(f"Connecting to BrowserMob Proxy service at: {bmp_url_clean}")
        try:
            # Test connection to BrowserMob Proxy service first
            test_response = requests.get(f"{self.bmp_url}/proxy", timeout=10)
            test_response.raise_for_status()
            logging.info("Successfully connected to BrowserMob Proxy service")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to BrowserMob Proxy at {self.bmp_url}: {e}")
        # Initialize the client
        self.proxy = Client(bmp_url_clean)
        # Create a proxy instance for HAR capture
        if not self.proxy.proxy_ports:
            response = requests.post(f"{self.bmp_url}/proxy")
            response.raise_for_status()
            self.proxy = Client(bmp_url_clean)
        logging.info("Proxy client ready for HAR capture (Chrome will not use proxy)")
        return "no_proxy"

    @keyword
    def connect_to_proxy_client(self):
        """
        Connect to the BrowserMob Proxy service and create a client.
        If no existing proxy instances are available, a new one will be created.

        \n*Returns*:
        str: Proxy URL in `host:port` format for Chrome.

        \n*Raises*:
        RuntimeError: If the service cannot be reached or client init fails.
        """
        bmp_url_clean = re.sub(r'^https?://', '', self.bmp_url)
        logging.info(f"Connecting to BrowserMob Proxy service at: {bmp_url_clean}")
        try:
            # Test connection to BrowserMob Proxy service first
            test_response = requests.get(f"{self.bmp_url}/proxy", timeout=10)
            test_response.raise_for_status()
            logging.info("Successfully connected to BrowserMob Proxy service")
            logging.info(f"Available proxies: {test_response.json()}")
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to connect to BrowserMob Proxy at {self.bmp_url}: {e}")
        # Initialize the client
        self.proxy = Client(bmp_url_clean)
        try:
            # Check if there are existing proxies
            existing_proxies = self.proxy.proxy_ports
            logging.info(f"Found {len(existing_proxies)} existing proxies: {existing_proxies}")
            if not existing_proxies:
                logging.info("No existing proxies found. Creating a new proxy...")
                response = requests.post(f"{self.bmp_url}/proxy")
                response.raise_for_status()
                proxy_data = response.json()
                logging.info(f"Created new proxy response: {proxy_data}")
                # Refresh the client to get the new proxy
                self.proxy = Client(bmp_url_clean)
                existing_proxies = self.proxy.proxy_ports
                logging.info(f"After refresh, proxy ports: {existing_proxies}")
            # Get the proxy port and construct the URL
            if existing_proxies:
                # Use first available proxy
                proxy_port = existing_proxies[0]
                # IMPORTANT: Use the same host as the BMP service, not localhost
                # This should be 10.88.55.55
                proxy_host = bmp_url_clean.split(':')[0]
                proxy_url = f"{proxy_host}:{proxy_port}"
                logging.info(f"Final proxy URL for Chrome: {proxy_url}")
                # Test the proxy connection
                try:
                    import socket
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(5)
                    result = sock.connect_ex((proxy_host, int(proxy_port)))
                    sock.close()
                    if result == 0:
                        logging.info(f"Proxy connection test PASSED for {proxy_url}")
                    else:
                        logging.error(f"Proxy connection test FAILED for {proxy_url} - port likely not exposed")
                except Exception as e:
                    logging.error(f"Proxy connection test error: {e}")
                return proxy_url
            else:
                raise RuntimeError("No proxy ports available after initialization")
        except Exception as e:
            raise RuntimeError(f"Failed to initialize proxy client: {e}")

    @keyword
    def get_chrome_proxy_url(self):
        """
        Get the proxy URL in Chrome-compatible format (`host:port`).
        \nMust be called after `connect_to_proxy_client`.

        \n*Returns*:
        str: Proxy URL for Chrome.

        \n*Raises*:
        RuntimeError: If no proxy client has been initialized.
        """
        if not self.proxy or not self.proxy.proxy_ports:
            raise RuntimeError("No proxy available. Call connect_to_proxy_client first.")
        proxy_port = self.proxy.proxy_ports[0]
        bmp_url_clean = re.sub(r'^https?://', '', self.bmp_url)
        proxy_host = bmp_url_clean.split(':')[0]
        proxy_url = f"{proxy_host}:{proxy_port}"
        logging.info(f"Chrome proxy URL: {proxy_url}")
        return proxy_url

    @keyword
    def stop_browser(self):
        """
        Stop the Selenium browser and close the BrowserMob Proxy client.
        \nCloses WebDriver if running, and shuts down the proxy session.
        """
        if self.driver:
            self.driver.quit()
            self.driver = None
        if self.proxy:
            self.proxy.close()
            self.proxy = None

    ##########################
    # TRAFFIC CAPTURE
    ##########################
    @keyword
    def start_capture(self, label="test_capture", capture_content=True, capture_headers=True, capture_binary_content=False):
        """
        Start capturing HTTP requests into a HAR file.

        \n*Args*:
        `label` (str): Label for the HAR capture.
        `capture_content` (bool): Capture response bodies (default: True).
        `capture_headers` (bool): Capture headers (default: True).
        `capture_binary_content` (bool): Capture binary content (default: False).

        \n*Raises*:
        RuntimeError: If proxy client is not initialized.
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
        """
        Retrieve all captured HTTP requests as HAR data.
        \n*Returns*:
        dict: HAR-formatted dictionary of captured requests.

        \n*Raises*:
        RuntimeError: If proxy client is not initialized.
        """
        if not self.proxy:
            raise RuntimeError("Proxy not initialized. Call Start Browser With Proxy first.")
        return self.proxy.har

    ##########################
    # RESPONSE EXTRACTION
    ##########################   
    @keyword
    def get_response_bodies(self, url_pattern=None, exact_match=False, url_contains=None):
        """
        Extract response bodies from captured requests.
        \n*Args*:
        - `url_pattern` (str, optional): Regex to filter URLs.
        - `exact_match` (bool): Require exact match if True.
        - `url_contains` (str, optional): Simple substring filter.

        \n*Returns*:
        list[dict]: Response metadata and bodies.

        \n*Raises*:
        RuntimeError: If proxy client is not initialized.
        """
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
        return self.get_response_bodies(url_pattern=f"{re.escape(endpoint_path)}$")

    ##########################
    # REQUEST EXTRACTION
    ##########################
    @keyword
    def get_request_payloads(self, url_pattern=None, exact_match=False, url_contains=None):
        """
        Extract request payloads from captured requests.

        \n*Args*:
        \n- `url_pattern` (str, optional): Regex to filter URLs.
        \n- `exact_match` (bool): Require exact match if True.
        \n- `url_contains` (str, optional): Simple substring filter.

        \n*Returns*:
        - list[dict]: Request metadata and payloads.
        \n*Raises*:
        - RuntimeError: If proxy client is not initialized.
        """
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
