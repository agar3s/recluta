from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import admin


class Company(models.Model):
    nit = models.CharField(max_length=30)
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=100)
    image = models.ImageField(upload_to='companies', blank=True, null=True)

    def address_to_update(self):
        return reverse_lazy('company_update', args=[self.pk])

    def adress_to_delete(self):
        return reverse_lazy('company_delete', args=[self.pk])

    def __unicode__(self):
        return self.company_name


class Applicant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mail = models.EmailField(unique=True)

    def __unicode__(self):
        return self.mail

    def full_name(self):
        return self.first_name+" "+self.last_name


class Offer(models.Model):

    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, default='Bogota')
    TYPE_OF_CONTRACT = (
        ('FT', 'Full Time'),
        ('PT', 'Part Time'),
        ('TL', 'Telecommute'),
        ('CT', 'Contractor'),
    )
    type_contract = models.CharField(max_length=2, choices=TYPE_OF_CONTRACT, default='FT')
    SALARY_CHOICES = (
        (0, 'Negotiable'),
        (10, '550.000 - 1.000.000'),
        (15, '1.000.000 - 1.500.000'),
        (20, '1.500.000 - 2.000.000'),
        (25, '2.000.000 - 2.500.000'),
        (30, '2.500.000 - 3.000.000'),
        (35, '3.000.000 - 3.500.000'),
        (40, '3.500.000 - 4.000.000'),
        (45, '4.000.000 - 4.500.000'),
        (50, '4.500.000 - 5.000.000'),
        (55, '5.000.000 - More'),
    )

    STATE_CHOICES = ((0, 'Draft'), (1, 'Terminate'), (2, 'Live'))
    state = models.IntegerField(choices=STATE_CHOICES, default=0)
    applicants = models.ManyToManyField(Applicant, through="OfferApplicant")
    salary = models.IntegerField(max_length=2, choices=SALARY_CHOICES, default=0)
    offer_valid_time = models.DateTimeField()
    skills = models.TextField(null=True)
    job_description = models.TextField(null=False)
    company = models.ForeignKey(Company, null=True)

    def address_to_update(self):
        return reverse_lazy('offer_update', args=[self.pk])

    def adress_to_delete(self):
        return reverse_lazy('offer_delete', args=[self.pk])

    def address_to_details(self):
        return reverse_lazy('offer_detail', args=[self.pk])

    def __unicode__(self):
        return self.job_title


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    def address_to_update(self):
        return reverse_lazy('developer_update', args=[self.pk])

    def adress_to_delete(self):
        return reverse_lazy('developer_delete', args=[self.pk])

    def __unicode__(self):
        return "%s's profile" % self.user


def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)


class OfferApplicant(models.Model):

    offer = models.ForeignKey(Offer)
    applicant = models.ForeignKey(Applicant)
    observation = models.TextField()

    def __unicode__(self):
        return "Offer: " + self.offer.job_title + " Applicant: " + self.applicant.mail

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
