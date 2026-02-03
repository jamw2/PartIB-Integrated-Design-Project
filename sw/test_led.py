from machine import Pin
from utime import sleep

# from main.py
# blue_led = Pin(10, Pin.OUT)
# green_led = Pin(11, Pin.OUT)
# red_led = Pin(12, Pin.OUT)
# yellow_led = Pin(14, Pin.OUT)


def test_led():
    led_pin = 14  # Pin 28 = GP28 (labelled 34 on the jumper)
    led = Pin(led_pin, Pin.OUT)

    while True:
        # Flash the LED
        print("Flashing LED")
        led.value(1)
        sleep(0.5)
        led.value(0)
        sleep(0.5)


if __name__ == "__main__":
    test_led()
