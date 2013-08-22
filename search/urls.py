from django.conf.urls.defaults import *
from haystack.query import SearchQuerySet
from django.conf.urls.defaults import *
from haystack.forms import FacetedSearchForm
from .views import HomeSearchView

# sqs = SearchQuerySet().facet('location')

# urlpatterns = patterns('haystack.views',
#     url(r'^$', HomeSearchView(form_class=FacetedSearchForm ,searchqueryset=sqs, template='search/home.html'), name='home'),
# )

urlpatterns = patterns('search.views',
    url(r'^$', 'homeSearch', name='home'),
)