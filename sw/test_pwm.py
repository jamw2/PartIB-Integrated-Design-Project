from machine import Pin, PWM
from utime import sleep


def test_pwm():
    pwm_pin_no = 13  # Pin 15  gp13
    pwm_pin = PWM(Pin(pwm_pin_no))
    pwm_pin.freq(50)

    level = 20  # 15-85
    direction = -1  # 1=up, -1=down

    # while True:
    #     # PWM the specified pin
    #     u16_level = int(16000 * level / 100)
    #     pwm_pin.duty_u16(u16_level)

    #     # update level and sleep
    #     print(f"Level={level}, u16_level={u16_level}, direction={direction}")
    #     level += direction
    #     if level == 50:
    #         direction = -1
    #     elif level == 10:
    #         direction = 1
    #     sleep(0.1)

    u16_level = int(16000 * level / 100)
    pwm_pin.duty_u16(u16_level)


if __name__ == "__main__":
    test_pwm()
