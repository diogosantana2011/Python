*** Settings ***
Library    RequestsLibrary
Library    Parallel

*** Keywords ***
Send Concurrent Requests
    &{data}=    Create Dictionary    foo=bar
    ${url}=  https://example.com/api
    ${result}=    Parallel Execute    2
    ...    POST    ${url}    json=${data}

    Log    ${result}
