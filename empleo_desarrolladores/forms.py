#!/usr/bin/env python
# encoding: utf-8
from django import forms
from models import Offer
from taggit.forms import *

class ApplicantForm(forms.Form):
    mail = forms.EmailField(label='Email', widget=forms.TextInput())
    first_name = forms.CharField(label='Nombres', widget=forms.TextInput())
    last_name = forms.CharField(label='Apellidos', widget=forms.TextInput())
    observation = forms.CharField(label='Observación', widget=forms.Textarea({'placeholder':'Ingresa alguna observación que tengas con respecto a la oferta o a tus habilidades'}))


class CreateOfferForm(forms.Form):
    job_title = forms.CharField(label='Título',widget=forms.TextInput())
    job_description = forms.CharField(label='Descripción',widget=forms.Textarea())
    skills = TagField(label='Conocimientos')
    location = forms.CharField(label='Ciudad', widget=forms.TextInput({'placeholder':'Bogotá'}))
    type_contract = forms.ChoiceField(label='Tipo de contrato', choices=Offer.TYPE_OF_CONTRACT)
    salary = forms.ChoiceField(label='Salario', choices=Offer.SALARY_CHOICES)

class CreateOfferFormLoader():

    def load_initial_data(self, offer):
        s = [skill.name for skill in offer.skills.all()]

        return CreateOfferForm(initial={
            'job_title': offer.job_title,
            'location': offer.location,
            'type_contract': offer.type_contract,
            'salary': offer.salary,
            'offer_valid_time': offer.offer_valid_time,
            'skills': ','.join(s),
            'job_description': offer.job_description,
        })

class CompanyForm(forms.Form):
    nit = forms.RegexField(max_length=30, regex=r'(^[0-9]{5,12}-[0-9]$)', error_message = ('El formato de NIT no es valido, debe ser por Ej.: 123456789-1' ), help_text='Esta información no sera compartida con terceros')
    name = forms.CharField(label='Nombre', widget=forms.TextInput())
    locationCompany = forms.CharField(label='Ciudad',widget=forms.TextInput({'placeholder':'Bogotá'}))
    website = forms.CharField(label='Sitio Web', required=False, widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.TextInput())
    phone = forms.RegexField(max_length=30, label='Teléfono', required=False, widget=forms.TextInput(), help_text="Código de area + N°. Ej.: (57) 765-4321", error_message = ('El teléfono no es valido'), regex=r'(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})' )  
    # image = forms.ImageField(require(d=False)

class CompanyFormLoader():
    def load_initial_data(self, company):
        return CompanyForm(initial={
            'nit':company.nit,
            'name':company.name,
            'locationCompany':company.location,
            'website':company.website,
            'email':company.email,
            'phone':company.phone,
        })
    
class UserEditForm(forms.Form):
    first_name = forms.CharField(required=False, label='Nombre',widget=forms.TextInput())
    last_name = forms.CharField(required=False, label='Apellidos', widget=forms.TextInput())
    email = forms.EmailField(label='Email', widget=forms.TextInput())

class UserEditFormLoader():
    def load_initial_data(self, user):
        return UserEditForm(initial={
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
        })

class ClarificationForm(forms.Form):
    aclaration = forms.CharField(label='Aclaración', widget=forms.Textarea())