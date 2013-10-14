from django.contrib.auth.models import User
import factory

class UserFactory(factory.DjangoModelFactory):
	FACTORY_FOR = User

	username = 'Dave Murray'
	password = 'pass'