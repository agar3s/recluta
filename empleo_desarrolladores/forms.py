#!/usr/bin/env python
# encoding: utf-8
from django import forms
from models import Offer, Card
from taggit.forms import *

class ApplicantForm(forms.Form):
    mail = forms.EmailField(label='Email', widget=forms.TextInput())
    first_name = forms.CharField(label='Nombres', widget=forms.TextInput())
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput())
    observation = forms.CharField(label='Observación', widget=forms.Textarea())


class CreateOfferForm(forms.Form):
    job_title = forms.CharField(label='Título',widget=forms.TextInput())
    job_description = forms.CharField(label='Descripción',widget=forms.Textarea())
    skills = TagField(label='Conocimientos')
    location = forms.CharField(label='Localización', widget=forms.TextInput())
    type_contract = forms.ChoiceField(label='Tipo de contrato', choices=Offer.TYPE_OF_CONTRACT)
    salary = forms.ChoiceField(label='Salario', choices=Offer.SALARY_CHOICES)

class CompanyForm(forms.Form):
    nit = forms.CharField(label='NIT', widget=forms.TextInput())
    name = forms.CharField(label='Nombre', widget=forms.TextInput())
    locationCompany = forms.CharField(label='Localización',widget=forms.TextInput())
    website = forms.CharField(label='Sitio Web',widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.TextInput())
    phone = forms.IntegerField(label='Teléfono',widget=forms.TextInput())
    # image = forms.ImageField(require(d=False)
    
class UserEditForm(forms.Form):
    first_name = forms.CharField(label='Nombre',widget=forms.TextInput())
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.TextInput())

class CreditCardForm(forms.Form):
    card_type = forms.ChoiceField(label='Tipo de Tarjeta',choices=Card.CARD_TYPE)
    number = forms.IntegerField(label='Número', widget=forms.TextInput())
    expiration = forms.DateTimeField(label='Vencimiento', widget=forms.TextInput())
    owner = forms.CharField(label='Propietario', widget=forms.TextInput())
    ccv2 = forms.IntegerField(label='CCV2 / Código de Seguridad', widget=forms.TextInput())
    address = forms.CharField(label='Dirección', widget=forms.TextInput())
    city = forms.CharField(label='Ciudad', widget=forms.TextInput())
    province = forms.CharField(label='Departamento', widget=forms.TextInput())
    postal_code = forms.IntegerField(label='Código', widget=forms.TextInput(), required=False)
