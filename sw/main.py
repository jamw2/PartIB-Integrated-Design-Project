from test_led import test_led
from test_pwm import test_pwm
from test_input import test_input_poll
from test_motor import test_motor
from test_linear_actuator import test_actuator1
from test_tcs3472 import test_tcs3472
from test_vl53l0x import test_vl53l0x
from test_mfrc522 import test_mfrc522
from test_TMF8x01_get_distance import test_TMF8x01_get_distance
from test_STU_22L_IO_Mode import test_STU_22L_IO_Mode
from test_STU_22L_UART import test_STU_22L_UART
from test_tiny_code_reader import test_tiny_code_reader

from netlog import wlan_connect, UDPLogger

wlan_connect("Eduroam Never Works", "iNeedWifi")
log = UDPLogger("10.29.50.253", 9000)

log.log("starting test")
# use log.log(...) inside your loop


print("Welcome to main.py!")

# Uncomment the test to run
# test_led()
# test_pwm()
# test_input_poll()
# test_motor()
# test_tcs3472()
# test_actuator1()
# test_vl53l0x()
# test_mfrc522()
# test_TMF8x01_get_distance()
# test_STU_22L_IO_Mode()
# test_STU_22L_UART()
# test_tiny_code_reader()

print("main.py Done!")

from main_code import drive_forward, navigate

time_constant = 1  # time to rotate 90 degrees at 50% power

route = [
    "LT",
    "SL",
    "RT",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SC",
    "SR",
    "SC",
    "SL",
    "SL",
    "SL",
    "SL",
    "SL",
    "SL",
    "R",
    "SL",
    "R",
    "ST",
]

drive_forward(time_constant)
navigate(route)
drive_forward(time_constant)
