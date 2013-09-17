from datetime import datetime
from django.utils import timezone
from django.http import HttpRequest
from django.test import TestCase
from empleo_desarrolladores.models import Company, Applicant, Offer
from django.contrib.auth.models import User
from empleo_desarrolladores.views import offerDetailsView, userProfileEditView, createPositionView, terminatePositionView
from django.test.client import RequestFactory

class CompanyTest(TestCase):
    def test_url_should_return_the_path_to_the_company_logo(self):
        company = Company()
        company.name = 'codetag'
        
        self.assertEqual(company.url('my_file.jpg'), 'media_data/company_image/codetag/my_file.jpg')

class ApplicantTest(TestCase):
    def test_full_name_should_return_a_string_containing_first_and_last_names_separated_by_a_space(self):
        applicant = Applicant()
        applicant.first_name = "yo"
        applicant.last_name = "robot"

        self.assertEqual(applicant.full_name(), "yo robot")

    def test_full_name_should_return_an_empty_string_when_first_and_last_name_are_empty(self):
        applicant = Applicant()
        
        self.assertEqual(applicant.full_name(), "")

class OfferTest(TestCase):
    def test_valid_time_should_return_true_when_the_offer_valid_time_is_greater_than_current_date(self):
        now = datetime.now()
        tomorrow = datetime(now.year, now.month, now.day+1, 0, 0, 0)
        offer = Offer()
        offer.offer_valid_time = timezone.make_aware(tomorrow, timezone.get_default_timezone())

        self.assertEqual(offer.valid_time(), True)

    def test_valid_time_should_return_true_when_the_offer_valid_time_is_equal_to_current_date(self):
        now = datetime.now()
        today = datetime(now.year,now.month, now.day, 23,59,59)
        offer = Offer()
        offer.offer_valid_time = timezone.make_aware(today, timezone.get_default_timezone())

        self.assertEqual(offer.valid_time(), True)

    def test_valid_time_should_retun_false_when_the_offer_valid_time_is_lower_than_curret_date(self):
        now = datetime.now()
        yesterday = datetime(now.year, now.month, now.day-1, 0, 0, 0)
        offer = Offer()
        offer.offer_valid_time = timezone.make_aware(yesterday, timezone.get_default_timezone())

        self.assertEqual(offer.valid_time(), False)

class OfferDetailsViewTest(TestCase):
    def test_GET_should_redirect_to_home_when_the_given_offer_has_state_1(self):
        offer = Offer(offer_valid_time = datetime.now(), state=1)
        offer.save()
        request = HttpRequest()
        request.method = 'GET'
        result = offerDetailsView(request, offer.id)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'], '/')

    def test_GET_should_redirect_to_home_when_the_given_offer_has_state_0(self):
        offer = Offer(offer_valid_time = datetime.now(), state=0)
        offer.save()
        request = HttpRequest()
        request.method = 'GET'
        result = offerDetailsView(request, offer.id)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'], '/')

    def test_GET_should_render_the_offer_detail_template_when_the_offers_state_is_not_1_nor_0(self):
        offer = Offer(offer_valid_time = datetime.now(), state=3)
        offer.save()
        request = HttpRequest()
        request.method = 'GET'
        result = offerDetailsView(request, offer.id)

        self.assertEqual(result.status_code, 200)

    def test_POST_should_redirect_to_home_when_the_given_data_is_valid(self):
        offer = Offer(offer_valid_time = datetime.now(), state=0)
        offer.save()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['first_name'] = 'yo'
        request.POST['last_name'] = 'bender'
        request.POST['mail'] = 'bender@gmail.com'
        request.POST['observation'] = 'well, none'

        result = offerDetailsView(request, offer.id)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'], '/')

class UserProfileEditViewTest(TestCase):
    def test_POST_should_redirect_to_home_when_the_given_data_is_valid(self):
        
        factory = RequestFactory()
        user = User.objects.create_user(username='yo',password='pass')

        request = factory.post('/edit_profile/')
        request.user = user
        request.POST['first_name'] = 'ignus'
        request.POST['last_name'] = 'smart'
        request.POST['email'] = 'ignus@gmail.com'
        
        result = userProfileEditView(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/')

    def test_GET_should_render_the_user_profile_edit_template(self):
        
        factory = RequestFactory()
        user = User.objects.create_user(username='yo',password='pass')

        request = factory.get('/edit_profile/')
        request.user = user
        result = userProfileEditView(request)

        self.assertEqual(result.status_code, 200)

class CreatePositionViewTest(TestCase):
    def test_POST_save_should_redirect_to_positions_list_when_the_given_data_is_valid(self):
        
        factory = RequestFactory()
        user = User.objects.create_user(username='yo',password='pass')

        request = factory.post('/positions/create/')
        request.user = user
        request.POST['job_title'] = 'Developer'
        request.POST['location'] = 'Bogota'
        request.POST['type_contract'] = 1
        request.POST['salary']=15
        request.POST['offer_valid_time']='23-12-2013'
        request.POST['skills']='Java'
        request.POST['job_description']='This is a description'
        request.POST['_save']=1
        result = createPositionView(request)
        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/list')

    def test_POST_publish_should_redirect_to_positions_list_when_the_given_data_is_valid(self):
        
        user = User.objects.create_user(username='yo',password='pass')

        factory = RequestFactory()
        request = factory.post('/positions/create/')
        request.user = user
        request.POST['job_title'] = 'Developer'
        request.POST['location'] = 'Bogota'
        request.POST['type_contract'] = 1
        request.POST['salary']=15
        request.POST['offer_valid_time']='23-12-2013'
        request.POST['skills']='Java'
        request.POST['job_description']='This is a description'
        request.POST['_publish']=1
        result = createPositionView(request)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/list')

    def test_GET_should_render_the_user_profile_edit_template(self):
        
        user = User.objects.create_user(username='yo',password='pass')

        factory = RequestFactory()
        request = factory.get('/positions/create/')
        request.user = user
        result = userProfileEditView(request)

        self.assertEqual(result.status_code, 200)

class TerminatePositionViewTest(TestCase):

    def test_GET_should_redirect_positions_list_when_user_company_equals_offer_company(self):
        
        company = Company()        

        user = User.objects.create_user(username='yo',password='pass')
        user.userprofile.company = company

        offer = Offer(offer_valid_time = datetime.now(), state=0)
        offer.company = company
        offer.save()

        factory = RequestFactory()
        request = factory.get('/positions/terminate/%s' % offer.id)
        request.user = user
        result = terminatePositionView(request, offer.id)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/list')

    def test_GET_should_redirect_positions_list_when_user_company_different_offer_company(self):
        
        company1 = Company()
        company2 = Company()        

        user = User.objects.create_user(username='yo',password='pass')
        user.userprofile.company = company2

        offer = Offer(offer_valid_time = datetime.now(), state=0)
        offer.company = company1
        offer.save()

        factory = RequestFactory()
        request = factory.get('/positions/terminate/%s' % offer.id)
        request.user = user
        result = terminatePositionView(request, offer.id)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/list')

