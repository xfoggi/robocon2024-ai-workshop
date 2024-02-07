*** Settings ***
Library             SeleniumLibrary

Suite Teardown      Close All Browsers


*** Variables ***
${BASE_URL}         https://stage.artima.ai/Identity/Account/Register
${EMAIL_INPUT}      id:Input_Email2
${SUBMIT_BUTTON}    css:button[type='submit']
${VALID_EMAIL}      user@example.com
${INVALID_EMAIL}    userexample.com


*** Test Cases ***
Valid Email Should Be Accepted
    Open Browser    ${BASE_URL}    browser=Chrome    executable_path=chromedriver
    Input Text    ${EMAIL_INPUT}    ${VALID_EMAIL}

    Click Element    ${SUBMIT_BUTTON}
    Email Submission Should Be Successful


*** Keywords ***
Email Submission Should Be Successful
    Wait For Condition    return document.readyState == 'complete'
    # Add any additional checks for successful submission, such as URL change, message appearance, etc.

Email Submission Should Fail
    Wait For Condition    return document.readyState == 'complete'
    # Add checks for specific error message related to email validation.
