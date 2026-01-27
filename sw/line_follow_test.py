from utime import sleep
from main_code import drive_forward, navigate

time_constant = 1 # time to rotate 90 degrees at 50% power

route = ["LT","SL","RT","SR","SR","SR","SR","SR","SR","SC","SR","SC","SL","SL","SL","SL","SL","SL","R","SL","R","ST"]

drive_forward(time_constant)
navigate(route)
drive_forward(time_constant)