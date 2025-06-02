import os
from dotenv import load_dotenv
from typing import Dict

from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.commons.exceptions import NotFoundError

from .utils import (
    _preprocessing_place,
    _return_results,
    ERROR_MESSAGE,
)


load_dotenv()


class WeatherManager:
    def __init__(self):
        self.owm = OWM(
            os.getenv('OPEN_WEATHER_MAP_API_KEY')
        )
        self.mgr = self.owm.weather_manager()

    def get_weather_today(
        self,
        place: str,
    ) -> Dict | str:
        try:
            observation = self.mgr.weather_at_place(
                _preprocessing_place(place),
            )
            return _return_results(observation.weather)
        except NotFoundError:
            return ERROR_MESSAGE

    def get_weather_tomorrow(
        self,
        place: str,
        interval: str = "3h",
    ) -> Dict | str:
        try:
            forecast = self.mgr.forecast_at_place(
                _preprocessing_place(place),
                interval,
            )
            return _return_results(
                forecast.get_weather_at(timestamps.tomorrow())
            )
        except NotFoundError:
            return ERROR_MESSAGE

    def get_weather(self, place: str) -> Dict:
        return {
            "today": self.get_weather_today(place),
            "tomorrow": self.get_weather_tomorrow(place),
        }


weather_manager = WeatherManager()
