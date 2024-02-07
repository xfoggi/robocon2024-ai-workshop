# Robot Framework Listener with OpenAI and JIRA Integration

## Description

This project enhances Robot Framework automated testing with AI-driven insights using OpenAI's ChatGPT and seamless test management through JIRA integration. It includes custom Robot Framework listeners and test suites, demonstrating advanced automation strategies.

## Features

- **AI-Driven Insights**: Utilize OpenAI's ChatGPT for dynamic question-answering during test execution.
- **JIRA Integration**: Automatically create and manage issues based on test results, facilitating better test management.
- **Customizable Test Suites**: Includes examples of automated web testing scripts for Google search and email registration validation.

## Requirements

- Python 3.x
- Robot Framework
- SeleniumLibrary for Robot Framework
- OpenAI API key
- JIRA account with API access

## Installation

1. Clone this repository.
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up environment variables for OpenAI API key and JIRA credentials.

## Usage
To run the test suites with the RobotListenerV2 enabled:
```bash
robot --listener RobotListenerV2.py test_suite_name.robot
```

Replace test_suite_name.robot with the path to the desired Robot Framework test suite file.

## License
This project is open-sourced under the MIT License.
