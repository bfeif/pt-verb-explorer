import os
import ujson as json
import pandas as pd
HOME = os.path.abspath('.')  # os.environ['VERB_TABLE_BUILDER_HOME']
VERB_JSON_LOCATION = 'data/verb-jsons'
TOP_VERB_LIST_LOCATION = 'data/verb-list/50_top_verbs.json'
VERB_JSON_FILENAME = 'verbo_{}.json'
VERB_TABLE_LOCATION = 'data/verb-tables'
VERB_TABLE_NAME = 'verb_table_{}.csv'


def load_verb_json_data(verb_strings):
    verb_data = {verb_string: json.load(open(os.path.join(HOME, VERB_JSON_LOCATION, VERB_JSON_FILENAME.format(verb_string)), 'r')) for verb_string in verb_strings}
    return verb_data


def build_verb_table(verb_list, save=True):
    """Function that builds the verb table"""

    print('Building verb tables...')

    # load verb data from jsons
    verbs = load_verb_json_data(verb_list)

    # prepare for the multiindex
    conjs_dfs  = []
    irregs_dfs = []
    for verb_string, verb in verbs.items():
        conjs_multified = {}
        irregs_multified = {}
        for mood, i in verb.items():
            for tense, j in i.items():
                for subject, k in j.items():
                    key = (mood, tense, subject)
                    conjs_multified[key] = {verb_string: k['conjugation']}
                    irregs_multified[key] = {verb_string: k['irregular']}
        conjs_df  = pd.DataFrame.from_dict(conjs_multified, orient='index', columns=[verb_string])
        irregs_df = pd.DataFrame.from_dict(irregs_multified, orient='index', columns=[verb_string])
        conjs_dfs.append(conjs_df)
        irregs_dfs.append(irregs_df)
    
    # create the verb tables from the lists of dfs
    conjs_verb_table  = pd.concat(conjs_dfs, axis=1)
    irregs_verb_table = pd.concat(irregs_dfs, axis=1)

    # save them out
    if save:
        new_directory_path = os.path.join(HOME, VERB_TABLE_LOCATION)
        if not os.path.exists(new_directory_path):
            os.mkdir(new_directory_path)
        for name, table in zip(['conjugations', 'irregularities'], [conjs_verb_table, irregs_verb_table]):
            table.to_csv(os.path.join(HOME, VERB_TABLE_LOCATION, VERB_TABLE_NAME.format(name)))

    # return
    return conjs_verb_table, irregs_verb_table


# main method
if __name__ == "__main__":

    # Verbs to do shit for
    verbs_to_load = json.load(open(os.path.join(HOME, TOP_VERB_LIST_LOCATION), 'r'))
    
    # build the verb table
    conjs_verb_table, irregs_verb_table = build_verb_table(verbs_to_load)
