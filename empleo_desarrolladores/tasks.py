from celery import task
from .models import Offer

@task
def terminate_offers():
	offers = Offer.objects.filter(state=2)
	for offer in offers:
		if not (offer.valid_time()):
			offer.state = 1
			offer.save()
