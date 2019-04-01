from _config import PATH
from feed_utils import FeedEntry

import re
import json
import feedparser


with open(PATH + 'sources.json') as json_file:  
    sources = json.load(json_file)




def get_headlines(feed):
	return [feed['entries'][i]['title'] for i in range(len(feed['entries']))]

def get_summaries(feed):
	return [feed['entries'][i]['summary'] for i in range(len(feed['entries']))]

def get_tags(feed):
	return [feed['entries'][i]['tags'] for i in range(len(feed['entries']))]



# test
guardian_feed = feedparser.parse(sources['theguardian'])

print(guardian_feed['entries'][0].keys())
print('\n')
print(FeedEntry.clear_html(guardian_feed['entries'][0]['summary']))
print('\n')


