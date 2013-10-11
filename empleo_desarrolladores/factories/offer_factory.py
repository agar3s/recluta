from company_factory import CompanyFactory
from empleo_desarrolladores.models import Offer
import factory

class OfferFactory(factory.DjangoModelFactory):
	FACTORY_FOR = Offer

	job_title = 'Django Developer'
	location = 'Bogota'
	state = 0 
	salary = 0
	offer_valid_time = '2014-10-10'
 	job_description = 'A description'
	company = factory.SubFactory(CompanyFactory)