from django import forms
from models import Offer, Company, UserProfile
from haystack.forms import HighlightedSearchForm
from django.contrib.admin.widgets import AdminDateWidget


class MySearchForm(HighlightedSearchForm):
    q = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'placeholder': 'Search Offers ...', 'class': 'span6'}))


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        exclude = ("applicants",)


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company


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
    skills = forms.CharField(widget=forms.TextInput())
    location = forms.CharField(widget=forms.TextInput())
    type_contract = forms.ChoiceField(choices=Offer.TYPE_OF_CONTRACT)
    salary = forms.ChoiceField(choices=Offer.SALARY_CHOICES)
    offer_valid_time = forms.DateField(widget=AdminDateWidget())
