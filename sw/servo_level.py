import machine
from machine import Pin, PWM
from utime import sleep_ms

# Servo setup
SERVO_PIN = 13
SERVO_FREQ_HZ = 50

# Level behaviour (matches robot.py mapping: duty_u16(int(16000 * level / 100)))
START_LEVEL = 15
MIN_LEVEL = 10
MAX_LEVEL = 90

# Buttons (update UP/DOWN pins when wiring is final)
LEVEL_UP_PIN = 16
LEVEL_DOWN_PIN = 19
EMERGENCY_STOP_PIN = 22  # same as main robot emergency stop button

POLL_INTERVAL_MS = 20


def level_to_duty(level):
    return int(16000 * level / 100)


def apply_level(servo, level):
    duty = level_to_duty(level)
    servo.duty_u16(duty)
    print("Servo level:", level)


def run():
    servo = PWM(Pin(SERVO_PIN))
    servo.freq(SERVO_FREQ_HZ)

    button_up = Pin(LEVEL_UP_PIN, Pin.IN, Pin.PULL_UP)
    button_down = Pin(LEVEL_DOWN_PIN, Pin.IN, Pin.PULL_UP)
    emergency_stop = Pin(EMERGENCY_STOP_PIN, Pin.IN, Pin.PULL_DOWN)

    level = START_LEVEL
    apply_level(servo, level)

    prev_up = 0
    prev_down = 0

    while True:
        # Highest priority: emergency stop
        if emergency_stop.value():
            servo.duty_u16(0)
            servo.deinit()
            print("EMERGENCY STOP pressed. Resetting...")
            machine.reset()

        up_now = not button_up.value()
        down_now = not button_down.value()

        # Rising edge on UP button
        if up_now and not prev_up:
            if level < MAX_LEVEL:
                level += 1
                apply_level(servo, level)
            else:
                print("Servo level:", level)

        # Rising edge on DOWN button
        if down_now and not prev_down:
            if level > MIN_LEVEL:
                level -= 1
                apply_level(servo, level)
            else:
                print("Servo level:", level)

        prev_up = up_now
        prev_down = down_now
        sleep_ms(POLL_INTERVAL_MS)


if __name__ == "__main__":
    run()

