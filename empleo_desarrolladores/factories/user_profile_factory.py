from empleo_desarrolladores.models import UserProfile
from company_factory import CompanyFactory
from card_factory import CardFactory
from user_factory import UserFactory
import factory

class UserProfileFactory(factory.DjangoModelFactory):
	FACTORY_FOR = UserProfile
	company = factory.SubFactory(CompanyFactory)
	card = factory.SubFactory(CardFactory)
	user = factory.SubFactory(UserFactory)