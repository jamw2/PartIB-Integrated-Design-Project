# LT - left at T junction
# RT - right at T junction
# SL - straight on when a branch appears on the left
# SR - straight on when a branch appears on the right
# L - left at a branch
# R - right at a branch
# ST - stop at T junction
# SC - straight on at crossroads

start_route = ["LT","SL","LT","ST"]

bay1_rackA_lower = ["SR"]
bay1_rackA_higher = ["SR","SR","SR","SR","SR","SR","SR","SC","R","RT"]
bay1_rackB_lower = ["R","SR","SR","SR","LT"]
bay1_rackB_higher = ["SR","SR","SR","SR","SR","SR","SR","SC","R","LT"]
rackA_lower_bay2 = ["L","R","ST"]
bay2_rackA_lower = ["LT","RT"]
bay2_rackA_higher = ["LT","RT","SR","SR","SR","SR","SR","SR","SC","R","RT"]
rackA_higher_bay1 = ["L","LT","SC","SL","SL","SL","SL","SL","SL","SL","ST"]
rackA_higher_bay2 = ["L","LT","SC","SR","SL","SL","SL","SL","SL","L","R","ST"]
rackA_higher_bay3 = ["L","RT","SC","SR","SR","SR","SR","SR","SR","R","L","ST"]
rackA_higher_bay4 = ["L","RT","SC","SR","SR","SR","SR","SR","SR","SR","ST"]