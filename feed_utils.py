import feedparser
import re



class FeedEntry():
	""" Data model for a fetched feed entry. """
	def __init__(self, date, country, scheme, title, summary, tags):
		# meta
		self.date = date
		self.country = country
		self.scheme = scheme
		# data
		self.title = title
		self.summary = summary
		self.tags = tags



	@property
	def get_title_vector():
		pass

	@property
	def get_summary_vector():
		pass

	@property
	def get_tags_vector():
		pass



	@staticmethod
	def clear_xml(text):
		""" Static helper to remove xml syntax from a string. """
		return re.sub(u"[^\x20-\x7f]+",u"", text)

	@staticmethod
	def clear_html(text):
		""" Static helper to remove xml syntax from a string. """
		return re.sub(re.compile('<.*?>'), '', text)

