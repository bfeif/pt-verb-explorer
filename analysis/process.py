import os.path
import ujson as json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
HOME = '..'
DATA_FOLDER = os.path.join(HOME, 'data')

# load the ranked list of all verbs
verbs_ranked = pd.read_csv(os.path.join(DATA_FOLDER, 'summary', 'top_50_verbs_frame.csv'), index_col=0)

# make a dataframe for each verb
dfs = []
irregular_statistic = []
for verb in verbs_ranked.index:
	verbfile = os.path.join(DATA_FOLDER, 'verb_data', 'verbo_{}.json'.format(verb))
	verb_dict = json.load(open(verbfile))
	reformed = {(verb, outerKey, innerKey): values for outerKey, innerDict in verb_dict.items() for innerKey, values in innerDict.items()}
	df = pd.DataFrame.from_dict(reformed, orient='index')
	df.index.names = ['verb', 'tense', 'subject']
	dfs.append(df)
	irregular_statistic.append((verb, df.mean()['irregular']))

# get the summary for each verb
irregular_statistic = pd.DataFrame(irregular_statistic)
irregular_statistic.set_index(0, inplace=True)
irregular_statistic.columns = ['irregularity']

# merge the irregularity with rank
df_rank_irreg = pd.concat([verbs_ranked, irregular_statistic], axis=1)
df_rank_irreg = df_rank_irreg.drop(labels=['pôr', 'vir', 'sair'], axis=0)
df_rank_irreg['irregularity_cdf'] = np.cumsum(df_rank_irreg['irregularity'])/np.sum(df_rank_irreg['irregularity'])

# plot a normal plot and a cdf
for i in ['', ' CDF']:
	plt.rcParams["figure.figsize"] = (10, 7)
	title = 'Portuguese Verb Conjugation Irregularity' + i
	ylabel = 'Verb Irregularity'
	ylabel = ylabel + ' (cumulative)' if 'CDF' in i else ylabel
	if 'CDF' in i:
		tick_locations = [0] + list(df_rank_irreg['rank'] + 1)
		tick_labels = [' '] + list(df_rank_irreg.index)
		x = tick_locations
		y = [0] + list(df_rank_irreg['irregularity_cdf'])
		plt.plot(x, y)
	else:
		x = df_rank_irreg['rank']
		y = df_rank_irreg['irregularity']
		tick_locations = list(df_rank_irreg['rank'])
		tick_labels = df_rank_irreg.index
		plt.scatter(x,y)
	plt.xlabel('Verb, Ordered by Frequency of Usage')
	plt.xticks(tick_locations, tick_labels, rotation=90)
	plt.ylabel(ylabel)
	plt.title(title)
	plt.tight_layout()
	plt.show()