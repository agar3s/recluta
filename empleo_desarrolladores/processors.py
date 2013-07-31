from models import Offer

def offers(request):
    return {'offers': Offer.objects.filter(state=2)}