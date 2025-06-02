from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from pyowm.weatherapi25.weather import Weather


def _return_results(w: "Weather") -> Dict:
    return {
        "temp": w.temperature('celsius')['temp'],
        "temp_feels_like": w.temperature('celsius')['feels_like'],
        "common_status": w.status,
        "humidity": w.humidity,
        "wind_speed": w.wind()['speed'],
        "clouds": w.clouds,
    }


def _preprocessing_place(place: str) -> str:
    place = place.lower().strip()
    return ' '.join(place.split())
