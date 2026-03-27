
"""Minimal HTTP API using Flask.

Run locally:
    python -m weather_api_service.api

Endpoints:
    GET /health
    GET /weather?city=Oslo&unit=C
"""

from __future__ import annotations

from flask import Flask, jsonify, request

from .service import WeatherError, format_report, get_weather


def create_app() -> Flask:
    app = Flask(__name__)

    @app.get('/health')
    def health():
        return jsonify({"status": "ok"})

    @app.get('/weather')
    def weather():
        city = request.args.get('city', '')
        unit = request.args.get('unit', 'C')
        try:
            report = get_weather(city)
            payload = format_report(report, unit=unit)
        except WeatherError as e:
            return jsonify({"error": str(e)}), 400
        return jsonify(payload)

    return app


def main() -> None:
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=False)


if __name__ == '__main__':
    main()
