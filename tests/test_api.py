
from weather_api_service.api import create_app


def test_health_endpoint():
    app = create_app()
    client = app.test_client()
    resp = client.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {'status': 'ok'}


def test_weather_endpoint_success_default_unit():
    app = create_app()
    client = app.test_client()
    resp = client.get('/weather?city=Oslo')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['city'] == 'Oslo'
    assert data['unit'] == 'C'
    assert data['condition'] == 'cloudy'


def test_weather_endpoint_success_fahrenheit():
    app = create_app()
    client = app.test_client()
    resp = client.get('/weather?city=Oslo&unit=F')
    assert resp.status_code == 200
    data = resp.get_json()
    assert data['unit'] == 'F'
    assert data['temperature'] == 41.0


def test_weather_endpoint_validation_error():
    app = create_app()
    client = app.test_client()
    resp = client.get('/weather?city=')
    assert resp.status_code == 400
    assert 'error' in resp.get_json()
