from test_motor import Motor
from utime import sleep

motor3 = Motor(dirPin=4, PWMPin=5)
motor4 = Motor(dirPin=7, PWMPin=6)


def turn_left(time):
    motor3.off()
    motor4.Forward()
    sleep(time)
    motor4.off()


def turn_right(time):
    motor3.Forward()
    motor4.off()
    sleep(time)
    motor3.off()


def rotate_left(time):
    motor3.Reverse()
    motor4.Forward()
    sleep(time / 2)
    motor3.off()
    motor4.off()


def rotate_right(time):
    motor3.Forward()
    motor4.Reverse()
    sleep(time / 2)
    motor3.off()
    motor4.off()


def drive_forward(time):
    motor3.Forward()
    motor4.Forward()
    sleep(time)
    motor3.off()
    motor4.off()


drive_forward(2)
