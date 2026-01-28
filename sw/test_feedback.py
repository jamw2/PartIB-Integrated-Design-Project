from machine import Pin, PWM, ADC
from utime import sleep


def test_pwm():
    pwm_pin_no = 15  # Pin 15  gp13
    pwm_pin = PWM(Pin(pwm_pin_no), 100)

    adc_pin = 28
    adc = ADC(Pin(adc_pin))
    level = 15  # 0-100
    direction = 1  # 1=up, -1=down

    while True:
        # PWM the specified pin
        u16_level = int(16000 * level / 100)
        pwm_pin.duty_u16(u16_level)

        # update level and sleep
        # print(f"Level={level}, u16_level={u16_level}, direction={direction}")
        level += direction
        if level == 100:
            direction = -1
        elif level == 15:
            direction = 1
        adc_value = adc.read_u16()
        dist = adc_value
        print(dist)  # 0 to 60000

        sleep(0.5)


if __name__ == "__main__":
    test_pwm()
