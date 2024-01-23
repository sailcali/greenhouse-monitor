#!/usr/bin/greenhouse-monitor/venv/bin/python3

from classes import Greenhouse, Heater
import time
from dotenv import load_dotenv

load_dotenv()

g = Greenhouse()
heater = Heater()
SET_LOW_POINT = 45
SET_HIGH_POINT = 60
SET_HIGH_HUMIDITY = 97
while True:
    
    heater.update_heater_status()
    g.update_greenhouse_temps()

    if heater.state == "off":
        if g.avg_temp() < SET_LOW_POINT or g.avg_hum() > SET_HIGH_HUMIDITY:
            heater.change_heater_status('on')
    else:
        if g.avg_temp() > SET_HIGH_POINT:
            heater.change_heater_status("off")
    
    print(heater.state, end="")
    print("\r", end="")
    time.sleep(60)

