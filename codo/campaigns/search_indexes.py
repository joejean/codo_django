import datetime
from haystack import indexes
from .models import Campaign

class CampaignIndex(indexes.SearchIndex, indexes.Indexable):
	'''This is a search index for the Campaign model. See haystack doc
	   http://django-haystack.readthedocs.io/en/v2.4.1/tutorial.html
	'''
	text = indexes.CharField(document=True, use_template=True)
	title = indexes.CharField(model_attr='title')
	organizer = indexes.CharField(model_attr='organizer')
	created = indexes.DateTimeField(model_attr='created')

	def get_model(self):
		return Campaign

	def index_queryset(self, using=None):
		"""Used when the entire index for model is updated."""
		return self.get_model().objects.filter(modified__lte=datetime.datetime.now())