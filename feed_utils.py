import feedparser
import re







class FeedEntry():
	""" Data model for a fetched feed entry. """
	def __init__(self, date, title, summary, title_embedding, summary_embedding, tags = None):
		# meta
		self.date = date
		# self.country = country # maybe not necessary
		# data
		self.title = title
		self.summary = summary
		self.title_embedding = title_embedding
		self.summary_embedding = summary_embedding
		self.tags = tags



	# how much these affect final vector is a parameter that should be learned	(weighted matmul)
	@property
	def get_title_embedding(self):
		pass

	@property
	def get_summary_embedding(self):
		pass

	@property
	def get_tags_embedding(self):
		pass


	@property
	def get_overall_vector(self, title_weight = 0.2, summary_weight = 0.6, tags_weight = 0.2):
		""" TODO Find out what kind of product is usefule here... """
		# v3.x = (v1.x + v2.x) / 2;
		# overall_vector.x = (self.title_vector.x + self.summary_vector.x + self.tags_vector.x) / 3
		# overall_vector.y = (self.title_vector.y + self.summary_vector.y + self.tags_vector.y) / 3

		# return (overall_vector.x, overall_vector.y)
		pass


	@property
	def get_summary(self):
		return self.clear_html(self.clear_xml(self.summary))



	# static methods for parsing
	@staticmethod
	def clear_xml(text):
		""" Static helper to remove xml syntax from a string. """
		return re.sub(u"[^\x20-\x7f]+", u"", text)

	@staticmethod
	def clear_html(text):
		""" Static helper to remove xml syntax from a string. """
		return re.sub(re.compile('<.*?>'), '', text)


	@staticmethod
	def remove_words(*args, text):
		return text.replace([arg  for arg in args], "")





# @property
def clear_summary(summary):
	return clear_html(clear_xml(summary))



# static methods for parsing
# @staticmethod
def clear_xml(text):
	""" Static helper to remove xml syntax from a string. """
	return re.sub(u"[^\x20-\x7f]+", u"", text)

# @staticmethod
def clear_html(text):
	""" Static helper to remove xml syntax from a string. """
	return re.sub(re.compile('<.*?>'), '', text)