from django.core.management.base import BaseCommand
from empleo_desarrolladores.models import Offer
from models_factory import State

class Command(BaseCommand):
    help = 'Terminate the offer with days remaining equals to 0'

    def handle(self, *args, **options):
        offers = Offer.objects.filter(state=State.published)
        for offer in offers:
            if not (offer.valid_time()):
                offer.state = State.finished
                offer.save()

            self.stdout.write('Successfully terminated offer "%s"' % offer.job_title)
