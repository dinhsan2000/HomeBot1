"""HomeBot weather module."""

from homebot import get_config
from homebot.core.logging import LOGE
import requests

URL = "https://api.openweathermap.org/data/2.5/weather"

TEMP_UNITS = {
	"imperial": "F",
	"metric": "C"
}

WIND_UNITS = {
	"imperial": "mph",
	"metric": "km/h"
}

def weather(update, context):
	try:
		city = update.message.text.split(' ', 1)[1]
	except IndexError:
		update.message.reply_text("Thành phố không được cung cấp")
		return
	if get_config("WEATHER_API_KEY", None) == None:
		update.message.reply_text("OpenWeatherMap API key not specified\n"
								  "Ask the bot hoster to configure it")
		LOGE("OpenWeatherMap API key not specified, get it at https://home.openweathermap.org/api_keys")
		return
	parameters = {
		"appid": get_config("WEATHER_API_KEY", None),
		"q": city,
		"units": get_config("WEATHER_TEMP_UNIT", "metric"),
	}
	temp_unit = TEMP_UNITS.get(get_config("WEATHER_TEMP_UNIT", None), "K")
	wind_unit = WIND_UNITS.get(get_config("WEATHER_TEMP_UNIT", None), "km/h")
	response = requests.get(url=URL, params=parameters).json()
	if response["cod"] != 200:
		update.message.reply_text(f"Lỗi: {response['message']}")
		return
	city_name = response["name"]
	city_country = response["sys"]["country"]
	city_lat = response["coord"]["lat"]
	city_lon = response["coord"]["lon"]
	weather_type = response["weather"][0]["main"]
	weather_type_description = response["weather"][0]["description"]
	temp = response["main"]["temp"]
	temp_min = response["main"]["temp_min"]
	temp_max = response["main"]["temp_max"]
	humidity = response["main"]["humidity"]
	wind_speed = response["wind"]["speed"]
	update.message.reply_text(
		f"Thời tiết hiện tại cho {city_name}, {city_country} ({city_lat}, {city_lon}):\n"
		f"Thời tiết: {weather_type} ({weather_type_description})\n"
		f"Nhiệt độ: {temp}{temp_unit} (Thấp nhất: {temp_min}{temp_unit} Cao nhất: {temp_max}{temp_unit})\n"
		f"Độ ẩm: {humidity}%\n"
		f"Mức gió: {wind_speed}{wind_unit}"
	)

commands = [
	[weather, ['weather']]
]
