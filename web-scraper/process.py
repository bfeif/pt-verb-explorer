import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import ujson as json
HOME = '../'
IMPERATIVO_TEMPOS = ['Imperativo Afirmativo', 'Imperativo Negativo']
BASE_URL = 'https://www.conjugacao.com.br/verbo'

# a function to make one conjugation into a dictionary
def dic_conjugation(conjugation, subject_index=0, verb_index=1):

	# fuck comments babayyyy
	conjugation_parsed = conjugation.find_all('span')
	conjugation_title = conjugation_parsed[subject_index].string
	conjugation_instance = conjugation_parsed[verb_index]
	conjugation_verb = conjugation_instance.string
	conjugation_irregular = len(conjugation_instance['class'])-1
	return (conjugation_title, {'conjugation': conjugation_verb, 'irregular': conjugation_irregular})

# function to make one tense of a mood (e.g. 'presente' of 'indicativo') into a dictionary
def dic_tense(mood_tense):

	# get the title of the tense
	# possible values: eg. [affirmative, negative] for imperative
	tense_title = mood_tense.h4.string

	# parse the conjugations
	conjugations = mood_tense.p.span.findChildren('span', recursive=False)
	conjugations = conjugations if tense_title not in IMPERATIVO_TEMPOS else conjugations[1:]

	# parse the conjugation set
	conjugations_parsed = dict([dic_conjugation(conjugation) for conjugation in conjugations])

	# return
	return tense_title, conjugations_parsed

# function to make a bs4 tense section a freaking normal data structure cus screw bs4
def dic_mood(bs4_tense_section):

	# get the title of the mood
	# possible values: [Indicativo, Subjuntivo, Imperativo]
	mood_title = bs4_tense_section.find("h3", { "class" : "modoconjuga" }).string

	# get all the tenses of the mood into a list of tags
	# possible values: eg. [affirmative, negative] for imperative
	mood_tenses = bs4_tense_section.find_all("div", { "class" : "tempo-conjugacao" })

	# parse the mood tenses
	mood_tenses_parsed = dict([dic_tense(mood_tense) for mood_tense in mood_tenses])

	# return
	return mood_title, mood_tenses_parsed

# get page
def get_page(url):

	# Set the URL you want to webscrape from
	url = 'https://www.conjugacao.com.br/verbo-ir/'

	# Connect to the URL
	response = requests.get(url)

	# Parse HTML and save to BeautifulSoup object
	page = BeautifulSoup(response.text, "html5lib")

	# return BeautifulSoup object
	return page

# function that gets all the conjugations for a verb
def get_verb(verb_string):

	# get the url for querying
	url = BASE_URL + verb_string + '/'

	# get the page
	page = get_page(url)
	
	# get all the conjugation 'moods'
	all_data = page.find_all("div", { "class" : "tempos" })

	# # we only care about the first three sets: indicativo, subjuntivo, imperativo
	# # just gonna index the first 3 from the list 'all_data' here cus I'm lazy af, but this is unsafe!
	# moods_unparsed = all_data[0:2]

	# # parse that sheit baby!
	# moods_parsed = dict([dic_mood(mood) for mood in moods_unparsed])

	# scratch that, just the indicative mood for now
	indicativo_mood = all_data[0]

	# parse that sheit baby!
	title, indicativo_mood_parsed = dic_mood(indicativo_mood)

	# output test
	dump_verb(verb_string, indicativo_mood_parsed)

# save the verb data
def dump_verb(verb_string, verb_conjugation_set):

	# u know it
	path = HOME + 'data/verbo_' + verb_string + '.json'
	json.dump(verb_conjugation_set, open(path, 'w'))

# main method
if __name__ == "__main__":

	# verbs to do shit for
	verbs = json.load(open(HOME + 'data/50_top_verbs.json', 'r'))
	for verb in verbs:
		get_verb(verb)