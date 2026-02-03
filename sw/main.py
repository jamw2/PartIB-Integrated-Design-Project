from main_code import drive_forward, navigate, turn_left, turn_right


time_constant = 2  # time to rotate 90 degrees at 50% power
# drive_forward(time_constant)
# turn_left(time_constant)
route = [
    "SC",
    "LT",
    "SL",
    "RT",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SR",
    "SC",
    "R",
    "SR",
    "R",
    "SC",
    "SL",
    "SL",
    "SL",
    "SL",
    "SL",
    "SL",
    "R",
    "SL",
    "L",
    "ST",
]
print("start")
drive_forward(time_constant)
print("started")
navigate(route)
drive_forward(time_constant)
