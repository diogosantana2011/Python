CHROME Setup
    [Arguments]    ${WEB_SERVER}
    # Connect to the running BrowserMob Proxy service
    ${proxy_url}=    Interceptor.Connect To Proxy Client
    Log    Proxy URL received: ${proxy_url}
    # Create Chrome options for headless mode and other settings
    ${chrome_options}=    Evaluate    sys.modules['selenium.webdriver'].ChromeOptions()    sys, selenium.webdriver
    Call Method    ${chrome_options}    add_argument    --no-sandbox
    Call Method    ${chrome_options}    add_argument    --headless
    Call Method    ${chrome_options}    add_argument    --disable-setuid-sandbox
    Call Method    ${chrome_options}    add_argument    --disable-dev-shm-usage
    Call Method    ${chrome_options}    add_argument    --disable-gpu
    Call Method    ${chrome_options}    add_argument    --disable-extensions
    # SSL certificate handling for proxy
    Call Method    ${chrome_options}    add_argument    --ignore-ssl-errors
    Call Method    ${chrome_options}    add_argument    --ignore-certificate-errors
    Call Method    ${chrome_options}    add_argument    --allow-running-insecure-content
    Call Method    ${chrome_options}    add_argument    --disable-web-security
    # Add proxy settings to Chrome options
    ${proxy_arg}=    Set Variable    --proxy-server=${proxy_url}
    Log    Proxy argument: ${proxy_arg}
    Call Method    ${chrome_options}    add_argument    ${proxy_arg}
    # Open browser using SeleniumLibrary routed through proxy
    Open Browser    ${WEB_SERVER}    browser=chrome    options=${chrome_options}
    Set Selenium Implicit Wait    30s
