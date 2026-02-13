from test_motor import Motor
from machine import ADC, Pin, I2C, PWM, SoftI2C
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from utime import sleep, ticks_diff, ticks_ms
import machine
import micropython

print("top")
i2c_bus = I2C(id=0, sda=Pin(20), scl=Pin(21), freq=100000)
print(i2c_bus.scan())
tof = DFRobot_TMF8701(i2c_bus=i2c_bus)
while (tof.begin() != 0):
    print("   Initialisation failed")
    sleep(0.5)
print("   Initialisation done.")

vl53l0 = VL53L0X(i2c_bus)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)

print("init")
# left
tof.start_measurement(calib_m=tof.eMODE_NO_CALIB, mode=tof.eCOMBINE)
sleep(1)
if (tof.is_data_ready() == True):
    dist1 = tof.get_distance_mm()

# # right
vl53l0.start()
dist2 = vl53l0.read()

print("start")
while True:
    if (tof.is_data_ready() == True):
        dist1 = tof.get_distance_mm()
    dist2 = vl53l0.read()
    print(f"left: {dist1}, right: {dist2}")
    sleep(0.5)
