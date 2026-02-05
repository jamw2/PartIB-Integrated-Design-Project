from test_motor import Motor
from machine import ADC, Pin, I2C
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from utime import sleep

# from netlog import UDPLogger, wlan_connect


# wlan_connect("Eduroam Never Works", "iNeedWifi")
# log = UDPLogger("10.29.50.253", 9000)

# Set up distance sensors
# i2c_bus = I2C(id=0, sda=Pin(8), scl=Pin(9))
# tof = DFRobot_TMF8701(i2c_bus=i2c_bus)
# tof.begin()
# vl53l0 = VL53L0X(i2c_bus)
# vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[0], 18)
# vl53l0.set_Vcsel_pulse_period(vl53l0.vcsel_period_type[1], 14)

# Set up motors
motor3 = Motor(dirPin=4, PWMPin=5)
motor4 = Motor(dirPin=7, PWMPin=6)

# Set up line sensors
line_sensor1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
line_sensor2 = Pin(18, Pin.IN, Pin.PULL_DOWN)
line_sensor3 = Pin(17, Pin.IN, Pin.PULL_DOWN)
line_sensor4 = Pin(16, Pin.IN, Pin.PULL_DOWN)

# Set up LEDs
blue_led = Pin(10, Pin.OUT)
green_led = Pin(11, Pin.OUT)
red_led = Pin(12, Pin.OUT)
yellow_led = Pin(14, Pin.OUT)

# Set up ADC (for measuring reels)
adc_pin = 28
adc = ADC(Pin(adc_pin))
us_pin = 26
us = ADC(Pin(us_pin))

# Global variables for the algorithms
reels = 0
bay = 0
time_constant = 1 # time to rotate 90 degrees at 100% power


def follow_line():
    # use the inner two line sensors
    sensor2 = line_sensor2.value()
    sensor3 = line_sensor3.value()
    # go straight if both sensors see the line
    if sensor2 and sensor3:
        motor3.Forward()
        motor4.Forward()
    # turn back to the line if it goes off to the left
    elif not sensor2:
        motor4.Forward(50)
        motor3.Forward()
    # otherwise turn back to the line the other way
    else:
        motor3.Forward(50)
        motor4.Forward()


def check_junction():
    # use the outer two line sensors
    sensor1 = line_sensor1.value()
    sensor4 = line_sensor4.value()
    # sense a junction on the left
    if sensor1 and not sensor4:
        return "L"
    # elif sensor1 and sensor4:
    #     return "T"
    # sense a junction on the right
    elif not sensor1 and sensor4:
        return "R"
    return False


def turn_left(time):
    motor3.off()
    motor4.Forward()
    sleep(time)
    motor4.off()


def turn_right(time):
    motor3.Forward()
    motor4.off()
    sleep(time)
    motor3.off()


def rotate_left(time):
    motor3.Reverse()
    motor4.Forward()
    sleep(time / 2)
    motor3.off()
    motor4.off()


def rotate_right(time):
    motor3.Forward()
    motor4.Reverse()
    sleep(time / 2)
    motor3.off()
    motor4.off()


def drive_forward(time):
    motor3.Forward()
    motor4.Forward()
    sleep(time)
    motor3.off()
    motor4.off()


# def navigate(route):
#     for inst in route:
#         success = False
#         i = 0
def navigate(route):
    idx = 0
    while idx < len(route):
        inst = route[idx]
        success = False
        i = 0

        while not success:
            junc = check_junction()
            while junc == False:
                if i % 50 == 0:
                    junc = check_junction()
                    # if junc == "L" or junc == "R":
                    #     drive_forward(time_constant * 0.2)
                    #     junc2 = check_junction()
                    #     if junc2 == "T":
                    #         junc = "T"
                follow_line()
                i += 1
            motor3.off()
            motor4.off()
            print(inst, junc)
            # us_val = read_us()
            # log.log(f"{inst}, {junc}, {us_val}")
            if inst == "LT":
                if junc == "T":
                    turn_left(time_constant)
                    success = True
                    idx += 1
            elif inst == "RT":
                if junc == "T":
                    turn_right(time_constant)
                    success = True
                    idx += 1
            elif inst == "SL":
                if junc == "L":
                    drive_forward(time_constant * 0.2)
                    success = True
                    idx += 1
            elif inst == "SR":
                if junc == "R":
                    drive_forward(time_constant * 0.2)
                    success = True
                    idx += 1
            elif inst == "L":
                if junc == "L":
                    turn_left(time_constant * 0.5)
                    motor4.Forward()
                    while not line_sensor4.value():
                        continue
                    motor4.off()
                    turn_right(time_constant * 0.2)
                    success = True
                    idx += 1
            elif inst == "R":
                if junc == "R":
                    turn_right(time_constant * 0.5)
                    motor3.Forward()
                    while not line_sensor1.value():
                        continue
                    motor3.off()
                    turn_left(time_constant * 0.2)
                    success = True
                    idx += 1
            elif inst == "ST":
                if junc == "T":
                    motor3.off()
                    motor4.off()
                    success = True
                    idx += 1
            elif inst == "SC":
                if junc == "T":
                    drive_forward(time_constant * 0.4)
                    success = True
                    idx += 1
            elif inst == "STL":
                if junc == "L":
                    motor3.off()
                    motor4.off()
                    success = True
                    idx += 1
            elif inst == "STR":
                if junc == "R":
                    motor3.off()
                    motor4.off()
                    success = True
                    idx += 1
            if not success:
                drive_forward(0.1)


