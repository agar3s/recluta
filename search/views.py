from empleo_desarrolladores.models import Offer
from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm

class HomeSearchView(FacetedSearchView):
	def extra_context(self):
		extra = super(HomeSearchView, self).extra_context()
		offers = Offer.objects.filter(state=2)
		extra['offers'] = offers
		extra['results'] = self.results
		return extra

def homeSearch(request):
	sqs = SearchQuerySet().facet('location')
	return HomeSearchView(form_class=FacetedSearchForm ,searchqueryset=sqs, template='search/home.html')(request)
