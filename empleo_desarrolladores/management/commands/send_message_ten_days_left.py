from django.core.management.base import BaseCommand
from empleo_desarrolladores.models import Offer
from messaging_handler import TenDaysLeftMessage
from models_factory import State

class Command(BaseCommand):
    help = 'Terminate the offer with days remaining equals to 0'

    def handle(self, *args, **options):
        offers = Offer.objects.filter(state=State.published, ten_days_left_message=False)
        sender = TenDaysLeftMessage()
        for offer in offers:
            offer.ten_days_left_message = True 
            offer.save()
        [sender.send(offer) for offer in offers if offer.ten_days_left()]
        self.stdout.write('Successfully sended messages')