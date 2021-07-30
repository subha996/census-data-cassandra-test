
from requests import get
from datetime import datetime



def user_info():
    now = datetime.now()
    time = now.strftime("%H:%M:%S")
    loc = get('https://ipapi.co/json/')
    res = loc.json()
    ip = res['ip']
    city = res['city']
    region = res['region']
    country_name = res['country_name']
    latitude = res['latitude']
    longitude = res['longitude']
    info = [time, ip, city, region, country_name, latitude, longitude]
    return list(info)



