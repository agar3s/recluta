import datetime
from haystack import indexes
from models import Offer


class OfferIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    company = indexes.CharField(model_attr='company', faceted=True)
    job_title = indexes.CharField(model_attr='job_title')
    location = indexes.CharField(model_attr='location', faceted=True)
    job_description = indexes.CharField(model_attr="job_description")

    def get_model(self):
        return Offer

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(state=2)
