from django import forms
from models import Offer, Card
from taggit.forms import *

class ApplicantForm(forms.Form):
    mail = forms.EmailField(widget=forms.TextInput())
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    observation = forms.CharField(widget=forms.Textarea())


class CreateOfferForm(forms.Form):
    job_title = forms.CharField(widget=forms.TextInput())
    job_description = forms.CharField(widget=forms.Textarea())
    skills = TagField()
    location = forms.CharField(widget=forms.TextInput())
    type_contract = forms.ChoiceField(choices=Offer.TYPE_OF_CONTRACT)
    salary = forms.ChoiceField(choices=Offer.SALARY_CHOICES)

class CompanyForm(forms.Form):
    nit = forms.CharField(widget=forms.TextInput())
    name = forms.CharField(widget=forms.TextInput())
    locationCompany = forms.CharField(label='Location',widget=forms.TextInput())
    website = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
    phone = forms.IntegerField(widget=forms.TextInput())
    # image = forms.ImageField(require(d=False)
    
class UserEditForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())

class CreditCardForm(forms.Form):
    card_type = forms.ChoiceField(choices=Card.CARD_TYPE)
    number = forms.IntegerField(widget=forms.TextInput())
    expiration = forms.DateTimeField(widget=forms.TextInput())
    owner = forms.CharField(widget=forms.TextInput())
    ccv2 = forms.IntegerField(widget=forms.TextInput())
    address = forms.CharField(widget=forms.TextInput())
    city = forms.CharField(widget=forms.TextInput())
    province = forms.CharField(widget=forms.TextInput())
    postal_code = forms.IntegerField(widget=forms.TextInput(), required=False)
