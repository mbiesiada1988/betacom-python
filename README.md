# Betacom - Playwright (Python)
## Setup
Create Python Virtual Environment with modules:

* Requests
```
pip install requests
```

* Playwright Pytest plugin
```
pip install pytest-playwright
```

* Playwright
```
playwright install
```

## Run
* Headless mode:
```
pytest
```

* Headed mode:
```
pytest --headed
```

## Output
Output files (in `.json` format) are saved in the `output` folder