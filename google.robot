*** Settings ***
Documentation     Simple Google Search Test Case
Library           SeleniumLibrary

*** Variables ***
${BROWSER}        Chrome
${URL}            https://www.google.com
${SEARCH_BOX}     name:q
${SEARCH_BUTTON}  name:btnK
@{KEYWORDS}       Robot Framework    SeleniumLibrary    OpenAI    GPT-4    Automation Testing


*** Test Cases ***
Search Multiple Keywords On Google
    Open Browser    ${URL}    ${BROWSER}
    Maximize Browser Window
    Scroll Element Into View    //button[@id='L2AGLb']
    Run Keyword And Ignore Error    Click Element    //button[@id='L2AGLb']
    FOR    ${KEYWORD}    IN    @{KEYWORDS}
        Input Text    ${SEARCH_BOX}    ${KEYWORD}
        Click Element    ${SEARCH_BUTTON}
        Wait Until Page Contains    ${KEYWORD}
        Go To    ${URL}
    END
    Close Browser
