import os.path
import ujson as json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
HOME = '.'
DATA_FOLDER = os.path.join(HOME, 'data')

#################################################
# CREATE VERB CONJUGATION/IRREGULARITY TABLE

# load the ranked list of all verbs
verbs_ranked = pd.read_csv(os.path.join(DATA_FOLDER, 'verb-list', 'top_50_verbs_frame.csv'), index_col=0)

# make a dataframe for each verb
verb_dfs = []
for verb in verbs_ranked.index:
    verbfile = os.path.join(DATA_FOLDER, 'verb-jsons', 'verbo_{}.json'.format(verb))
    verb_dict = json.load(open(verbfile))
    reformed_dict = {(verb, mood, tense, subject): {'conjugation': subject_data["conjugation"],
                                                    'is_irregular': subject_data["irregular"]}
                     for mood, mood_dict in verb_dict.items()
                     for tense, tense_dict in mood_dict.items()
                     for subject, subject_data in tense_dict.items()}
    verb_df = pd.DataFrame.from_dict(reformed_dict, orient='index')
    verb_dfs.append(verb_df)

# concat into one dataframe
verb_irregularity_df = pd.concat(verb_dfs, axis=0)


#################################################
# CREATE VERB FREQUENCY TABLE
subtlex_column_name_mapper = {'Word': 'word', 'FREQcount': 'term_count', 'CDcount': 'document_count'}
verb_frequency_df = pd.read_csv(
    os.path.join(DATA_FOLDER, 'SUBTLEX-BRPOR.no-web.valid-char.csv'),
    delimiter='\t',
    header=0
).rename(
    mapper=subtlex_column_name_mapper,
    axis=1
).set_index(
    'word'
)


#################################################
# JOIN AND ANALYZE

# join and manipulate to a useful format
verb_df = verb_irregularity_df.merge(
    verb_frequency_df["term_count"],
    how="left",
    left_on="conjugation",
    right_index=True
)
verb_df['term_frequency'] = verb_df['term_count'] / verb_df['term_count'].sum()
verb_df['term_frequency'] = verb_df['term_frequency'].fillna(0)
hierarchical_index_mapper = {
    "level_0": "verb",
    "level_1": "mood",
    "level_2": "tense",
    "level_3": "subject"}
verb_df = verb_df.reset_index().rename(hierarchical_index_mapper, axis=1)

# plot verb frequency vs irregularity
verb_df.groupby(
    'verb'
).agg(
    frequency=("term_frequency", "sum"),
    irregularity=("is_irregular", "mean")
).plot(kind='scatter', x="frequency", y="irregularity")
plt.xscale('log')
plt.xlim((10**-4, 10**0))
plt.xlabel('Verb Frequency')
plt.ylabel('Verb Irregularity')
plt.title('Verb Frequency vs Irregularity, Brazilian Portuguese')
plt.show()

# plot verb frequency vs rank
verb_df.groupby(
    'verb'
)["term_frequency"].sum().sort_values(
    ascending=False
).reset_index().reset_index().plot(
    kind='scatter',
    x='index',
    y='term_frequency'
)
plt.xlabel('Rank')
plt.ylabel('Verb Frequency')
plt.title('Verb Frequency vs Rank, Brazilian Portuguese')
plt.show()
plt.show()