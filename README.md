# junit-report-result-analyzer

Small POC to create an automated tool to analyze all JUnit reports found on the provided path, 
returns 0 if no errors or failures are found among the analyzed JUnit test reports, otherwise return code is 1

## How to use

install it with 
```
python -m venv .venv && source .venv/bin/activate && pip install -e .
```

run it with

```
check-junit-results
```

optionally provide "PATH" as an argument, local directory is used as the default value for the location of the JUnit reports

