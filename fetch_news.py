from _config import PATH
from feed_utils import FeedEntry

import re
import json
import feedparser
import datetime



now = datetime.datetime.now()


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


# example on how to create entry objects for every current feed entry
for i in range(len(guardian_feed)):


	test_entry = FeedEntry(
		now.date(),
		"test",
		get_headlines(guardian_feed)[i],
		get_summaries(guardian_feed)[i],
		get_tags(guardian_feed)[i]
		)


	print(test_entry.title)
	print('\n')
	print(test_entry.get_summary)
	print('\n')
	print(test_entry.tags)
	print('\n')
	print('\n')

