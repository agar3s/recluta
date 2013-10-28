from django.core.mail import EmailMultiAlternatives
from django.template import Context, loader

class OfferApplicantMessage():
	def send(self, offer_applicant):
		to_applicant = offer_applicant.applicant.mail
		template = loader.get_template('applicant_mail.html')
		html = template.render(Context({'offer':offer_applicant.offer, 'applicant':offer_applicant.applicant, 'offer_applicant':offer_applicant}))
		msg = EmailMultiAlternatives('Has aplicado a la oferta %s' %(offer_applicant.offer.job_title), html,'notification@codetag.me', [to_applicant])
		msg.attach_alternative(html, 'text/html')
		msg.send()
