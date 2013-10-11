from empleo_desarrolladores.models import Card
import factory

class CardFactory(factory.DjangoModelFactory):
	FACTORY_FOR = Card
	card_type = 'VS'
	number = 232323
	expiration = '2015-10-10'
	owner = 'Bruce Dickinson'
	ccv2 = 343434
	address = 'Kra 123 Cll 23 23'
	city = 'Bogota'
	province = 'Cundinamarca'
	postal_code = 34434