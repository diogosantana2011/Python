*** Settings ***
Library    RequestsLibrary
Library    Collections
Suite Setup    Create Session    httpBin   https://httpbin.org

*** Variables ***
${url}    https://httpbin.org

*** Test Cases ***
Makes a HTTP GET request
    ${response}=     GET     ${url}    expected_status=200

Asserts on response body
    ${response}=    GET On Session    httpBin     /get    params=randomParams=DiogoRequest
    Dictionary Should Contain Key    ${response.json()['args']}    key=randomParams
    Dictionary Should Contain Item    ${response.json()['args']}    key=randomParams    value=DiogoRequest
    Log    ${response.json()['args']['randomParams']}