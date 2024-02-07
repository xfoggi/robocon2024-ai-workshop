*** Settings ***
Documentation     A test suite with a single test for demonstration purposes.

*** Test Cases ***
Simple test
    [Tags]    example
    [Documentation]    This is a test case with a single step.
    Log To Console    Hello, world!

Failin test
    [Tags]    example
    [Documentation]    This is a test case with a single step.
    Log To Console    Hello, world!
    Fail    This is a failing test