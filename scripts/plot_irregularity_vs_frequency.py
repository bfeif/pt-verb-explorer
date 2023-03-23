import os.path
import ujson as json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
HOME = '.'
DATA_FOLDER = os.path.join(HOME, 'data')
FOCUS_VERBS = ["ser", "dar", "andar", "chegar"]
verb_pt_en_translations = json.load(open(os.path.join(DATA_FOLDER, 'verb-list', 'verbs_pt_en.json')))


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
print(verb_df.head())
hierarchical_index_mapper = {
    "level_0": "infinitive",
    "level_1": "mood",
    "level_2": "tense",
    "level_3": "subject"}
verb_df = verb_df.reset_index().rename(hierarchical_index_mapper, axis=1)
verb_agg = verb_df.groupby(
    'infinitive'
).agg(
    frequency=("term_frequency", "sum"),
    irregularity=("is_irregular", "mean")
).sort_values(by='frequency', ascending=False).reset_index()
verb_agg['frequency_rank'] = np.arange(1, len(verb_agg) + 1, 1)

# add english translations
print(verb_agg.head())
verb_agg['infinitive_en'] = verb_agg['infinitive'].apply(lambda x: verb_pt_en_translations[x])
verb_agg['hover_string'] = verb_agg['infinitive'] + ' (' + verb_agg['infinitive_en'] + ')'

# plot verb frequency vs irregularity
verb_agg.plot(kind='scatter', x="frequency", y="irregularity")
focus_verb_mask = verb_agg["infinitive"].isin(FOCUS_VERBS)
verb_agg["marker_string"] = None
verb_agg.loc[focus_verb_mask, "marker_string"] = verb_agg.loc[focus_verb_mask, "hover_string"]
fig = go.Figure()
fig.add_trace(go.Scatter(
    mode="markers+text",
    x=verb_agg["frequency"],
    y=verb_agg["irregularity"],
    text=verb_agg['marker_string'],
    hovertext=verb_agg["hover_string"],
    marker=dict(color="LightSeaGreen"),
))
fig.update_layout(title_text='Verb Frequency vs Irregularity, Brazilian Portuguese')
fig.update_traces(textposition='top right')
fig.update_xaxes(
    type="log",
    range=[-3.5, 0],
    title='Verb Frequency'
)
fig.update_yaxes(
    range=[-0.05, 1],
    title='Verb Irregularity'
)
fig.show()
fig.write_json('verb_frequency_vs_irregularity.json')

# plot verb frequency vs rank
fig = go.Figure()
fig.add_trace(go.Scatter(
    mode="markers+text",
    x=verb_agg["frequency_rank"],
    y=verb_agg["frequency"],
    text=verb_agg['marker_string'],
    hovertext=verb_agg["hover_string"],
    marker=dict(color="LightSeaGreen"),
))
fig.update_layout(title_text='Verb Frequency vs Rank, Brazilian Portuguese')
fig.update_traces(textposition='top right')
fig.update_xaxes(title='Rank')
fig.update_yaxes(title='Frequency')
fig.show()
fig.write_json('verb_rank_vs_frequency.json')