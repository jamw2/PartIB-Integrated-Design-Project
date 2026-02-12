from machine import Pin
from utime import sleep

# Same wiring as main.py
line_sensor1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
line_sensor2 = Pin(18, Pin.IN, Pin.PULL_DOWN)
line_sensor3 = Pin(17, Pin.IN, Pin.PULL_DOWN)
line_sensor4 = Pin(16, Pin.IN, Pin.PULL_DOWN)

sensors = [
    ("line_sensor1", line_sensor1),
    ("line_sensor2", line_sensor2),
    ("line_sensor3", line_sensor3),
    ("line_sensor4", line_sensor4),
]

print("Line sensor test started.")
print("Move each sensor over the line to verify it triggers.")

last_state = None

while True:
    active = [name for name, sensor in sensors if sensor.value()]
    state = ", ".join(active) if active else "none"

    # Print only when state changes to keep serial output readable.
    if state != last_state:
        print("Active:", state)
        last_state = state

    sleep(0.05)
