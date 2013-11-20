#!/usr/bin/env python
# encoding: utf-8
from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone
from django.template import defaultfilters
from datetime import datetime, timedelta

class Company(models.Model):

    def url(self, filename):
        path = "media_data/company_image/%s/%s" % (self.name, str(filename))
        return path

    nit = models.CharField(max_length=30)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=40)
    image = models.ImageField(upload_to=url, blank=True, null=True)

    def __unicode__(self):
        return self.name


class Applicant(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    mail = models.EmailField(unique=True)

    def __unicode__(self):
        return self.mail

    def full_name(self):
        return ('%s %s' % (self.first_name, self.last_name)).strip()


class Offer(models.Model):

    job_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100, null=True, default='Bogota')
    TYPE_OF_CONTRACT = (
        ('FT', 'Tiempo Completo'),
        ('PT', 'Medio Tiempo'),
        ('TL', 'Telecommute'),
        ('CT', 'Contractor'),
    )
    type_contract = models.CharField(max_length=2, choices=TYPE_OF_CONTRACT, default='FT')
    SALARY_CHOICES = (
        (0, 'Negociable'),
        (10, '550.000 - 1.000.000'),
        (15, '1.000.000 - 1.500.000'),
        (20, '1.500.000 - 2.000.000'),
        (25, '2.000.000 - 2.500.000'),
        (30, '2.500.000 - 3.000.000'),
        (35, '3.000.000 - 3.500.000'),
        (40, '3.500.000 - 4.000.000'),
        (45, '4.000.000 - 4.500.000'),
        (50, '4.500.000 - 5.000.000'),
        (55, '5.000.000 - Más'),
    )

    STATE_CHOICES = ((0, 'draft'), (1, 'finished'), (2, 'published'))
    state = models.IntegerField(choices=STATE_CHOICES, default=0)
    applicants = models.ManyToManyField(Applicant, through="OfferApplicant")
    salary = models.IntegerField(max_length=2, choices=SALARY_CHOICES, default=0)
    offer_valid_time = models.DateTimeField()
    skills = TaggableManager()
    job_description = models.TextField(null=False)
    company = models.ForeignKey(Company, null=True)
    slug = models.SlugField(max_length=250, unique=True)
    clarification = models.TextField(null=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = defaultfilters.slugify(self.company.name+'-'+self.job_title)
        super(Offer, self).save(*args, **kwargs)

    def days_remaining(self):
        now = timezone.make_aware(datetime.now(), timezone.get_default_timezone())
        days_remaining = self.offer_valid_time - now
        return days_remaining.days

    def get_salary(self):
        for i in self.SALARY_CHOICES:
            if self.salary == i[0]:
                return i[1]

    def set_state(self, state):
        for i in self.STATE_CHOICES:
            if state == i[1]:
                self.state  = i[0]

    def is_published(self):
        return True if self.state==2 else False

    def is_draft(self):
        return True if self.state==0 else False

    def is_finished(self):
        return True if self.state==1 else False

    def __unicode__(self):
        return self.job_title

    def valid_time(self):
        return self.offer_valid_time >= timezone.now() 


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    company = models.ForeignKey(Company, null=True, blank=True)

    def __unicode__(self):
        return "%s's profile" % self.user


class OfferApplicant(models.Model):

    offer = models.ForeignKey(Offer)
    applicant = models.ForeignKey(Applicant)
    observation = models.TextField()
    state = models.BooleanField()
    token = models.TextField(unique=True)

    def __unicode__(self):
        return "Offer: " + self.offer.job_title + " Applicant: " + self.applicant.mail

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
