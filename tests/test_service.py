
import pytest

from weather_api_service.service import (
    WeatherError,
    WeatherReport,
    c_to_f,
    format_report,
    get_weather,
    validate_city,
)


def test_validate_city_normalizes_and_title_cases():
    assert validate_city('  oslo  ') == 'Oslo'


@pytest.mark.parametrize('city', ['', '   '])
def test_validate_city_rejects_empty(city):
    with pytest.raises(WeatherError):
        validate_city(city)


def test_validate_city_rejects_digits():
    with pytest.raises(WeatherError):
        validate_city('Oslo2')


def test_validate_city_rejects_non_string():
    with pytest.raises(WeatherError):
        validate_city(None)  # type: ignore


def test_get_weather_returns_known_city_mapping():
    r = get_weather('Trondheim')
    assert r.city == 'Trondheim'
    assert r.condition == 'snow'
    assert r.temperature_c == 3.5


def test_get_weather_returns_default_for_unknown_city():
    r = get_weather('Heggstad')
    assert r.condition == 'sunny'
    assert r.temperature_c == 10.0


def test_weather_report_feels_like_adjustment():
    r = WeatherReport(city='Bergen', temperature_c=7.0, condition='rain')
    assert r.feels_like_c() == 6.0


def test_c_to_f_numeric():
    assert c_to_f(0) == 32.0
    assert c_to_f(100) == 212.0


def test_c_to_f_rejects_non_numeric():
    with pytest.raises(WeatherError):
        c_to_f('nope')  # type: ignore


def test_format_report_celsius():
    r = get_weather('Oslo')
    out = format_report(r, unit='C')
    assert out['unit'] == 'C'
    assert out['temperature'] == 5.0
    assert out['feels_like'] == 5.0


def test_format_report_fahrenheit():
    r = get_weather('Oslo')
    out = format_report(r, unit='F')
    assert out['unit'] == 'F'
    assert out['temperature'] == 41.0
    assert out['feels_like'] == 41.0


def test_format_report_rejects_unit():
    r = get_weather('Oslo')
    with pytest.raises(WeatherError):
        format_report(r, unit='K')
