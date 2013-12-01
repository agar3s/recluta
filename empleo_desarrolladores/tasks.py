from .models import Offer
from messaging_handler import TenDaysLeftMessage
from models_factory import State

def terminate_offers():
	offers = Offer.objects.filter(state=State.published)
	for offer in offers:
		if not (offer.valid_time()):
			offer.state = 1
			offer.save()

def ten_days_left():
	offers = Offer.objects.filter(state=State.published)
	sender = TenDaysLeftMessage()
	[sender.send(offer) for offer in offers if offer.ten_days_left()]
