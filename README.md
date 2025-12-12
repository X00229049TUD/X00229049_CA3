# DevOps CA3 – Python Calculator (X00229049)

## Overview

This repository extends the CA2 Python calculator into a complete CI/CD implementation using GitHub and Azure DevOps. The focus is on robust automated delivery across environments, including build automation, code quality checks, security controls, performance testing, and Selenium-based user acceptance testing (UAT).

## Technologies Used

- Python 3.11
- Flask (web UI + API endpoint)
- **Testing**: pytest, pytest-cov
- **Static analysis**: pylint
- **CI/CD**: Azure DevOps YAML pipeline
- **Performance testing**: Apache JMeter
- **UAT**: Behave (BDD) + Selenium (headless Chrome)
- **Source control**: Git + GitHub (private repo)

## Local Development Setup 

### Requirements

- Python 3.x (recommended: 3.11)
- Git
- Optional: Python virtual environment

### Setup Steps

```bash
git clone https://github.com/X00229049TUD/X00229049_CA3.git
cd X00229049_CA3

# (Optional) Create virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
## Application Features

- Calculator operations: *add, sub, mul, div, pow, min, max*
- Web UI for interactive calculation
- API endpoint for automated checks (used in deployment smoke tests)

Division by zero raises a ValueError.

The project follows a simple structure:
```
calculator/
    __init__.py
    core.py
tests/
    test_core.py
    test_multiply_divide.py
    test_power.py
    test_min_max.py
main.py
azure-pipelines.yml
README.md
requirements.txt
```

## CI Pipeline Implementation
The Azure DevOps pipeline is implemented in `azure-pipelines.yml` and runs on `ubuntu-latest`.

### Triggers:

- CI trigger on pushes to main
- PR validation on PRs targeting main

### Stages (high-level):

1. BuildAndTest
    - Install dependencies
    - Run pylint
    - Run pytest with coverage gate (>=80%)
    - Publish code coverage
    - Publish build artifact (drop)
2. Deploy_Test
    - Deploy (simulated) using artifact
    - Smoke test the running app via curl

3. PerformanceTests
    - Run JMeter test plan against the app
    - Publish JMeter HTML report + raw results as pipeline artifacts

4. UATTests
    - Run Behave + Selenium headless UI tests
    - Publish UAT evidence artifact (Behave output + screenshots on failure)

## Branch Policies and Protection
Branch protection is configured on GitHub (not Azure Repos), following CA
requirements.
### main branch protection rules
- PR required before merging to main
- At least 1 approving review
- Required Azure Pipeline check must pass
- Linear history enabled (no merge commits)
- Force-push and branch deletion disabled
## Testing Strategy
### Unit tests:
    Framework: pytest
    Coverage: pytest-cov
    Pipeline enforces minimum coverage threshold (>=80%)

### Performance tests:
    Tool: Apache JMeter
    Output: HTML dashboard published as pipeline artifact (jmeter-report)

### UAT tests:
    Tooling: Behave + Selenium (headless Chrome)
    Output: pipeline artifact uat-evidence contains:
    uat/behave-output.txt
    uat/screenshots/*.png (only created on failure)

## Environment Setup and Configuration
Two environments are used in Azure DevOps:
- Test
- Prod

Each environment is configured in Azure DevOps Environments and referenced by deployment jobs in YAML.

## Deployment Process

### Test deployment:
- Uses build artifact (drop) from BuildAndTest stage
- Starts Flask app
- Runs smoke test request to confirm the service responds correctly
- Stops the app after verification

### Prod deployment:
- Requires manual approval gate before execution
- After approval, deploys and verifies the application in the Prod environment
- Approval gates are configured using Azure DevOps Environments, requiring a designated approver before the Prod deployment stage can execute.

## Security and Performance Testing
### Performance:
- JMeter stage executes automatically after Test deploy
- Reports are available under pipeline “Artifacts” (jmeter-report and jmeter-results)

## UAT Testing with Selenium

UAT is implemented using Behave + Selenium.
- Headless Chrome is used in CI (--headless=new)
- On step failure, a screenshot is captured automatically into uat/screenshots/

To run locally:
```
python app.py
behave uat/features
```
## Security Testing

Security controls are integrated into the CI/CD process to identify common risks early:

- Secret scanning is performed to detect hard-coded credentials or tokens
- Dependency analysis ensures third-party Python packages do not introduce known vulnerabilities

These checks help prevent insecure configurations from progressing through the pipeline.

## Evidence and Artifacts

The following evidence is available directly from Azure DevOps pipeline runs:
- Build artifact: `drop`
- Code coverage report (HTML + Cobertura summary)
- JMeter performance report (`jmeter-report`)
- UAT evidence (`uat-evidence`) including:
  - Behave execution output
  - Screenshots captured on test failure

## Troubleshooting Guide
- Pipeline succeeds but UAT results not visible in “Tests” tab:
    - This is expected if JUnit publishing is not enabled. UAT results are available via logs and uat-evidence artifact.

- Selenium fails on CI:
    - Confirm headless flags are enabled and ChromeDriver is available on ubuntu-latest.

- JMeter report empty:
    - Ensure the app is running before JMeter starts and the JMX target host/port matches the Flask server.

## Running the App
For example:
```bash
python3 -m main.py add 2 3
python3 -m main.py sub 5 2
```