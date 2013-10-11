from empleo_desarrolladores.models import Company
import factory

class CompanyFactory(factory.DjangoModelFactory):
	FACTORY_FOR = Company
	name = 'Microsoft de Colombia'
	nit = 12343
	email = "microsoftcol@mail.com"
	location = "Bogota"
	website = "microsoft.com.co"
	phone = 3454345
