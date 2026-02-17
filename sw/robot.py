from test_motor import Motor
from machine import ADC, Pin, I2C, PWM
from libs.VL53L0X.VL53L0X import VL53L0X
from libs.DFRobot_TMF8x01.DFRobot_TMF8x01 import DFRobot_TMF8701
from utime import sleep


class robot:
    def __init__(self,  time_constant=1):
        self.time_constant = time_constant

        # Set up distance sensors
        i2c_bus = I2C(id=0, sda=Pin(20), scl=Pin(21), freq=100000)
        self.tof = DFRobot_TMF8701(i2c_bus=i2c_bus)
        while self.tof.begin() != 0:
            print("   Initialisation failed")
            sleep(0.5)
        print("   Initialisation done.")
        self.tof.start_measurement(
            calib_m=self.tof.eMODE_NO_CALIB, mode=self.tof.eCOMBINE
        )
        self.vl53l0 = VL53L0X(i2c_bus)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[0], 18)
        self.vl53l0.set_Vcsel_pulse_period(self.vl53l0.vcsel_period_type[1], 14)
        self.vl53l0.start()

        # Set up motors
        self.motor3 = Motor(dirPin=4, PWMPin=5)
        self.motor4 = Motor(dirPin=7, PWMPin=6)

        # Set up line sensors
        self.line_sensor1 = Pin(19, Pin.IN, Pin.PULL_DOWN)
        self.line_sensor2 = Pin(18, Pin.IN, Pin.PULL_DOWN)
        self.line_sensor3 = Pin(17, Pin.IN, Pin.PULL_DOWN)
        self.line_sensor4 = Pin(16, Pin.IN, Pin.PULL_DOWN)

        # Set up LEDs
        self.blue_led = Pin(14, Pin.OUT)
        self.green_led = Pin(12, Pin.OUT)
        self.red_led = Pin(11, Pin.OUT)
        self.yellow_led = Pin(10, Pin.OUT)

        # Set up ADC
        self.adc = ADC(Pin(28))
        self.us = ADC(Pin(26))

        # Set up PWM servos
        self.servo1 = PWM(Pin(13))  # level 15 down, 20 up
        self.servo1.freq(50)
        self.servo2 = PWM(Pin(15))  # level 15 open, 20 closed
        self.servo2.freq(50)

    # bouncing between inner edges
    def follow_line(self):
        sensor2 = self.line_sensor2.value()
        sensor3 = self.line_sensor3.value()
        if sensor2 and sensor3:
            self.motor3.Forward()
            self.motor4.Forward()
        elif not sensor2:
            self.motor4.Forward(50)
            self.motor3.Forward()
        # search for line
        else:
            self.motor3.Forward(50)
            self.motor4.Forward()

    def check_junction(self):
        sensor1 = self.line_sensor1.value()
        sensor4 = self.line_sensor4.value()
        if sensor1:
            return "L"
        elif sensor4:
            return "R"
        return False

    # turn pivoting on inside wheel
    def turn_left(self, time):
        self.drive_forward(0.25)
        self.motor3.off()
        self.motor4.Forward()
        sleep(time)
        while not self.line_sensor3.value():
            continue
        self.motor4.off()

    def turn_right(self, time):
        self.drive_forward(0.25)
        self.motor3.Forward()
        self.motor4.off()
        sleep(time)
        while not self.line_sensor2.value():
            continue
        self.motor3.off()

    # rotate around spot
    def rotate_left(self, time):
        self.motor3.Reverse(50)
        self.motor4.Forward(50)
        sleep(time)
        while not self.line_sensor3.value():
            continue
        self.motor3.off()
        self.motor4.off()

    def rotate_right(self, time):
        self.motor3.Forward(50)
        self.motor4.Reverse(50)
        sleep(time)
        while not self.line_sensor2.value():
            continue
        self.motor3.off()
        self.motor4.off()

    def drive_forward(self, time):
        self.motor3.Forward()
        self.motor4.Forward()
        sleep(time)
        self.motor3.off()
        self.motor4.off()

    def reverse(self, time):
        self.motor3.Reverse()
        self.motor4.Reverse()
        sleep(time)
        self.motor3.off()
        self.motor4.off()

    def navigate(self, route):
        for inst in route:
            success = False
            i = 0

            # until next instruction
            while not success:
                junc = self.check_junction()
                while junc is False:
                    junc = self.check_junction()
                    self.follow_line()
                print(inst, junc)
                self.motor3.off()
                self.motor4.off()
                if inst == "SL":
                    if junc == "L":
                        self.drive_forward(self.time_constant * 0.2)
                        success = True
                elif inst == "SR":
                    if junc == "R":
                        self.motor3.off()
                        self.motor4.off()
                        sleep(0.2)
                        self.drive_forward(self.time_constant * 0.2)
                        success = True
                elif inst == "L":
                    if junc == "L":
                        self.turn_left(self.time_constant * 0.3)
                        success = True
                elif inst == "R":
                    if junc == "R":
                        self.turn_right(self.time_constant * 0.3)
                        success = True
                elif inst == "STL":
                    if junc == "L":
                        self.motor3.off()
                        self.motor4.off()
                        success = True
                elif inst == "STR":
                    if junc == "R":
                        self.motor3.off()
                        self.motor4.off()
                        success = True
                elif inst == "RL":
                    if junc == "L":
                        self.drive_forward(0.1)
                        self.rotate_left(self.time_constant*0.3)
                        success = True
                elif inst == "RR":
                    if junc == "R":
                        self.drive_forward(0.1)
                        self.rotate_right(self.time_constant*0.3)
                        success = True
                if not success:
                    self.drive_forward(0.1)

    def read_us(self):
        return self.us.read_u16()

    def read_reel(self):
        adc_value = self.adc.read_u16()
        scaled_voltage = adc_value / 65535
        scaled_voltage = scaled_voltage / 0.72
        if scaled_voltage < 0.1:
            self.blue_led.value(1)
            return 0
        elif scaled_voltage < 0.45:
            self.green_led.value(1)
            return 1
        elif scaled_voltage < 0.94:
            self.red_led.value(1)
            return 2
        self.yellow_led.value(1)
        return 3

    # scans racks until empty one found
    def find_empty(self, rack):
        dist = 0
        for position in range(1, 7):
            if rack == 0 or rack == 3:
                if self.tof.is_data_ready() is True:
                    dist = self.tof.get_distance_mm()
                inst = "STL"
            else:
                dist = self.vl53l0.read()
                inst = "STR"
            if dist == 0 or dist > 200:
                return position
            self.drive_forward(self.time_constant * 0.2)
            self.navigate(inst)
            position += 1
        return position

    def lift(self):
        self.servo1.duty_u16(int(16000 * 29 / 100))

    def lower(self):
        self.servo1.duty_u16(int(16000 * 31 / 100))

    def open(self):
        self.servo2.duty_u16(int(16000 * 11 / 100))

    def close(self):
        self.servo2.duty_u16(int(16000 * 14 / 100))

    def pick_reel(self):
        self.lower()
        self.drive_forward(self.time_constant * 0.5)
        self.lift()
        self.close()
        sleep(0.5)

    def place_reel(self, rack_location):
        if rack_location == 0 or rack_location == 3:
            self.turn_left(self.time_constant * 0.5)
        else:
            self.turn_right(self.time_constant * 0.5)

        self.drive_forward(self.time_constant)

        self.open()
        self.lower()

        self.green_led.value(0)
        self.yellow_led.value(0)
        self.red_led.value(0)
        self.blue_led.value(0)

        self.reverse(self.time_constant)
        if rack_location == 0 or rack_location == 3:
            self.turn_left(self.time_constant * 0.5)
        else:
            self.turn_right(self.time_constant * 0.5)

 
