import os
import ujson as json
from verb_table_builder import build_verb_table
from web_scraper import scrape_data
HOME = '.'
TOP_VERB_LIST_LOCATION = 'data/verb-list/50_top_verbs.json'

# main method
if __name__ == "__main__":

    # Load the verbs to build verb table for
    verbs = json.load(open(os.path.join(HOME, TOP_VERB_LIST_LOCATION), 'r'))
    
    # Do the data collecting/scraping
    scrape_data.scrape_verbs(verbs)

    # build the verb table
    conjs_verb_table, irregs_verb_table = build_verb_table.build_verb_table(verbs)