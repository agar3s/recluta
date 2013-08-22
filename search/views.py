from haystack.views import FacetedSearchView
from haystack.query import SearchQuerySet
from haystack.forms import FacetedSearchForm

class HomeSearchView(FacetedSearchView):
	
	def get_results(self):
		if self.get_query():
			return self.form.search()
		else:
			return self.searchqueryset.all()
		

def homeSearch(request):
	sqs = SearchQuerySet().facet('location')
	view = HomeSearchView(form_class=FacetedSearchForm, 
		searchqueryset=sqs, 
		template='search/home.html',
		results_per_page=10)
	return view(request)
