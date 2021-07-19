from typing import Callable, List
from dataclasses import dataclass
import re
from datetime import datetime, timedelta
from pytz import UTC, timezone
from noaa_sdk import NOAA
from .do_later import Fork

zip_code = 98102

noaa_time_format = '%Y-%m-%dT%H:%M:%S%z'

@dataclass
class WeatherInfo:
    time: str
    icon: str
    temp: str

def get_weather(post_result: Callable[[List[WeatherInfo]], None]):
    def c_to_f(temp):
        return int(round(temp * 1.8 + 32, 0))

    def image_for_obs(iconurl):
        regex = re.compile("https:\/\/api\.weather\.gov\/icons\/land\/([^\d,]+),?(\d+)?\?size=\w+")
        mapping = {
            "day/skc": "sunny",
            "night/skc": "sunny_night",
            "day/sct": "cloudy2",
            "night/sct": "cloudy2_night",
            "day/bkn": "cloudy3",
            "night/bkn": "cloudy3_night",
            "day/rain": "shower1",
            "night/rain": "shower1_night",
            "day/few": "cloudy1",
            "night/few": "cloudy1_night",
            "day/ovc": "overcast",
            "night/ovc": "overcast",
            None: "unknown"
        }
        matches = regex.match(iconurl or "")
        if (matches == None): return mapping[None]
        else: return mapping[matches.group(1)]
    
    now = datetime.now(timezone('US/Pacific'))
    today = now.date()
    two_hours = now + timedelta(hours=2)
    tomorrow = datetime.replace(now, day=today.day + 1, hour=11)
    next_day = datetime.replace(tomorrow, day=today.day + 2)

    required_forecasts = {
        '2hr': two_hours,
        tomorrow.strftime('%a'): tomorrow,
        next_day.strftime('%a'): next_day
    }

    weather: List[WeatherInfo] = []

    n = NOAA()
    def get_observation():
        obs = next(n.get_observations(zip_code, 'US'))
    
        weather.insert(0, WeatherInfo(
            time="Now",
            icon=image_for_obs(obs['icon']),
            temp=f'{c_to_f(obs["temperature"]["value"])}°'
        ))
        post_result(weather)
    Fork(get_observation)

    hourly_forecasts = n.get_forecasts(zip_code, 'US')
    long_forecasts = n.get_forecasts(zip_code, 'US', type="forecast")

    for label in required_forecasts:
        if required_forecasts[label] - now < timedelta(hours=10): 
            forecasts_to_check = hourly_forecasts
        else: 
            forecasts_to_check = long_forecasts
        
        for forecast in forecasts_to_check:
            if (required_forecasts[label] > datetime.strptime(forecast['startTime'], noaa_time_format) and required_forecasts[label] < datetime.strptime(forecast['endTime'], noaa_time_format)):
                weather.append(WeatherInfo(
                    time=label,
                    icon=image_for_obs(forecast['icon']),
                    temp=f'{forecast["temperature"]}°'
                ))
                post_result(weather)