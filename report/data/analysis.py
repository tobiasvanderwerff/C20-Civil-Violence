import pandas as pd

data = pd.read_csv("navigation_strategies-table.csv", low_memory=False)
data = data.query('`[step]` == 800')
data = data[['escape-strategy', 'movement-type', 'hunt-strategy', 'sinus-frequency', 'sinus-amplitude', 'catch-rate', 'mean-catch-duration', 'time-between-lock-ons']]
data.columns = [column.replace("-", "_") for column in data.columns]
data = data.query('sinus_amplitude == 2 and sinus_frequency == 25')

#d1 = data.query('escape_strategy == "default" and movement_type == "default" and hunt_strategy == "default"')
#d1['mean_catch_duration'].mean()
#d1['mean_catch_duration'].std()

# escape_strategy
# "default" "turn 90 deg" "sacrifice" "sprint"

# hunt_strategy
# "default" "proportional nav"

# movement_type
# "default" "sinus"

# esc mov hunt m1_av m1_std m2_av m2_std m3_av m3_std

pre = {
	'escape_strategy':
	[["default"] * 4][0] +
	[["turn 90 deg"] * 4][0] +
	[["sacrifice"] * 4][0] +
	[["sprint"] * 4][0],
	'movement_type':
	[["default"] * 2 +
	["sinus"] * 2][0] * 4,
	'hunt_strategy': ["default", "proportional nav"] * 2 * 4,
}

# 16x1 <- get_stat("catch_rate", "avg")
def get_stat(measure: str, stat: str) -> list:
	vec = []	
	for i in range(0, 16):
		if stat == "avg":
			vec.append(
			data [
			(data.escape_strategy == pre["escape_strategy"][i]) &
			(data.movement_type == pre["movement_type"][i]) &
			(data.hunt_strategy == pre["hunt_strategy"][i])
			][measure].mean())
		elif stat == "std":
			vec.append(
			data [
			(data.escape_strategy == pre["escape_strategy"][i]) &
			(data.movement_type == pre["movement_type"][i]) &
			(data.hunt_strategy == pre["hunt_strategy"][i])
			][measure].std())
		elif stat == "non":
			vec.append(
			data [
			(data.escape_strategy == pre["escape_strategy"][i]) &
			(data.movement_type == pre["movement_type"][i]) &
			(data.hunt_strategy == pre["hunt_strategy"][i])
			][measure])
	return vec
	
out = {
	'escape_strategy':
	[["default"] * 4][0] +
	[["turn 90 deg"] * 4][0] +
	[["sacrifice"] * 4][0] +
	[["sprint"] * 4][0],
	'movement_type':
	[["default"] * 2 +
	["sinus"] * 2][0] * 4,
	'hunt_strategy': ["default", "proportional nav"] * 2 * 4,
	'catch_rate_avg': get_stat("catch_rate", "avg"),
	'catch_rate_std': get_stat("catch_rate", "std"),
	'catch_duration_avg': get_stat("mean_catch_duration", "avg"),
	'catch_duration_std': get_stat("mean_catch_duration", "std"),
	'time_between_lock_ons_avg': get_stat("time_between_lock_ons", "avg"),
	'time_between_lock_ons_std': get_stat("time_between_lock_ons", "std")
}

df = pd.DataFrame(out)

# df.to_csv("analysis.csv", index = False)
# print(df.head(16))

import numpy as np
import matplotlib.pyplot as plt

## BOX PLOT
# default escape. catch rate: four boxes in one box-plot
catch_rate = get_stat("catch_rate", "non")[0:4]
boxplot = catch_rate[0].values.tolist()
fig2, ax2 = plt.subplots()
ax2.set_title('Escape: default. Catch rate')
ax2.boxplot(boxplot)
plt.show()

## BAR PLOT

# Default escape
# Catch rates
fig, (ax1, ax2, ax3) = plt.subplots(1, 3)
fig.suptitle('Predator statistics. Prey strategy: default.')
x = ['Move: default\n Nav: default', 'Move: default\n Nav: prop', 'Move: sinus\n Nav: default', 'Move: sinus\n Nav: prop']

# Catch rate
y = df["catch_rate_avg"][0:4].values.tolist()
e = df["catch_rate_std"][0:4].values.tolist()
ax1.set_title('Catch rate')
ax1.bar(x, y, yerr=e, capsize=8)

# Catch duration
y = df["catch_duration_avg"][0:4].values.tolist()
e = df["catch_duration_std"][0:4].values.tolist()
ax2.set_title('Catch duration')
ax2.bar(x, y, yerr=e, capsize=8)

# Lock-on time
y = df["time_between_lock_ons_avg"][0:4].values.tolist()
e = df["time_between_lock_ons_std"][0:4].values.tolist()
ax3.set_title('Time between lock-ons')
ax3.bar(x, y, yerr=e, capsize=8)

plt.show()


########################## 4 times catch rate

#measure = "catch_rate"
#measure_label = "catch rate"
#measure = "catch_duration"
#measure_label = "ticks"
measure = "time_between_lock_ons"
measure_label = "ticks"

fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharex=True, sharey=True)
fig.suptitle('Time between lock-ons')
x = ['Move: default\n Nav: default', 'Move: default\n Nav: prop', 'Move: sinus\n Nav: default', 'Move: sinus\n Nav: prop']

a = 0
b = 4
y = df[measure + "_avg"][a:b].values.tolist()
e = df[measure + "_std"][a:b].values.tolist()
ax1.set_title('Prey strategy: default')
ax1.set_ylabel(measure_label)
ax1.bar(x, y, yerr=e, capsize=8)
a += 4
b += 4
y = df[measure + "_avg"][a:b].values.tolist()
e = df[measure + "_std"][a:b].values.tolist()
ax2.set_title('Prey strategy: turn 90°')
ax2.bar(x, y, yerr=e, capsize=8)
a += 4
b += 4
y = df[measure + "_avg"][a:b].values.tolist()
e = df[measure + "_std"][a:b].values.tolist()
ax3.set_title('Prey strategy: sacrifice')
ax3.set_ylabel(measure_label)
ax3.bar(x, y, yerr=e, capsize=8)
a += 4
b += 4
y = df[measure + "_avg"][a:b].values.tolist()
e = df[measure + "_std"][a:b].values.tolist()
ax4.set_title('Prey strategy: sprint')
ax4.bar(x, y, yerr=e, capsize=8)

plt.show()



