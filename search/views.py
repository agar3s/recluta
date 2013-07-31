# Create your views here.
from django.views.generic.base import View
from empleo_desarrolladores.models import Offer
from haystack.views import basic_search, FacetedSearchView
from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView, search_view_factory
from haystack.inputs import AutoQuery, Exact

# class Home(View, FacetedSearchView):

#     def get(self, request):
#     	sqs = SearchQuerySet().facet('location')
#         offers = Offer.objects.filter(state=2)
#         return basic_search(request,searchqueryset=sqs, form_class=FacetedSearchForm, extra_context={'offers': offers}, template='search/home.html', results_per_page=5)

def home(request):
	sqs = SearchQuerySet().facet('location')
	view = search_view_factory(
		view_class=FacetedSearchView,
		template='search/home.html',
		searchqueryset=sqs,
		form_class=FacetedSearchForm,
		results_per_page=5
	)
	return view(request)