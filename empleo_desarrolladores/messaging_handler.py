#!/usr/bin/env python
# encoding: utf-8
from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader
from models import UserProfile

class OfferApplicantMessage():
	def send(self, offer_applicant):
		to_applicant = offer_applicant.applicant.mail
		template = loader.get_template('applicant_mail.html')
		html = template.render(Context({'offer':offer_applicant.offer, 'applicant':offer_applicant.applicant, 'offer_applicant':offer_applicant}))
		msg = EmailMultiAlternatives('Has aplicado a la oferta %s' %(offer_applicant.offer.job_title), html,'notification@codetag.me', [to_applicant])
		msg.attach_alternative(html, 'text/html')
		msg.send()

class TenDaysLeftMessage():
	def send(self, offer):
		emails = [profile.user.email for profile in UserProfile.objects.filter(company=offer.company)]
		template = loader.get_template('ten_days_left_message.html')
		html = template.render(Context({'offer':offer}))
		msg = EmailMultiAlternatives(u'La oferta "%s" terminará en 10 días' % (offer.job_title), html, 'notification@codetag.me', emails)
		msg.attach_alternative(html, 'text/html')
		msg.send()
