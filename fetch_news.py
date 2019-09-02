import torch
import json
import feedparser
import datetime
import numpy as np
import re
import pickle
import math_utils

from _config import PATH
from feed_utils import FeedEntry, clear_summary
from models import InferSent



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


# parse feeds
newyorktimes_feed = feedparser.parse(sources['newyorktimes'])
aljazeera_feed = feedparser.parse(sources['bbc'])
bbc_feed = feedparser.parse(sources['bbc'])
guardian_feed = feedparser.parse(sources['theguardian'])
reuters_feed = feedparser.parse(sources['reuters'])




# load infersent model
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
# print(guardian_feed)[0]


# load timeline file
timeline = pickle.load(open( "timeline.p", "rb" ) )



# update timeline (this should remain hardcoded for every single feed because they may vary in their stucture)

# new york times
newyorktimes_titles = [get_headlines(newyorktimes_feed)[i] for i in range(len(newyorktimes_feed))]
newyorktimes_summaries = [clear_summary(get_summaries(newyorktimes_feed)[i]) for i in range(len(newyorktimes_feed))]
newyorktimes_title_embeddings = model.encode(newyorktimes_titles, bsize=64, tokenize=False, verbose=True)  
newyorktimes_summary_embeddings = model.encode(newyorktimes_summaries, bsize=64, tokenize=False, verbose=True)  

newyorktimes_entries = [
	FeedEntry(
		now.date(),
		newyorktimes_titles[i],
		newyorktimes_summaries[i],
		newyorktimes_title_embeddings[i],
		newyorktimes_summary_embeddings[i]) 
	for i in range(len(newyorktimes_feed))]

for entry in newyorktimes_entries:
	if entry.title not in [existing_entry.title for existing_entry in timeline['newyorktimes'][str(now.date())]]:
		timeline['newyorktimes'][str(now.date())].append(entry)
		print("entry appended")
	else:
		print("skipping...already exists")



# aljazeera 
aljazeera_titles = [get_headlines(aljazeera_feed)[i] for i in range(len(aljazeera_feed))]
aljazeera_summaries = [clear_summary(get_summaries(aljazeera_feed)[i]) for i in range(len(aljazeera_feed))]
aljazeera_title_embeddings = model.encode(aljazeera_titles, bsize=64, tokenize=False, verbose=True)  
aljazeera_summary_embeddings = model.encode(aljazeera_summaries, bsize=64, tokenize=False, verbose=True)  

aljazeera_entries = [
	FeedEntry(
		now.date(),
		aljazeera_titles[i],
		aljazeera_summaries[i],
		aljazeera_title_embeddings[i],
		aljazeera_summary_embeddings[i]) 
	for i in range(len(aljazeera_feed))]

for entry in aljazeera_entries:
	if entry.title not in [existing_entry.title for existing_entry in timeline['aljazeera'][str(now.date())]]:
		timeline['aljazeera'][str(now.date())].append(entry)
		print("entry appended")
	else:
		print("skipping...already exists")


# bbc 
bbc_titles = [get_headlines(bbc_feed)[i] for i in range(len(bbc_feed))]
bbc_summaries = [clear_summary(get_summaries(bbc_feed)[i]) for i in range(len(bbc_feed))]
bbc_title_embeddings = model.encode(bbc_titles, bsize=64, tokenize=False, verbose=True)  
bbc_summary_embeddings = model.encode(bbc_summaries, bsize=64, tokenize=False, verbose=True)  

bbc_entries = [
	FeedEntry(
		now.date(),
		bbc_titles[i],
		bbc_summaries[i],
		bbc_title_embeddings[i],
		bbc_summary_embeddings[i]) 
	for i in range(len(bbc_feed))]

for entry in bbc_entries:
	if entry.title not in [existing_entry.title for existing_entry in timeline['bbc'][str(now.date())]]:
		timeline['bbc'][str(now.date())].append(entry)
		print("entry appended")
	else:
		print("skipping...already exists")




# guardian
guardian_titles = [get_headlines(guardian_feed)[i] for i in range(len(guardian_feed))]
guardian_summaries = [clear_summary(get_summaries(guardian_feed)[i]) for i in range(len(guardian_feed))]
guardian_title_embeddings = model.encode(guardian_titles, bsize=64, tokenize=False, verbose=True)  
guardian_summary_embeddings = model.encode(guardian_summaries, bsize=64, tokenize=False, verbose=True)  

guardian_entries = [
	FeedEntry(
		now.date(),
		guardian_titles[i],
		guardian_summaries[i],
		guardian_title_embeddings[i],
		guardian_summary_embeddings[i]) 
	for i in range(len(guardian_feed))]

for entry in guardian_entries:
	if entry.title not in [existing_entry.title for existing_entry in timeline['theguardian'][str(now.date())]]:
		timeline['theguardian'][str(now.date())].append(entry)
		print("entry appended")
	else:
		print("skipping...already exists")




# reuters 
reuters_titles = [get_headlines(reuters_feed)[i] for i in range(len(reuters_feed))]
reuters_summaries = [clear_summary(get_summaries(reuters_feed)[i]) for i in range(len(reuters_feed))]
reuters_title_embeddings = model.encode(reuters_titles, bsize=64, tokenize=False, verbose=True)  
reuters_summary_embeddings = model.encode(reuters_summaries, bsize=64, tokenize=False, verbose=True)  

