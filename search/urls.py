from django.conf.urls.defaults import *
from haystack.forms import SearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView
# from views import Home
from django.conf.urls.defaults import *
from haystack.forms import FacetedSearchForm
from haystack.views import FacetedSearchView, search_view_factory
from empleo_desarrolladores.models import Offer

# sqs = SearchQuerySet().facet('location')

# urlpatterns = patterns('haystack.views',
#     url(r'^$', search_view_factory(view_class=FacetedSearchView, form_class=FacetedSearchForm ,searchqueryset=sqs, template='search/home.html'), name='home'),
# )

# urlpatterns = patterns('search.views',
#     url(r'^$', Home.as_view(), name='home'),
# )

urlpatterns = patterns('search.views',
    url(r'^$', 'home', name='home'),
)