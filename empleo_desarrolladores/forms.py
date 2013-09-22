from django import forms
from models import Offer, UserProfile
from taggit.forms import *

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)


class ApplicantForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    mail = forms.EmailField(widget=forms.TextInput())
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
    # image = forms.ImageField(required=False)

class UserEditForm(forms.Form):
    first_name = forms.CharField(widget=forms.TextInput())
    last_name = forms.CharField(widget=forms.TextInput())
    email = forms.EmailField(widget=forms.TextInput())
