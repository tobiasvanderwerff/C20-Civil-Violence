import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

filename = "Rebellion exp1-table.csv"		# name of data file

# delete the first 6 lines of a table file
def clean_netlogo_table(filename):
	with open(filename) as f, open("temp.txt", "w") as out:
		if "BehaviorSpace results" not in f.readline(): return

		to_delete = []
		for line in range(5): 	# skip first 6 lines of table data
			to_delete.append(next(f))
		for line in f:			# append rest of lines to temp file
			out.write(line)
	os.remove(filename)
	os.rename("temp.txt", filename)

# load relevant data
def load():
	# clean table
	clean_netlogo_table(filename)

	# load data by file name
	data = pd.read_csv(filename, low_memory=False)
	data = data[['[run number]', '[step]', 'government-legitimacy', 'sm-response-rate', 'cop-response-rate', 'count agents with [not active? and jail-term = 0]', 'count agents with [jail-term > 0]', 'count agents with [active?]']]
	data = data.rename(columns={'[run number]': 'run', '[step]': 'step', 'count agents with [not active? and jail-term = 0]': 'quiet', 'count agents with [jail-term > 0]': 'jailed', 'count agents with [active?]': 'active'}, errors="raise")		# rename the long column names
	data.columns = [column.replace("-", "_") for column in data.columns]		# example: government-legitimacy becomes government_legitimacy
	print(data.info())

	return data

# filter data relevant for experiment 1 for conditions (runs) 1-4 as described in the report
def filter_ex1():
	data = load()

	# query for the used variable settings
	cond1 = data.query('government_legitimacy == "0.88" and sm_response_rate == "50" and cop_response_rate == "50"')
	cond2 = data.query('government_legitimacy == "0.82" and sm_response_rate == "50" and cop_response_rate == "50"')
	cond3 = data.query('government_legitimacy == "0.82" and sm_response_rate == "85" and cop_response_rate == "50"')
	cond4 = data.query('government_legitimacy == "0.82" and sm_response_rate == "50" and cop_response_rate == "80"')
	conds = [cond1, cond2, cond3, cond4]

	# average the 10 runs down to 1 run by grouping the steps together
	conds = [cond.groupby([cond.step]).mean() for cond in conds]

	# drop columns not needed anymore
	conds = [cond.drop(columns=['run', 'government_legitimacy', 'sm_response_rate', 'cop_response_rate']) for cond in conds]

	print(conds[0].info())

	return conds

def plotting():
	conds = filter_ex1()

	f, axes = plt.subplots(2, 2)	# dimension of subplot is 2x2
	for i, cond in enumerate(conds):
		sns.lineplot(data=cond, ax=axes[i%2, i//2])
	f.savefig("plot" + filename + ".pdf")

plotting()
