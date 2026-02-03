from machine import ADC, Pin, I2C

print("start")

line_sensor1 = Pin(16, Pin.IN, Pin.PULL_DOWN)
line_sensor2 = Pin(17, Pin.IN, Pin.PULL_DOWN)
line_sensor3 = Pin(18, Pin.IN, Pin.PULL_DOWN)
line_sensor4 = Pin(19, Pin.IN, Pin.PULL_DOWN)


while True:
    sensor1 = line_sensor1.value()
    sensor2 = line_sensor2.value()
    sensor3 = line_sensor3.value()
    sensor4 = line_sensor4.value()
    if sensor1:
        print(1)
    if sensor2:
        print(2)
    if sensor3:
        print(3)
    if sensor4:
        print(4)
