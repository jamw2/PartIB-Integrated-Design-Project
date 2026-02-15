from machine import Pin
from utime import sleep, ticks_diff, ticks_ms
import machine
import micropython
from netlog import UDPLogger, wlan_connect
from robot import robot
from routes import start_route, routes_to_bays, routes_to_racks
# callback memory allocation
micropython.alloc_emergency_exception_buf(100)

button_pin = 22
button = Pin(button_pin, Pin.IN, Pin.PULL_DOWN)

# button variables
_DEBOUNCE_MS = 250
_last_press_ms = 0
_start_requested = False
_running = False


# deeper logic to run outside of callback
def _on_button_press_scheduled(_):
    global _running, _start_requested
    if _running:
        log.log("reset")
        sleep(0.05)
        machine.reset()
    else:
        _start_requested = True


# interrupt handler for button, with debouncing
def _on_button_irq(_pin):
    global _last_press_ms
    now = ticks_ms()
    if ticks_diff(now, _last_press_ms) < _DEBOUNCE_MS:
        return
    _last_press_ms = now
    micropython.schedule(_on_button_press_scheduled, 0)


# set up interrupt
button.irq(trigger=Pin.IRQ_RISING, handler=_on_button_irq)

wlan_connect("Eduroam Never Works", "iNeedWifi")
log = UDPLogger("10.11.160.253", 9000)

# Global variables for the algorithms
bay = 0
time_constant = 1  # time to rotate 180 degrees at 100% power

bot = robot(log=log, time_constant=time_constant)

follow_line = bot.follow_line
check_junction = bot.check_junction
turn_left = bot.turn_left
turn_right = bot.turn_right
rotate_left = bot.rotate_left
rotate_right = bot.rotate_right
drive_forward = bot.drive_forward
reverse = bot.reverse
navigate = bot.navigate
read_us = bot.read_us
read_reel = bot.read_reel
find_empty = bot.find_empty
lift = bot.lift
lower = bot.lower
open = bot.open
close = bot.close
pick_reel = bot.pick_reel

# set up servo locations
# lift()
# open()

# main loop
# while True:
#     # wait for button
#     if _start_requested and not _running:
#         _start_requested = False
#         _running = True
#         print("start")
#         # exit starting box
#         drive_forward(time_constant)

#         navigate(start_route)
#         while True:
#             pick_reel()
#             rack_location = read_reel()
#             reverse(time_constant * 0.5)
#             rotate_left(time_constant)

#             navigate(routes_to_racks[bay][rack_location])

#             num_steps_to_backtrack = find_empty(rack_location)

#             place_reel(rack_location)

#             for i in range(num_steps_to_backtrack):
#                 if rack_location == 0 or rack_location == 3:
#                     navigate("SR")
#                 else:
#                     navigate("SL")
#             bay = (bay + 1) % 4
#             navigate(routes_to_bays[rack_location][bay])

#     sleep(0.05)

# testing navigation
log.log("online")
while True:
    if _start_requested and not _running:
        _start_requested = False
        _running = True
        log.log("start")
        drive_forward(time_constant * 0.7)

        navigate(start_route)
        pick_reel()
        rotate_left(time_constant)

        navigate(routes_to_racks[0][0])

        num_steps_to_backtrack = find_empty(0)
        log.log(num_steps_to_backtrack)

        rotate_left(time_constant)

        for i in range(num_steps_to_backtrack):
            navigate("SR")

        navigate(routes_to_bays[[0][1]])
        _running = False
        log.log("done")

    sleep(0.05)