reuters_entries = [
	FeedEntry(
		now.date(),
		reuters_titles[i],
		reuters_summaries[i],
		reuters_title_embeddings[i],
		reuters_summary_embeddings[i]) 
	for i in range(len(reuters_feed))]

for entry in reuters_entries:
	if entry.title not in [existing_entry.title for existing_entry in timeline['reuters'][str(now.date())]]:
		timeline['reuters'][str(now.date())].append(entry)
		print("entry appended")
	else:
		print("skipping...already exists")


# write updates to timeline file
pickle.dump(timeline, open( "timeline.p", "wb" ))
























# ##############test embeddings
# import nltk
# # nltk.download('punkt')







# sentences = []
# # example on how to create entry objects for every current feed entry
# guardian_entries = [FeedEntry(now.date(),
# 		get_headlines(guardian_feed)[i],
# 		get_summaries(guardian_feed)[i],
# 		get_tags(guardian_feed)[i]) for i in range(len(guardian_feed))]


# aljazeera_entries = [FeedEntry(now.date(),
# 		get_headlines(aljazeera_feed)[i],
# 		get_summaries(aljazeera_feed)[i],
# 		get_tags(aljazeera_feed)[i]) for i in range(len(aljazeera_feed))]


# nytimes_entries = [FeedEntry(now.date(),
# 		get_headlines(nytimes_feed)[i],
# 		get_summaries(nytimes_feed)[i],
# 		get_tags(nytimes_feed)[i]) for i in range(len(nytimes_feed))]
# # print(nytimes_entries)


# aljazeera_titles = [entry.get_summary for entry in aljazeera_entries]
# nytimes_titles = [entry.get_summary for entry in nytimes_entries]
# # print(aljazeera_titles)
# # print(nytimes_titles)


# # aljazeera_sample_embedding = model.encode(aljazeera_titles[np.random.randint(0,len(aljazeera_titles)-1)])[0]
# # aljazeera_sample_embedding = model.encode(aljazeera_titles[0])

# # print(aljazeera_sample_embedding[0])

# aljazeera_embeddings = model.encode(aljazeera_titles, bsize=64, tokenize=False, verbose=True) 
# nytimes_embeddings = model.encode(nytimes_titles, bsize=64, tokenize=False, verbose=True)


# r = np.random.randint(0, len(aljazeera_embeddings)-1)
# aljazeera_sample_embedding = aljazeera_embeddings[r]

# # print(len(aljazeera_embeddings))
# # print(len(nytimes_embeddings))
# min_dist = -1
# # closest_index = 0
# # aljazeera_sample_embedding_normalized = math_utils.normalize(aljazeera_sample_embedding)
# # for i,embedding in enumerate(nytimes_embeddings):

# # 	current_dist = math_utils.cosine_distance(math_utils.normalize(embedding), aljazeera_sample_embedding_normalized)
# # 	# current_dist = math_utils.euclidean_distance(aljazeera_sample_embedding, embedding)
# # 	print(current_dist)

# # 	print(nytimes_titles[i])
# # 	print(aljazeera_titles[r])
# # 	print("\n")
# # 	if current_dist >= min_dist:
# # 		min_dist = current_dist
# # 		closest_index = i


# # 	# print(current_dist)
# # print("closest:\n")
# # print(min_dist)
# # print(nytimes_titles[closest_index])
# # print("\n")
# # print(aljazeera_titles[r])
# # # print("\n")

# # # _, _ = model.visualize(nytimes_titles[closest_index])
# # # _, _ = model.visualize(aljazeera_titles[r])




# timeline = pickle.load(open( "timeline.p", "rb" ) )

# for entry in nytimes_entries:
# 	if entry.title not in [existing_entry.title for existing_entry in timeline['newyorktimes'][str(now.date())]]:
# 		timeline['newyorktimes'][str(now.date())].append(entry)
# 		# print(entry.title)
# 		print(timeline['newyorktimes'][str(now.date())])
# 		print("entry appended")
# 	else:
# 		print("skipping...already exists")

# for entry in aljazeera_entries:
# 	if entry.title not in [existing_entry.title for existing_entry in timeline['aljazeera'][str(now.date())]]:
# 		timeline['aljazeera'][str(now.date())].append(entry)
# 		print("entry appended")
# 	else:
# 		print("skipping...already exists")

# # for entry in bbc_entries:
# # 	if entry.title not in [existing_entry.title for existing_entry in timeline['bbc'][str(now.date())]]:
# 		# timeline['bbc'][str(now.date())].append(entry)
# 	# 	print("entry appended")
# # else:
# # 	print("skipping...already exists")

# for entry in guardian_entries:
# 	if entry.title not in [existing_entry.title for existing_entry in timeline['theguardian'][str(now.date())]]:
# 		timeline['theguardian'][str(now.date())].append(entry)
# 		print("entry appended")
# 	else:
# 		print("skipping...already exists")

# # # for entry in reuters_entries:
# # # 	if entry.title not in [existing_entry.title for existing_entry in timeline['reuters'][str(now.date())]]:
# # 		# timeline['reuters'][str(now.date())].append(entry)
# # 	# 	print("entry appended")
# # else:
# # 	print("skipping...already exists")


# pickle.dump(timeline, open( "timeline.p", "wb" ))


# print(timeline)


 	