# rackA upper = 0
# rackA lower = 1
# rackB upper = 2
# rackB lower = 3

# unscaled ultrasonic sensor reading
def read_us():
    us_value = us.read_u16()
    return us_value


def read_reel():
    adc_value = adc.read_u16()
    scaled_voltage = adc_value / 65535
    scaled_voltage = scaled_voltage / 0.72
    print(f"{adc_value},{scaled_voltage}")
    if scaled_voltage < 0.1:
        blue_led.value(1)
        return 0
    elif scaled_voltage < 0.45:
        green_led.value(1)
        return 1
    elif scaled_voltage < 0.94:
        red_led.value(1)
        return 2
    yellow_led.value(1)
    return 3

"""
def find_empty(rack):
    position = 1
    while True:
        if rack == 0 or rack == 3:
            tof.start_measurement(calib_m=tof.eMODE_NO_CALIB, mode=tof.eCOMBINE)
            if tof.is_data_ready() == True:
                dist = tof.get_distance_mm()
            inst = "STL"
        else:
            vl53l0.start()
            dist = vl53l0.read()
            inst = "STR"
        if dist < 200:
            return position
        navigate(inst)
        position += 1
"""

def place_reel(rack):

    green_led.value(0)
    yellow_led.value(0)
    red_led.value(0)
    blue_led.value(0)
    return


# LT - left at T junction
# RT - right at T junction
# SL - straight on when a branch appears on the left
# SR - straight on when a branch appears on the right
# L - left at a branch
# R - right at a branch
# ST - stop at T junction
# SC - straight on at crossroads
# STL - stop at a branch on the left
# STR - stop at a branch on the right

# bay1 = 0
# bay2 = 1
# bay3 = 2
# bay4 = 3

# rackA upper = 0
# rackA lower = 1
# rackB upper = 2
# rackB lower = 3

start_route = ["L", "SL", "L","STL"]

routes_to_racks = [
    [
        ["SR", "SR", "SR", "SR", "SR", "SR", "SR", "SC", "R", "R", "R", "R", "STL"],
        ["SR", "STR"],
        ["SR", "SR", "SR", "SR", "SR", "SR", "SR", "SC", "R", "R", "L", "L", "STR"],
        ["R", "SR", "SR", "SR", "L", "STL"],],
    [
        ["L","R","SR","SR","SR","SR","SR","SR","SC","R","R","R","R","STL",],
        ["L", "R", "STR"],
        ["L","R","SR","SR","SR","SR","SR","SR","SC","R","R","L","L","STR",],
        ["R", "SR", "SR", "L", "STL"],
    ],
    [
        ["R","R","SL","SL","SL","SL","SL","SL","SC","L","L","R","R","STL",],
        ["L", "SL", "SL", "R", "STR"],
        ["R","R","SL","SL","SL","SL","SL","SL","SC","L","L","L","L","STR",],
        ["R", "L", "STL"],
    ],
    [
        ["SL", "SL", "SL", "SL", "SL", "SL", "SL", "SC", "L", "L", "RT", "R", "STL"],
        ["L", "SL", "SL", "SL", "RT", "STR"],
        ["SL", "SL", "SL", "SL", "SL", "SL", "SL", "SC", "L", "L", "LT", "L", "STR"],
        ["SL", "STL"],
    ],
]

routes_to_bays = [
    [
        ["SL", "STL"],
        ["L", "R", "STL"],
        ["L", "SR", "SR", "R", "STL"],
        ["L", "SR", "SR", "SR", "R", "STL"],
    ],
    [
        ["L", "L", "L", "L", "SC", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "STL"],
        ["L", "L", "L", "L", "SC", "SR", "SL", "SL", "SL", "SL", "SL", "L", "R", "STL"],
        ["L", "L", "R", "R", "SC", "SR", "SR", "SR", "SR", "SR", "SR", "R", "L", "STL"],
        ["L", "L", "R", "R", "SC", "SR", "SR", "SR", "SR", "SR", "SR", "SR", "STL"],
    ],
    [
        ["R", "SL", "SL", "SL", "LT", "STL"],
        ["R", "SL", "SL", "L", "STL"],
        ["R", "L", "STL"],
        ["SR", "STL"],
    ],
    [
        ["R", "R", "L", "L", "SC", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "STL"],
        ["R", "R", "L", "L", "SC", "SR", "SL", "SL", "SL", "SL", "SL", "L", "R", "STL"],
        ["R", "R", "R", "R", "SC", "SR", "SR", "SR", "SR", "SR", "SR", "R", "L", "STL"],
        ["R", "R", "R", "R", "SC", "SR", "SR", "SR", "SR", "SR", "SR", "SR", "STL"],
    ],
]

# main loop

# while True:
#     reels += 1
#     drive_forward(time_constant)
#     navigate(start_route)
#     rack_location = read_reel()
#     navigate(routes_to_racks[bay][rack_location])
#     num_steps_to_backtrack = find_empty(rack_location)
#     place_reel(rack_location)
#     turn_left(2 * time_constant)
#     for i in range(num_steps_to_backtrack):
#         if rack_location == 0 or rack_location == 3:
#             navigate("STR")
#         else:
#             navigate("STL")
#     navigate(routes_to_bays[rack_location][bay])
