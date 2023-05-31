import json

import urllib3 as urllib3
import SecretKeyHolder
from datetime import date, timedelta

url_base = "http://apis.data.go.kr/1360000/AsosHourlyInfoService/getWthrDataList"
service_key = SecretKeyHolder.weather_decoded
data_type = "JSON"
data_cd = "ASOS"
date_cd = "HR"
station_id = "108"
start_day_str = "20220802"
start_hour = "00"
end_hour = "23"


def weather_data_request():
    today_str = (date.today() - timedelta(days=1)).strftime("%Y%m%d")
    fields = {
        "serviceKey": service_key,
        "dataType": data_type,
        "dataCd": data_cd,
        "dateCd": date_cd,
        "stnIds": station_id,
        "endDt": today_str,
        "endHh": end_hour,
        "startDt": start_day_str,
        "startHh": start_hour
    }

    # urllib setting
    http = urllib3.PoolManager()

    # send http request
    response = http.request(
        "GET", url=url_base, fields=fields
    )

    # JSON parse
    weather_history = json.loads(response.data.decode('utf-8'))
    return weather_history


def save_weather_data(weather_history, date_str):
    with open(f'weather_data_{date_str}', 'w', encoding='utf-8') as make_file:
        json.dump(weather_history, make_file)
    return


def read_weather_data(date_str):
    with open(f'weather_data_{date_str}', 'r', encoding='utf-8') as read_file:
        weather_data_json = json.load(read_file)
    return weather_data_json


weather_data = weather_data_request()
print(weather_data)
save_weather_data(weather_data, (date.today() - timedelta(days=1)).strftime("%Y%m%d"))
data_read = read_weather_data((date.today() - timedelta(days=1)).strftime("%Y%m%d"))
print(data_read)