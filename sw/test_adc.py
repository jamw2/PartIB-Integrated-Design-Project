from machine import ADC, Pin
from utime import sleep

#Set the LED pin and configuration
adc_pin = 28
adc = ADC(Pin(adc_pin))

#Continiously update the LED value and print said value
while True:
  adc_value = adc.read_u16()
  dist = adc_value * 5200 / 65535
  # print distance in mm
  print(dist)
  sleep(1)