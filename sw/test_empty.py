from machine import Pin
from utime import sleep, ticks_diff, ticks_ms
import machine
import micropython
from robot import robot
from routes import start_route, routes_to_bays, routes_to_racks

bot = robot(1)

bot.find_empty(1)
