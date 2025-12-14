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

# Create virtual environment
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
    test_modulo.py
main.py
app.py
azure-pipelines.yml
README.md
requirements.txt
```

## CI Pipeline Implementation
The Azure DevOps pipeline is implemented in `azure-pipelines.yml` and runs on `ubuntu-latest`.

### Triggers:

- CI trigger on pushes to main
- PR validation on PRs targeting main

### Stages:
At a high level, the pipeline enforces the following flow:
- **Build, lint, unit test, and coverage enforcement**
- **Security scanning (secrets and dependencies)**
- **Deployment to Test with smoke testing**
- **Performance testing**
- **User Acceptance Testing (UAT)**
- **Controlled deployment to Production**
s
Each stage must succeed before the next stage can execute, ensuring that only verified and secure code progresses through the pipeline.

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

Production deployment is implemented as a separate pipeline stage and is not executed automatically.

Key characteristics:
- Uses a dedicated Azure DevOps Environment (`Production`)
- Protected by a manual approval gate
- Only runs if:
    - All previous stages succeed
    - An authorized approver approves the deployment

During the production stage:
- The application is started using the production artifact
- A verification request is executed against the API
- The application is stopped after validation (simulated production - deployment)

This demonstrates controlled release management and separation between Test and Production environments.

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
UAT tests are implemented using a black-box approach, interacting with the application through the web interface in the same way an end user would. This validates not only functionality, but also integration between the UI, backend logic, and deployment configuration.

## Security Testing

### Secret Scanning (Gitleaks)
- Tool: Gitleaks
- Purpose: Detect hard-coded secrets, tokens, or credentials
- Scope:
    - Scans the repository working tree
    - Uses a configuration file (`.gitleaks.toml`)
- Output:
    - JSON report published as a pipeline artifact (`sec-gitleaks`)
- Pipeline behavior:
    - The pipeline fails immediately if secrets are detected
This ensures that sensitive information cannot be accidentally committed or deployed.

### Dependency Vulnerability Scanning (pip-audit)
- Tool: pip-audit
- Purpose: Identify known vulnerabilities in third-party Python dependencies
- Scope:
    - Scans `requirements.txt` against vulnerability databases
- Output:
    - JSON report published as a pipeline artifact (`sec-pip-audit`)
- Pipeline behavior:
    - The pipeline fails if vulnerable dependencies are detected

## Evidence and Artifacts
Artifacts are used to ensure traceability and immutability across pipeline stages.
- The **build artifact** (`drop`) is created once and reused by:
    - Test deployment
    - Performance testing
    - UAT testing
    - Production deployment
- This ensures that the exact same build is tested and deployed across all environments.

Additional artifacts provide assessment evidence:
- `sec-gitleaks`: Secret scanning results
- `sec-pip-audit`: Dependency vulnerability scan results
- `jmeter-report`: Performance test dashboard
- `uat-evidence`: UAT logs and screenshots

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