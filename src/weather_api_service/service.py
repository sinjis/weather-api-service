
"""Core weather-domain logic.

This module is intentionally small but fully tested to demonstrate high unit-test coverage.
"""

from __future__ import annotations

from dataclasses import dataclass


class WeatherError(ValueError):
    """Raised when user input is invalid for weather calculations."""


@dataclass(frozen=True)
class WeatherReport:
    city: str
    temperature_c: float
    condition: str

    def feels_like_c(self) -> float:
        """A tiny, deterministic 'feels like' approximation for demo purposes."""
        # Mild adjustment based on condition
        delta = {
            "sunny": 1.0,
            "cloudy": 0.0,
            "rain": -1.0,
            "snow": -2.0,
        }.get(self.condition, 0.0)
        return round(self.temperature_c + delta, 1)


def validate_city(city: str) -> str:
    """Validate and normalize a city name."""
    if not isinstance(city, str):
        raise WeatherError("city must be a string")
    normalized = city.strip()
    if not normalized:
        raise WeatherError("city cannot be empty")
    if any(ch.isdigit() for ch in normalized):
        raise WeatherError("city cannot contain digits")
    # Title-case for consistent responses
    return normalized.title()


def get_weather(city: str) -> WeatherReport:
    """Return a deterministic weather report for a given city.

    This is a stub (no external calls) so that the repo is self-contained.
    """
    city_n = validate_city(city)

    # Deterministic pseudo-data so tests remain stable.
    # We intentionally keep the mapping tiny.
    lookup = {
        "Oslo": (5.0, "cloudy"),
        "Trondheim": (3.5, "snow"),
        "Bergen": (7.0, "rain"),
    }
    temp, cond = lookup.get(city_n, (10.0, "sunny"))
    return WeatherReport(city=city_n, temperature_c=temp, condition=cond)


def c_to_f(c: float) -> float:
    """Convert Celsius to Fahrenheit."""
    if not isinstance(c, (int, float)):
        raise WeatherError("temperature must be numeric")
    return (c * 9.0 / 5.0) + 32.0


def format_report(report: WeatherReport, unit: str = "C") -> dict:
    """Format a report as a JSON-serializable dict."""
    unit_n = unit.upper().strip()
    if unit_n not in {"C", "F"}:
        raise WeatherError("unit must be 'C' or 'F'")
    temp = report.temperature_c if unit_n == "C" else round(c_to_f(report.temperature_c), 1)
    feels_like = report.feels_like_c() if unit_n == "C" else round(c_to_f(report.feels_like_c()), 1)
    return {
        "city": report.city,
        "temperature": temp,
        "unit": unit_n,
        "condition": report.condition,
        "feels_like": feels_like,
    }
