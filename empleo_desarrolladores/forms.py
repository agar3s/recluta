from django import forms
from models import Offer, Company, UserProfile

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer

class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ("user",)
