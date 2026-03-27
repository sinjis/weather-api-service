
# weather-api-service

Minimal sample "Weather API" service intended for GitHub upload.

* Language: Python
* HTTP framework: Flask
* Tests: pytest
* Coverage: configured for 100% (lines + branches)

## Structure

```
src/weather_api_service/   # application code
tests/                     # unit tests
```

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]

# run tests with coverage
pytest

# run server
python -m weather_api_service.api
```

Then browse:
* `GET http://localhost:8080/health`
* `GET http://localhost:8080/weather?city=Oslo&unit=C`

## Coverage

```bash
pytest --cov
```
