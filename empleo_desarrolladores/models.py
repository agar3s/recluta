from django.db import models
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib import admin

class Developer(models.Model):
    name = models.CharField(max_length=100)
    mail = models.EmailField()

    def address_to_update(self):
        return reverse_lazy('developer_update', args=[self.pk])
                
    def adress_to_delete(self):
        return reverse_lazy('developer_delete', args=[self.pk])

    def __unicode__(self):
        return self.developer.name

class Offer(models.Model):
    offer_company_that_publishes = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)
    TYPE_OF_CONTRACT = (
        ('TF', 'Termino Fijo'),
        ('FR', 'Freelance'),
        )
    type_contract = models.CharField(max_length=2, choices=TYPE_OF_CONTRACT, default = 'TF')
    SALARY_CHOICES = (
        (0, 'A Convenir'),
        (10, 'De 550.000 a 1.000.000'),
        (15, 'De 1.000.000 a 1.500.000'),
        (20, 'De 1.500.000 a 2.000.000'),
        (25, 'De 2.000.000 a 2.500.000'),
        (30, 'De 2.500.000 a 3.000.000'),
        (35, 'De 3.000.000 a 3.500.000'),
        (40, 'De 3.500.000 a 4.000.000'),
        (45, 'De 4.000.000 a 4.500.000'),
        (50, 'De 4.500.000 a 5.000.000'),
        (55, 'De 5.000.000 en Adelante'),
        )
    salary = models.IntegerField(max_length=2, choices = SALARY_CHOICES, default = 0)
    Offer_valid_time = models.DateTimeField()
    mandatory_skills = models.TextField(null=False)
    optional_skills = models.TextField(null=False)
    job_description = models.TextField(null=False)
    obligations_under = models.TextField(null=False)

    def address_to_update(self):
        return reverse_lazy('offer_update', args=[self.pk])
                
    def adress_to_delete(self):
        return reverse_lazy('offer_delete', args=[self.pk])

    def __unicode__(self):
        return self.offer.job_title

class Company(models.Model):
    nit = models.CharField(max_length=30) 
    company_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField(max_length=100)
    image = models.ImageField(upload_to='companies')

    def address_to_update(self):
        return reverse_lazy('company_update', args=[self.pk])
                
    def adress_to_delete(self):
        return reverse_lazy('company_delete', args=[self.pk])

    def __unicode__(self):
        return self.company.company_name

class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True)
    biography = models.TextField(null=True)
            
    def __unicode__(self):
        return "%s's profile" % self.user

def create_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

from django.db.models.signals import post_save
post_save.connect(create_profile, sender=User)
