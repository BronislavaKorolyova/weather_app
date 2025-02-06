
import logging
import os
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from back.weather_service import WeatherService
from back.geo_service import GeoService

geo_service = GeoService()
weather_service = WeatherService()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def register_routes(app):
    @app.route("/", methods=["GET", "POST"])
    def home():
        result = None
        instance_id = os.getenv("APP_INSTANCE", "unknown")
        if request.method == "POST":
            city = request.form.get("city")
            country = request.form.get("country")
            logging.debug(f'{instance_id} Received city: {city}, country: {country}')
            try:
                location = geo_service.get_location(city, country)
                if location:
                    logging.info(f'Location found: {location}')
                    return redirect(url_for("weather", lat=location.lat, lon=location.lon, city_name=location.name, country_code=location.country))
                else:
                    result = "No data found for the given location."
                    logging.warning('No data found for the given location')
            except Exception as e:
                result = f"Error: {e}"
        return render_template("index.html", result=result, instance_id=instance_id)

    @app.route("/weather", methods=["GET"])
    def weather():
        latitude = request.args.get("lat")
        longitude = request.args.get("lon")
        city_name = request.args.get("city_name")
        country_code = request.args.get("country_code")
        logging.debug(f'Query parameters - Latitude: {latitude}, Longitude: {longitude}, City: {city_name}, Country: {country_code}')
        if not latitude or not longitude:
            logging.error('Missing coordinates, redirecting to home page')        
            return redirect(url_for("home"))
        try:
            daily_weather = weather_service.get_weather_data(latitude, longitude, city_name, country_code)
            return render_template("weather.html", daily_weather=daily_weather)
        except Exception as e:
            logging.error(f'Error fetching weather data: {e}', exc_info=True)
            return render_template("weather.html", error=f"Error fetching weather data: {e}")

    @app.errorhandler(Exception)
    def handle_exception(e):
        logging.error('An exception occurred', exc_info=True)
        if hasattr(e, 'code') and 400 <= e.code <= 599:
        	logging.warning(f'HTTP error occurred: {e}')
        	return render_template("error.html", error_message=str(e)), e.code

        logging.critical('An unexpected error occurred', exc_info=True)
        return render_template("error.html", error_message="An unexpected error occurred."), 500            

