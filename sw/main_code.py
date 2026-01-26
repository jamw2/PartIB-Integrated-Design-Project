from test_motor import Motor
from machine import Pin
from utime import sleep

motor3 = Motor(dirPin=4, PWMPin=5)
motor4 = Motor(dirPin=6, PWMPin=7)
line_sensor1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
line_sensor2 = Pin(17, Pin.IN, Pin.PULL_DOWN)
line_sensor3 = Pin(18, Pin.IN, Pin.PULL_DOWN)
line_sensor4 = Pin(19, Pin.IN, Pin.PULL_DOWN)
reels = 0


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
                        turn_left(1)
                        success = True
                case "RT":
                    if junc == "T":
                        turn_right(1)
                        success = True
                case "SL":
                    if junc == "L":
                        drive_forward(0.4)
                        success = True
                case "SR":
                    if junc == "R":
                        drive_forward(0.4)
                        success = True
                case "L":
                    if junc == "L":
                        turn_left(1)
                        success = True
                case "R":
                    if junc == "R":
                        turn_right(1)
                        success = True
                case "ST":
                    if junc == "T":
                        motor3.off()
                        motor4.off()
                        success = True
                case "SC":
                    if junc == "T":
                        drive_forward(0.4)
                        success = True
    
# LT - left at T junction
# RT - right at T junction
# SL - straight on when a branch appears on the left
# SR - straight on when a branch appears on the right
# L - left at a branch
# R - right at a branch
# ST - stop at T junction
# SC - straight on at crossroads

start_route = ["LT","SL","LT","ST"]

bay1_rackA_lower = ["SR"]
bay1_rackA_higher = ["SR","SR","SR","SR","SR","SR","SR","SC","R","RT"]
bay1_rackB_lower = ["R","SR","SR","SR","LT"]
bay1_rackB_higher = ["SR","SR","SR","SR","SR","SR","SR","SC","R","LT"]

bay2_rackA_lower = ["LT","RT"]
bay2_rackA_higher = ["LT","RT","SR","SR","SR","SR","SR","SR","SC","R","RT"]
bay2_rackB_lower = ["RT","SR","SR","LT"]
bay2_rackB_higher = ["LT","RT","SR","SR","SR","SR","SR","SR","SC","R","LT"]

bay3_rackA_lower = ["LT","SL","SL","RT"]
bay3_rackA_higher = ["RT","RT","SL","SL","SL","SL","SL","SL","SC","L","RT"]
bay3_rackB_lower = ["RT","LT"]
bay3_rackB_higher = ["RT","RT","SL","SL","SL","SL","SL","SL","SC","L","LT"]

bay4_rackA_lower = ["L","SL","SL","SL","RT"]
bay4_rackA_higher = ["SL","SL","SL","SL","SL","SL","SL","SC","L","RT"]
bay4_rackB_lower = ["SL"]
bay4_rackB_higher = ["SL","SL","SL","SL","SL","SL","SL","SC","L","LT"]

rackA_lower_bay1 = ["SL","ST"]
rackA_lower_bay2 = ["L","R","ST"]
rackA_lower_bay3 = ["L","SR","SR","R","ST"]
rackA_lower_bay4 = ["L","SR","SR","SR","R","ST"]

rackA_higher_bay1 = ["L","LT","SC","SL","SL","SL","SL","SL","SL","SL","ST"]
rackA_higher_bay2 = ["L","LT","SC","SR","SL","SL","SL","SL","SL","L","R","ST"]
rackA_higher_bay3 = ["L","RT","SC","SR","SR","SR","SR","SR","SR","R","L","ST"]
rackA_higher_bay4 = ["L","RT","SC","SR","SR","SR","SR","SR","SR","SR","ST"]

rackB_lower_bay1 = ["R","SL","SL","SL","LT","ST"]
rackB_lower_bay2 = ["R","SL","SL","L","ST"]
rackB_lower_bay3 = ["R","L","ST"]
rackB_lower_bay4 = ["SR","ST"]

rackB_higher_bay1 = ["R","LT","SC","SL","SL","SL","SL","SL","SL","SL","ST"]
rackB_higher_bay2 = ["R","LT","SC","SR","SL","SL","SL","SL","SL","L","R","ST"]
rackB_higher_bay3 = ["R","RT","SC","SR","SR","SR","SR","SR","SR","R","L","ST"]
rackB_higher_bay4 = ["R","RT","SC","SR","SR","SR","SR","SR","SR","SR","ST"]


# main loop

while True:
    reels += 1
    start_route