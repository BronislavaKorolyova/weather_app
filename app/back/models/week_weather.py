class WeekWeather:
	def __init__(self, city, country):
		self.city = city
		self.country = country
		self.days = [] #list of weather
		self.next_id = 1
        
	def add_day(self, date, night_temp, day_temp, humidity, summary):
		from back.models.day_weather import Weather
		self.days.append(Weather(night_temp, day_temp, humidity, date, summary))        
