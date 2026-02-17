# LT - left at T junction
# RT - right at T junction
# SL - straight on when a branch appears on the left
# SR - straight on when a branch appears on the right
# L - left at a branch
# R - right at a branch
# ST - stop at T junction
# SC - straight on at crossroads
# STL - stop at a branch on the left
# STR - stop at a branch on the right
# RL - rotate left
# RR - rotate right

# bay1 = 0
# bay2 = 1
# bay3 = 2
# bay4 = 3

# rackA upper = 0
# rackA lower = 1
# rackB upper = 2
# rackB lower = 3

start_route = ["L", "SL", "L", "STL"]

# [bay][rack]
routes_to_racks = [
    [
        ["SR", "SR", "SR", "SR", "SR", "SR", "SR", "SL", "RR", "R", "R", "RR", "R", "R", "STL"],
        ["SR", "STR"],
        ["SR", "SR", "SR", "SR", "SR", "SR", "SR", "SL", "RR", "R", "R", "RL", "L", "L", "STR"],
        ["R", "SR", "SR", "SR", "L", "STL"],
    ],
    [
        ["L", "R", "SR", "SR", "SR", "SR", "SR", "SR", "SL", "RR", "R", "R", "RR", "R", "R", "STL",],
        ["L", "R", "STR"],
        ["L", "R", "SR", "SR", "SR", "SR", "SR", "SR", "SL", "RR", "R", "R", "RL", "L", "L", "STR"],
        ["R", "SR", "SR", "L", "STL"],
    ],
    [
        ["R","R","SL","SL","SL","SL","SL","SL","SL","RL","L", "L","RR","R","R","STL"],
        ["L", "SL", "SL", "R", "STR"],
        ["R","R","SL","SL","SL","SL","SL","SL","SL","RL","L","L","RL", "L", "L","STR",],
        ["R", "L", "STL"],
    ],
    [
        ["SL", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "RL", "L", "L", "RR", "R", "R", "STL"],
        ["L", "SL", "SL", "SL", "RT", "STR"],
        ["SL", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "RL", "L", "L", "RL", "L", "L", "STR"],
        ["SL", "STL"],
    ],
]

# [rack][bay]
routes_to_bays = [
    [
        ["RL", "L", "L", "RL", "L", "L", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "STL"],
        ["RL", "L", "L", "RL", "L", "L", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "L", "RBR", "STL"],
        ["RL", "L", "L", "RR", "R", "R", "SL", "SR", "SR", "SR", "SR", "SR", "SR", "R", "L", "STL"],
        ["RL", "L", "L", "RR", "R", "R", "SL", "SR", "SR", "SR", "SR", "SR", "SR", "SR", "STL"],
    ],
    [
        ["SL", "STL"],
        ["L", "R", "STL"],
        ["L", "SR", "SR", "R", "STL"],
        ["L", "SR", "SR", "SR", "R", "STL"],
    ],
    [
        ["RR", "R", "R", "RL", "L", "L", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "STL"],
        ["RR", "R", "R", "RL", "L", "L", "SL", "SL", "SL", "SL", "SL", "SL", "SL", "L", "R", "STL"],
        ["RR", "R", "R", "RR", "R", "R", "SL", "SR", "SR", "SR", "SR", "SR", "SR", "R", "L", "STL"],
        ["RR", "R", "R", "RR", "R", "R", "SL", "SR", "SR", "SR", "SR", "SR", "SR", "SR", "STL"],
    ],
    [
        ["R", "SL", "SL", "SL", "LT", "STL"],
        ["R", "SL", "SL", "L", "STL"],
        ["R", "L", "STL"],
        ["SR", "STL"],
    ],
]
