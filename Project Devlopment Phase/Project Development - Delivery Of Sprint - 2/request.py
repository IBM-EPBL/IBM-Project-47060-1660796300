import requests
url = "http://localhost:60000/predict_api"
r = requests.post(url,json={'wind_speed':8,'wind_direction':120,'pressure':1,'air_temperature':10})

print(r.json())
