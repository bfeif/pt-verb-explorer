import os.path
import ujson as json
import pandas as pd
HOME = '..'
DATA_FOLDER = os.path.join(HOME, 'data')

verbfile = os.path.join(DATA_FOLDER, 'verbo_ir.json')
verb = json.load(open(verbfile))


for tense, conjugations in verb.items():
	df = pd.DataFrame.from_dict(conjugations, orient='index')