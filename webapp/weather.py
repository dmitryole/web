from flask import current_app
import requests

def weather_by_city(city_name):
    weather_url = current_app.config['WEATHER_URL']
    params = {
        "key": current_app.config['WEATHER_API_KEY'],
        "q": city_name,
        "format": "json",
        "num_of_days": 1,
        "lang": "ru"
    }
    try:
        # Запрос
        result = requests.get(weather_url, params=params)
        # Обратотка сетевых ошибок 
        result.raise_for_status()
        weather = result.json()
        if 'data' in weather:
            if 'current_condition' in weather['data']:
                try:
                    return weather['data']['current_condition'][0]
                except(IndexError, TypeError):
                    return False
        return False
    except(result.RequestException, ValueError):
        print('Сетевая ошибка')
        return False

if __name__ == "__main__":
    weather = weather_by_city("Yekaterinburg,Russia")
    print(weather)