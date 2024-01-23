import requests
from datetime import datetime
import db_util
import os

TOKEN = os.environ.get("SMARTTHINGS_TOKEN")
GREENHOUSE_IP = "http://192.168.86.247:5000"
DEVICE_URL = 'https://api.smartthings.com/v1/devices'
headers = {"Authorization": "Bearer " + TOKEN}
HEATER_ID = os.environ.get("HEATER_ID")

class Heater:
    def __init__(self):
        self.state = "off"
        self.update_heater_status()

    def update_heater_status(self):
        try:
            status_response = requests.get(f'{DEVICE_URL}/{HEATER_ID}/status', headers=headers)
            self.state = status_response.json()['components']['main']['switch']['switch']['value']
        except Exception as e:
            print(f"Connection error getting heater status: {e} at time: {datetime.now()}")
        

    def change_heater_status(self, new_state):
        params = {'commands': [{"component": 'main',
                                    "capability": 'switch',
                                    "command": new_state}]}
        try:
            response = requests.post(f"{DEVICE_URL}/{HEATER_ID}/commands", headers=headers, json=params)
            res = response.json()
            print(f'Heater turning {new_state} at time: {datetime.now()}')
            return res['results'][0]['status']
        except Exception as e:
            print(f"Connection error changing heater status: {e} at time: {datetime.now()}")
    
class Greenhouse:
    def __init__(self):
        self.temps = [65]
        self.hums = [65]

    def avg_temp(self):
        return sum(self.temps) / len(self.temps)
    
    def avg_hum(self):
        return sum(self.hums) / len(self.hums)
    
    def update_greenhouse_temps(self):
        try:
            response = requests.get(GREENHOUSE_IP)
            res = response.json()
            temp = res['temp']
            hum = res['humidity']

            db_util.log(temp,hum)

            if len(self.temps) > 9:
                del self.temps[0]
            self.temps.append(temp)
            if len(self.hums) > 9:
                del self.hums[0]
            self.hums.append(hum)
        except Exception as e:
            print(f"Could not connect to greenhouse at time: {datetime.now()}")
        
        
    
