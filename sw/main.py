from machine import Pin
from utime import sleep, ticks_diff, ticks_ms
import machine
import micropython
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

# Global variables for the algorithms
bay = 0
time_constant = 1  # time to rotate 180 degrees at 100% power

bot = robot(time_constant=time_constant)

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
place_reel = bot.place_reel

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
lift()
open()
while True:
    if _start_requested and not _running:
        _start_requested = False
        _running = True
        drive_forward(time_constant * 0.8)

        lower()
        navigate(start_route)
        rack = 0
        while True:
            if bay % 2 == 0:
                rack = 0
            else:
                rack = 2
            pick_reel()
            read_reel()
            rotate_left(time_constant*1.5)

            navigate(routes_to_racks[bay][rack])

            find_empty(0)
            
            place_reel(0)

            bay = (bay + 1) % 4
            navigate(routes_to_bays[rack][bay])

    bay = (bay + 1) % 4

    sleep(0.05)
