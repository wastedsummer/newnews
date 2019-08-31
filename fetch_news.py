from _config import PATH
from feed_utils import FeedEntry

import re
import json
import feedparser
import datetime
import numpy as np

import math_utils



now = datetime.datetime.now()


with open(PATH + 'sources.json') as json_file:  
    sources = json.load(json_file)




def get_headlines(feed):
	return [feed['entries'][i]['title'] for i in range(len(feed['entries']))]

def get_summaries(feed):
	return [feed['entries'][i]['summary'] for i in range(len(feed['entries']))]

def get_tags(feed):
	try:
		return [feed['entries'][i]['tags'] for i in range(len(feed['entries']))]
	except KeyError:
		# print("No tags available...\n")
		return [[{None}] for i in range(len(feed['entries']))]


# test

# for source in sources.keys():
guardian_feed = feedparser.parse(sources['theguardian'])
# nytimes_feed = feedparser.parse(sources['newyorktimes'])
nytimes_feed = feedparser.parse(sources['newyorktimes'])

aljazeera_feed = feedparser.parse(sources['bbc'])




##############test embeddings
import nltk
# nltk.download('punkt')

import torch
from models import InferSent






model_version = 2
MODEL_PATH = 'encoder/infersent%s.pkl' % model_version
hyperparameters = {'bsize': 64, 'word_emb_dim': 300, 'enc_lstm_dim': 2048,
                'pool_type': 'max', 'dpout_model': 0.0, 'version': model_version}
model = InferSent(hyperparameters)
model.load_state_dict(torch.load(MODEL_PATH))
use_cuda = False
model = model.cuda() if use_cuda else model
W2V_PATH = 'GloVe/glove.840B.300d.txt' if model_version == 1 else 'fastText/crawl-300d-2M.vec'
model.set_w2v_path(W2V_PATH)
model.build_vocab_k_words(K=10000)

sentences = []
# example on how to create entry objects for every current feed entry
guardian_entries = [FeedEntry(now.date(),
		get_headlines(guardian_feed)[i],
		get_summaries(guardian_feed)[i],
		get_tags(guardian_feed)[i]) for i in range(len(guardian_feed))]


aljazeera_entries = [FeedEntry(now.date(),
		get_headlines(aljazeera_feed)[i],
		get_summaries(aljazeera_feed)[i],
		get_tags(aljazeera_feed)[i]) for i in range(len(aljazeera_feed))]


nytimes_entries = [FeedEntry(now.date(),
		get_headlines(nytimes_feed)[i],
		get_summaries(nytimes_feed)[i],
		get_tags(nytimes_feed)[i]) for i in range(len(nytimes_feed))]
# print(nytimes_entries)


aljazeera_titles = [entry.get_summary for entry in aljazeera_entries]
nytimes_titles = [entry.get_summary for entry in nytimes_entries]
# print(aljazeera_titles)
# print(nytimes_titles)


# aljazeera_sample_embedding = model.encode(aljazeera_titles[np.random.randint(0,len(aljazeera_titles)-1)])[0]
# aljazeera_sample_embedding = model.encode(aljazeera_titles[0])

# print(aljazeera_sample_embedding[0])

aljazeera_embeddings = model.encode(aljazeera_titles, bsize=64, tokenize=False, verbose=True) 
nytimes_embeddings = model.encode(nytimes_titles, bsize=64, tokenize=False, verbose=True)


r = np.random.randint(0, len(aljazeera_embeddings-1))
aljazeera_sample_embedding = aljazeera_embeddings[r]

# print(len(aljazeera_embeddings))
# print(len(nytimes_embeddings))
min_dist = -1
# closest_index = 0
aljazeera_sample_embedding_normalized = math_utils.normalize(aljazeera_sample_embedding)
for i,embedding in enumerate(nytimes_embeddings):

	current_dist = math_utils.cosine_distance(math_utils.normalize(embedding), aljazeera_sample_embedding_normalized)
	# current_dist = math_utils.euclidean_distance(aljazeera_sample_embedding, embedding)
	print(current_dist)

	print(nytimes_titles[i])
	print(aljazeera_titles[r])
	print("\n")
	if current_dist >= min_dist:
		min_dist = current_dist
		closest_index = i


	# print(current_dist)
print("closest:\n")
print(min_dist)
print(nytimes_titles[closest_index])
print("\n")
print(aljazeera_titles[r])
# print("\n")


_, _ = model.visualize(nytimes_titles[closest_index])
_, _ = model.visualize(aljazeera_titles[r])

# print(nytimes_embeddings[closest_index])
# print("\n")
# print(aljazeera_embeddings[r])

# print(guardian_titles)
# for summary in nytimes_titles:
# 	print(summary)
# 	print("\n")
# print(math_utils.euclidean_distance(np.array([0,0,1]), np.array([1,0,0])))

# embeddings = model.encode(sentences, bsize=64, tokenize=False, verbose=True)
# for i in range(1,len(sentences)):
# 	u = math_utils.normalize(embeddings[i-1])
# 	v = math_utils.normalize(embeddings[i])

# 	print(math_utils.cosine_distance(u,v))
# 	print(sentences[i])
# 	print(embeddings[i])
# 	print("\n")

# for i in range(len(guardian_feed)):


# 	test_entry = FeedEntry(
# 		now.date(),
# 		get_headlines(guardian_feed)[i],
# 		get_summaries(guardian_feed)[i],
# 		get_tags(guardian_feed)[i]
# 		)
# # test
# 	sentences.append(test_entry.title)

	# # print(test_entry.title)
	# print('\n')
	# print(test_entry.get_summary)
	# print('tags:\n')
	# # print(test_entry.tags)
	# # print('\n')
	# print('...............\n')




# # print(embeddings[0])


# import numpy as np

# from random import randint

# idx = randint(0, len(sentences)-1)
# _, _ = model.visualize(sentences[idx])