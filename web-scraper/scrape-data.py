import os
import requests
from bs4 import BeautifulSoup
import ujson as json
HOME = '../'
VERB_JSON_LOCATION = 'data/verb-jsons'
TOP_VERB_LIST_LOCATION = 'data/verb-list/50_top_verbs.json'
VERB_JSON_FILENAME = 'verbo_{}.json'
IMPERATIVO_TEMPOS = ['Imperativo Afirmativo', 'Imperativo Negativo']
BASE_URL = 'https://www.conjugacao.com.br/verbo-'
SUBJECT_LOOKUP = {
	'eu': 'eu',
	'eles': 'eles',
	'ele': 'ele',
	'nós': 'nós',
	'vós': 'vós',
	'tu': 'tu',
	'você': 'você',
	'vocês': 'vocês',
	'que eu': 'eu',
	'que eles': 'eles',
	'que ele': 'ele',
	'que nós': 'nós',
	'que vós': 'vós',
	'que tu': 'tu',
	'quando eu': 'eu',
	'quando eles': 'eles',
	'quando ele': 'ele',
	'quando nós': 'nós',
	'quando vós': 'vós',
	'quando tu': 'tu',
	'se eu': 'eu',
	'se eles': 'eles',
	'se ele': 'ele',
	'se nós': 'nós',
	'se vós': 'vós',
	'se tu': 'tu'
}


def get_page(url):
	'''Get a webpage given a url; return BeautifulSoup object'''
	response = requests.get(url)
	page = BeautifulSoup(response.text, "html5lib")
	return page


def preprocess_verb_string(verb_name):
	'''function that strips portuguese-specific special characters from the verb-string'''
	return verb_name.replace('ç', 'c').replace('ô', 'o')


def dic_conjugation(conjugation, tense_title):
	'''make one conjugation into a dictionary'''
	if tense_title == 'Imperativo Afirmativo':
		subject_index = 1
		verb_index = 0
	elif tense_title == 'Imperativo Negativo':
		subject_index = 2
		verb_index = 1
	else:
		subject_index = 0
		verb_index = 1
	conjugation_parsed = conjugation.find_all('span')
	conjugation_subject = SUBJECT_LOOKUP[conjugation_parsed[subject_index].string]
	conjugation_instance = conjugation_parsed[verb_index]
	conjugation_verb = conjugation_instance.string
	conjugation_irregular = len(conjugation_instance['class']) - 1
	return (conjugation_subject, {'conjugation': conjugation_verb, 'irregular': conjugation_irregular})


def dic_tense(mood_tense, mood_title):
	'''make one tense of a mood (e.g. 'presente' of 'indicativo') into a dictionary'''

	# get the title of the tense
	# possible values: eg. [affirmative, negative] for imperative
	tense_title = mood_tense.h4.string

	# parse the conjugations
	conjugations = mood_tense.p.span.findChildren('span', recursive=False)
	conjugations = conjugations if tense_title not in IMPERATIVO_TEMPOS else conjugations[1:]

	# parse the conjugation set
	conjugations_parsed = dict([dic_conjugation(conjugation, tense_title)
								for conjugation in conjugations])

	# return
	return tense_title, conjugations_parsed


def dic_mood(bs4_tense_section):
	'''make a bs4 tense section a freaking normal data structure cus screw bs4'''

	# get the title of the mood
	# possible values: [Indicativo, Subjuntivo, Imperativo]
	mood_title = bs4_tense_section.find("h3", {"class": "modoconjuga"}).string

	# Get all the tenses of the mood into a list of tags
	# Possible values: eg. [affirmative, negative] for imperative
	mood_tenses = bs4_tense_section.find_all(
		"div", {"class": "tempo-conjugacao"})

	# Parse the mood tenses
	mood_tenses_parsed = dict([dic_tense(mood_tense, mood_title)
							   for mood_tense in mood_tenses])

	# Return
	return mood_title, mood_tenses_parsed


def scrape_verb(verb_string, dump=True):
	'''get all the conjugations for a verb'''

	# Get the url for querying
	url = BASE_URL + preprocess_verb_string(verb_string) + '/'

	# Get the page
	page = get_page(url)

	# Get all the conjugation 'moods'
	all_data = page.find_all("div", {"class": "tempos"})

	# We only care about the first three sets: indicativo, subjuntivo, imperativo
	moods_unparsed = all_data[:3]

	# Parse that sheit baby!
	moods_parsed = dict([dic_mood(mood) for mood in moods_unparsed])

	# Output test
	if dump:
		dump_verb(verb_string, moods_parsed)


def dump_verb(verb_string, verb_conjugation_set):
	'''save the verb data'''

	# You know it
	print('Saving data for verb {}...'.format(verb_string))
	path = os.path.join(HOME, VERB_JSON_LOCATION, VERB_JSON_FILENAME.format(verb_string))
	json.dump(verb_conjugation_set, open(path, 'w'))


def scrape_verbs(verbs_to_scrape, dump=True):
	'''Scrape all the verbs'''

	# Set up the folder structure if necessary
	path = os.path.join(HOME, VERB_JSON_LOCATION)
	if not os.path.exists(path):
		os.mkdir(path)

	# Scrape all the verbs
	for verb in verbs:
		print('Collecting data for verb {}...'.format(verb))
		scrape_verb(verb)


# main method
if __name__ == "__main__":

	# Verbs to do shit for
	verbs = json.load(open(os.path.join(HOME, TOP_VERB_LIST_LOCATION), 'r'))

	# run
	scrape_verbs(verbs)