# from test_led import test_led
# from test_pwm import test_pwm
# from test_input import test_input_poll
# from test_motor import test_motor
# from test_linear_actuator import test_actuator1
# from test_tcs3472 import test_tcs3472
# from test_vl53l0x import test_vl53l0x
# from test_mfrc522 import test_mfrc522
# from test_TMF8x01_get_distance import test_TMF8x01_get_distance
# from test_STU_22L_IO_Mode import test_STU_22L_IO_Mode
# from test_STU_22L_UART import test_STU_22L_UART
# from test_tiny_code_reader import test_tiny_code_reader

# from netlog import wlan_connect, UDPLogger

# wlan_connect("Eduroam Never Works", "iNeedWifi")
# log = UDPLogger("10.29.50.253", 9000)

# log.log("starting test")
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

# print("main.py Done!")

import machine
import micropython
from main import drive_forward, navigate, turn_left
from machine import Pin
from utime import sleep, ticks_diff, ticks_ms

micropython.alloc_emergency_exception_buf(100)

button_pin = 22
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)
time_constant = 1.5 / 2  # time to rotate 90 degrees at 50% power

route = [
    "L",
    "SL",
    "R",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "R",
    "SR",
    "R",
    "SL",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "R",
    "SL",
    "L",
]

_DEBOUNCE_MS = 250
_last_press_ms = 0
_start_requested = False
_running = False


def _on_button_press_scheduled(_):
    global _running, _start_requested
    if _running:
        print("reset")
        sleep(0.05)
        machine.reset()
    else:
        _start_requested = True


def _on_button_irq(_pin):
    global _last_press_ms
    now = ticks_ms()
    if ticks_diff(now, _last_press_ms) < _DEBOUNCE_MS:
        return
    _last_press_ms = now
    micropython.schedule(_on_button_press_scheduled, 0)


button.irq(trigger=Pin.IRQ_RISING, handler=_on_button_irq)


while True:
    if _start_requested and not _running:
        _start_requested = False
        _running = True
        print("start")
        drive_forward(time_constant)
        navigate(route)
        turn_left(0.4 * 2 / 2)
        drive_forward(time_constant)
        _running = False
        print("done")

    sleep(0.05)
