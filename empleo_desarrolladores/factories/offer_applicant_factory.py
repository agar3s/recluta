from empleo_desarrolladores.models import OfferApplicant
from offer_factory import OfferFactory
from applicant_factory import ApplicantFactory

import factory

class OfferApplicantFactory(factory.DjangoModelFactory):
	FACTORY_FOR = OfferApplicant
	offer = factory.SubFactory(OfferFactory)
	applicant = factory.SubFactory(ApplicantFactory)
	state = False
	token = 'Mytoken1234567'
	observation = 'I need the job'