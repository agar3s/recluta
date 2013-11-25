from company_factory import CompanyFactory
from empleo_desarrolladores.models import Offer
import factory
from datetime import datetime, timedelta

class State():
	published = 2
	finished = 1
	draft = 0

class OfferFactory(factory.DjangoModelFactory):
	FACTORY_FOR = Offer

	job_title = 'Django Developer'
	location = 'Bogota'
	state = 0 
	salary = 0
	offer_valid_time = datetime.now() + timedelta(days=30)
 	job_description = 'A description'
 	highlighted = False
	company = factory.SubFactory(CompanyFactory)