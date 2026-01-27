from test_motor import Motor
from machine import ADC, Pin
from utime import sleep

motor3 = Motor(dirPin=4, PWMPin=5)
motor4 = Motor(dirPin=7, PWMPin=6)
line_sensor1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
line_sensor2 = Pin(17, Pin.IN, Pin.PULL_DOWN)
line_sensor3 = Pin(18, Pin.IN, Pin.PULL_DOWN)
line_sensor4 = Pin(19, Pin.IN, Pin.PULL_DOWN)
blue_led = Pin(10, Pin.OUT)
green_led = Pin(11, Pin.OUT)
red_led = Pin(12, Pin.OUT)
yellow_led = Pin(14, Pin.OUT)
adc_pin = 28
adc = ADC(Pin(adc_pin))
reels = 0
bay = 0
time_constant = 1 # time to rotate 90 degrees at 50% power


def follow_line():
    sensor2 = line_sensor2.value()
    sensor3 = line_sensor3.value()
    if not sensor2 and not sensor3:
        motor3.Forward()
        motor4.Forward()
    elif sensor2:
        motor4.off()
        motor3.Forward()
    else:
        motor3.off()
        motor4.Forward()

def check_junction():
    sensor1 = line_sensor1.value()
    sensor4 = line_sensor4.value()
    if sensor1 and not sensor4:
        return "L"
    elif sensor1 and sensor4:
        return "T"
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

def drive_forward(time):
    motor3.Forward()
    motor4.Forward()
    sleep(time)


def navigate(route):
    for inst in route:
        success = False
        i = 0

        while not success:
            junc = check_junction()
            while junc == False:
                if i % 100 == 0:
                    junc = check_junction()
                follow_line()
                i += 1
            motor3.off()
            motor4.off()

            match inst:
                case "LT":
                    if junc == "T":
                        turn_left(time_constant)
                        success = True
                case "RT":
                    if junc == "T":
                        turn_right(time_constant)
                        success = True
                case "SL":
                    if junc == "L":
                        drive_forward(time_constant*0.4)
                        success = True
                case "SR":
                    if junc == "R":
                        drive_forward(time_constant*0.4)
                        success = True
                case "L":
                    if junc == "L":
                        turn_left(time_constant)
                        success = True
                case "R":
                    if junc == "R":
                        turn_right(time_constant)
                        success = True
                case "ST":
                    if junc == "T":
                        motor3.off()
                        motor4.off()
                        success = True
                case "SC":
                    if junc == "T":
                        drive_forward(time_constant*0.4)
                        success = True

# rackA upper = 0
# rackA lower = 1
# rackB upper = 2
# rackB lower = 3
def read_reel():
    adc_value = adc.read_u16()
    scaled_voltage = adc_value / 65535
    if scaled_voltage < 0.1:
        blue_led.value(1)
        return 0
    elif scaled_voltage < 0.45:
        green_led.value(1)
        return 1
    elif scaled_voltage < 0.85:
        red_led.value(1)
        return 2
    yellow_led.value(1)
    return 3

# LT - left at T junction
# RT - right at T junction
# SL - straight on when a branch appears on the left
# SR - straight on when a branch appears on the right
# L - left at a branch
# R - right at a branch
# ST - stop at T junction
# SC - straight on at crossroads

# bay1 = 0
# bay2 = 1
# bay3 = 2
# bay4 = 3

start_route = ["LT","SL","LT","ST"]

routes_to_racks = [[["SR","SR","SR","SR","SR","SR","SR","SC","R","RT"],["SR"],["SR","SR","SR","SR","SR","SR","SR","SC","R","LT"],["R","SR","SR","SR","LT"]],
[["LT","RT","SR","SR","SR","SR","SR","SR","SC","R","RT"],["LT","RT"],["LT","RT","SR","SR","SR","SR","SR","SR","SC","R","LT"],["RT","SR","SR","LT"]],
[["RT","RT","SL","SL","SL","SL","SL","SL","SC","L","RT"],["LT","SL","SL","RT"],["RT","RT","SL","SL","SL","SL","SL","SL","SC","L","LT"],["RT","LT"]],
[["SL","SL","SL","SL","SL","SL","SL","SC","L","RT"],["L","SL","SL","SL","RT"],["SL","SL","SL","SL","SL","SL","SL","SC","L","LT"],["SL"]]]

routes_to_bays = [[["SL","ST"],["L","R","ST"],["L","SR","SR","R","ST"],["L","SR","SR","SR","R","ST"]],
[["L","LT","SC","SL","SL","SL","SL","SL","SL","SL","ST"],["L","LT","SC","SR","SL","SL","SL","SL","SL","L","R","ST"],["L","RT","SC","SR","SR","SR","SR","SR","SR","R","L","ST"],["L","RT","SC","SR","SR","SR","SR","SR","SR","SR","ST"]
],
[["R","SL","SL","SL","LT","ST"],["R","SL","SL","L","ST"],["R","L","ST"],["SR","ST"]],
[["R","LT","SC","SL","SL","SL","SL","SL","SL","SL","ST"],["R","LT","SC","SR","SL","SL","SL","SL","SL","L","R","ST"],["R","RT","SC","SR","SR","SR","SR","SR","SR","R","L","ST"],["R","RT","SC","SR","SR","SR","SR","SR","SR","SR","ST"]]]

# main loop

while True:
    reels += 1
    drive_forward(time_constant)
    navigate(start_route)
    rack_location = read_reel()
    navigate(routes_to_racks[bay][rack_location])
    
    navigate(routes_to_bays[rack_location][bay])