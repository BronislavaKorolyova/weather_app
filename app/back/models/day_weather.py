import datetime as dt

class Weather(object):
	def __init__(self, night_temp: float, day_temp: float, humidity: float, date, summary: str):
		self.night_temp = night_temp 
		self.day_temp = day_temp 
		self.humidity = humidity
		self.date = date
		self.summary = summary
