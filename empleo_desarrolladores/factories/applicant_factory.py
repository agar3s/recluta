from empleo_desarrolladores.models import Applicant
import factory

class ApplicantFactory(factory.DjangoModelFactory):
	FACTORY_FOR = Applicant
	first_name = 'yo'
	last_name = 'bender'
	mail = 'bender@gmail.com'