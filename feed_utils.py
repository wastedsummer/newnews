import feedparser
import re



class FeedEntry():
	""" Data model for a fetched feed entry. """
	def __init__(self, date, title, summary, tags):
		# meta
		self.date = date
		# self.country = country # maybe not necessary
		# data
		self.title = title
		self.summary = summary
		self.tags = tags



	# how much these affect final vector is a parameter that should be learned	(weighted matmul)
	@property
	def get_title_vector(self):
		pass

	@property
	def get_summary_vector(self):
		pass

	@property
	def get_tags_vector(self):
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

