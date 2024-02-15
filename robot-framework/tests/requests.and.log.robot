*** Settings ***
Library    Collections
Library    DateTime
Library    RequestsLibrary
Suite Setup    Create Session  jsonplaceholder  https://jsonplaceholder.typicode.com

*** Variables ***
${BROWSER}    chromium
${HEADLESS}    true
${name}=    Diogo Santana
${msg}=    This message will be logged.

*** Test Cases ***
Log a message to the console
    Log    You can combine variables and strings like this: ${msg}
    Log    This message was logged by: ${name}

Tests DateTime
    ${date_now}=    Get Current Date
    Log    Current time is: ${date_now}

Makes a request via HTTP GET
    ${response}=    GET    https://google.com    expected_status=200

Makes a request with Query string parameters
    ${response}=    GET  https://google.com/search?  params=query=ciao  expected_status=200
    Should Be Equal As Strings          ${response.reason}  OK

Quick Get A JSON Body Test
    ${resp_json}=     GET On Session  jsonplaceholder  /posts/1
    Dictionary Should Contain Value     ${resp_json.json()}  sunt aut facere repellat provident occaecati excepturi optio reprehenderit
    Log    ${resp_json.json()}