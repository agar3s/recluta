from models import Applicant, OfferApplicant, Card, Offer, Company
from hashids import Hashids
from datetime import datetime, timedelta

class ApplicantFactory():
    def get_instance_form(self, form):
        mail = form.cleaned_data['mail']
        if Applicant.objects.filter(mail=mail).exists():
            applicant = Applicant.objects.get(mail=mail)
        else:
            applicant = Applicant()
            applicant.first_name = form.cleaned_data['first_name']
            applicant.last_name = form.cleaned_data['last_name']
            applicant.mail = mail
            applicant.save()

        return applicant

class OfferApplicantFactory():
    def get_instance_form(self, applicant, offer, form):
        hashid = Hashids(salt='codetag Job Post')
        if OfferApplicant.objects.filter(applicant=applicant, offer=offer).exists():
            offer_applicant = OfferApplicant.objects.get(applicant=applicant, offer=offer)
            offer_applicant.observation = form.cleaned_data['observation']
            offer_applicant.state = False
            offer_applicant.token = hashid.encrypt(offer.id, applicant.id)
            offer_applicant.save()
        else:
            offer_applicant = OfferApplicant()
            offer_applicant.applicant = applicant
            offer_applicant.offer = offer
            offer_applicant.observation = form.cleaned_data['observation']
            offer_applicant.state = False
            offer_applicant.token = hashid.encrypt(offer.id, applicant.id)
            offer_applicant.save()

        return offer_applicant

class CardFactory():
    def save_instance_form(self, form, user):
        card = Card()
        card.card_type = form.cleaned_data['card_type']
        card.number = form.cleaned_data['number']
        card.expiration = form.cleaned_data['expiration']
        card.owner = form.cleaned_data['owner']
        card.ccv2 = form.cleaned_data['ccv2']
        card.address = form.cleaned_data['address']
        card.city = form.cleaned_data['city']
        card.province = form.cleaned_data['province']
        card.postal_code = form.cleaned_data['postal_code']
        card.save()
        user.card = card
        user.save()

class UserProfileFactory():
    def save_instance_form(self, form, user):
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        user.email = form.cleaned_data['email']
        user.save()

class OfferFactory():
    def get_instance_form(self, form, offer_slug, company):
        if Offer.objects.filter(slug=offer_slug).exists():       
            offer = Offer.objects.get(slug=offer_slug)
        else:
            offer = Offer()
            offer.job_title = form.cleaned_data['job_title']
            offer.location = form.cleaned_data['location']
            offer.type_contract = form.cleaned_data['type_contract']
            offer.salary = form.cleaned_data['salary']
            offer.state = 0
            offer.offer_valid_time = datetime.now() + timedelta(days=30)
            skills = form.cleaned_data['skills']
            offer.job_description = form.cleaned_data['job_description']
            offer.company = company
            offer.save()
            for skill in skills:
                offer.skills.add(skill)
        return offer

    def update_instance_form(self, form, offer, company):
        offer.job_title = form.cleaned_data['job_title']
        offer.location = form.cleaned_data['location']
        offer.type_contract = form.cleaned_data['type_contract']
        offer.salary = form.cleaned_data['salary']
        offer.offer_valid_time = datetime.now() + timedelta(days=30)
        skills = form.cleaned_data['skills']
        offer.job_description = form.cleaned_data['job_description']
        offer.company = company

        for skill in skills:
            offer.skills.add(skill)

class CompanyFactory():
    def save_instance_form(self, form, user):
        company = Company()
        company.nit = form.cleaned_data['nit']
        company.name = form.cleaned_data['name']
        company.location = form.cleaned_data['locationCompany']
        company.website = form.cleaned_data['website']
        company.email = form.cleaned_data['email']
        company.phone = form.cleaned_data['phone']
        company.save()
        user.company = company
        user.save()

    def update_instance_form(self, company, form):
        company.nit = form.cleaned_data['nit']
        company.name = form.cleaned_data['name']
        company.location = form.cleaned_data['locationCompany']
        company.website = form.cleaned_data['website']
        company.email = form.cleaned_data['email']
        company.phone = form.cleaned_data['phone']
        company.save()


