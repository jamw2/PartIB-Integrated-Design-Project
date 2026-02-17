from machine import ADC, Pin
from utime import sleep
from robot import robot

bot = robot()

def test():
    bot.open()
    sleep(1)
    # Set the LED pin and configuration
    adc_pin = 28
    adc = ADC(Pin(adc_pin))
    bot.close()
    sleep(1)
    print(bot.read_reel())
    # Continiously update the LED value and print said value
    # while True:
    #     # adc_value = adc.read_u16()
    #     # dist = adc_value  # * 5200 / 65535
    #     # # print distance in mm
    #     # print(dist)
    #     print(bot.read_reel())
    #     sleep(1)


test()
