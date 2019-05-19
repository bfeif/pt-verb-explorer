import os.path
import ujson as json
import pandas as pd
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
plt.scatter(df_rank_irreg['rank'], df_rank_irreg['irregularity'])
plt.xlabel('Verb Frequency of Usage (Ordinal)')
plt.ylabel('Verb Irregularity')
plt.title('Portuguese Verb Conjugation Irregularity')
plt.show()