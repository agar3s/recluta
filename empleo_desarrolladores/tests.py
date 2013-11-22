from datetime import datetime, timedelta
from django.utils import timezone
from empleo_desarrolladores.factories.company_factory import CompanyFactory
from empleo_desarrolladores.factories.offer_factory import OfferFactory, State
from empleo_desarrolladores.factories.user_factory import UserFactory
from empleo_desarrolladores.factories.offer_applicant_factory import OfferApplicantFactory
from empleo_desarrolladores.factories.applicant_factory import ApplicantFactory
from django.http import HttpRequest
from django.test import TestCase
from django.test.utils import override_settings
from empleo_desarrolladores.models import Applicant, OfferApplicant 
from search.views import homeSearch
from empleo_desarrolladores.views import offerDetailsView, userProfileEditView, createPositionView, terminatePositionView, positionsListView, oldPositionsListView, completeCompanyInfoView, companyDetailView, positionDashBoardView,successfulApplicationView, positionPreviewView
from empleo_desarrolladores.views import plansAndPricingView, positionClarificationsView, positionDetailsView, purchaseFailView, purchaseSuccessView
from django.test.client import RequestFactory
import haystack
from django.core.management import call_command
from django_nose import FastFixtureTestCase

class CompanyTest(TestCase):
    def test_url_should_return_the_path_to_the_company_logo(self):
        company = CompanyFactory(name='codetag')
        
        self.assertEqual(company.url('my_file.jpg'), 'media_data/company_image/codetag/my_file.jpg')

class ApplicantTest(TestCase):
    def test_full_name_should_return_a_string_containing_first_and_last_names_separated_by_a_space(self):
        applicant = ApplicantFactory()

        self.assertEqual(applicant.full_name(), 'yo bender')

    def test_full_name_should_return_an_empty_string_when_first_and_last_name_are_empty(self):
        applicant = ApplicantFactory(first_name='', last_name='')

        self.assertEqual(applicant.full_name(), '')

class OfferTest(TestCase):
    def test_valid_time_should_return_true_when_the_offer_valid_time_is_greater_than_current_date(self):
        now = datetime.now()
        tomorrow = now + timedelta(days=1)
        offer = OfferFactory(offer_valid_time = timezone.make_aware(tomorrow, timezone.get_default_timezone()))
        
        self.assertEqual(offer.valid_time(), True)

    def test_get_salary_return_the_correct_info(self):
        offer = OfferFactory(salary=10)

        self.assertEqual(offer.get_salary(), '550.000 - 1.000.000')

    def test_valid_time_should_return_true_when_the_offer_valid_time_is_equal_to_current_date(self):
        now = datetime.now()
        today = datetime(now.year,now.month, now.day, 23,59,59)
        offer = OfferFactory(offer_valid_time = timezone.make_aware(today, timezone.get_default_timezone()))
        
        self.assertEqual(offer.valid_time(), True)

    def test_valid_time_should_retun_false_when_the_offer_valid_time_is_lower_than_curret_date(self):
        now = datetime.now()
        yesterday = now - timedelta(days=1)
        offer = OfferFactory(offer_valid_time = timezone.make_aware(yesterday, timezone.get_default_timezone()))

        self.assertEqual(offer.valid_time(), False)

    def test_days_remaining_function_return_the_correct_number_days(self):
        now = datetime.now()
        next_week = now + timedelta(days=7)
        offer = OfferFactory(offer_valid_time = timezone.make_aware(next_week, timezone.get_default_timezone()))

        self.assertEqual(offer.days_remaining(), 6)

class OfferDetailsViewTest(TestCase):
    def test_GET_should_redirect_http_404_when_the_given_offer_is_finished(self):
        offer = OfferFactory()

        request = HttpRequest()
        request.method = 'GET'
        result = offerDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 404)

    def test_GET_should_redirect_http_404_when_the_given_offer_is_draft(self):

        offer = OfferFactory()

        request = HttpRequest()
        request.method = 'GET'
        result = offerDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 404)

    def test_GET_should_render_the_offer_detail_template_when_the_offer_is_published(self):

        offer = OfferFactory(state=State.published)

        request = HttpRequest()
        request.method = 'GET'
        result = offerDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 200)

    def test_POST_should_redirect_to_home_when_the_given_data_is_valid(self):

        offer = OfferFactory()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['first_name'] = 'yo'
        request.POST['last_name'] = 'bender'
        request.POST['mail'] = 'bender@gmail.com'
        request.POST['observation'] = 'well, none'

        result = offerDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'], '/')
        applicants = Applicant.objects.filter(mail='bender@gmail.com')
        self.assertEqual(applicants.count(),1)
        applicant = applicants[0]
        applications = OfferApplicant.objects.filter(applicant=applicant, offer=offer, state=False, observation='well, none')
        self.assertEqual(applications.count(), 1)

    def test_POST_should_redirect_to_home_when_the_given_data_is_valid_and_should_not_duplicate_the_applicants_when_it_already_exists(self):

        offer = OfferFactory()

        applicant = ApplicantFactory()

        request = HttpRequest()
        request.method = 'POST'
        request.POST['first_name'] = 'yo'
        request.POST['last_name'] = 'bender'
        request.POST['mail'] = 'bender@gmail.com'
        request.POST['observation'] = 'well, none'

        result = offerDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'], '/')
        applicants = Applicant.objects.filter(mail='bender@gmail.com')
        self.assertEqual(applicants.count(),1)
        applicant = applicants[0]
        applications = OfferApplicant.objects.filter(applicant=applicant, offer=offer, state=False, observation='well, none')
        self.assertEqual(applications.count(), 1)

    def test_GET_should_render_the_correct_template_content_when_offer_has_a_clarification(self):
        offer = OfferFactory(state=State.published, clarification="A clarification")

        user = UserFactory()
        user.userprofile.company = offer.company
        user.userprofile.save()

        factory = RequestFactory()
        request = factory.get('/offer/%s' % (offer.slug))
        request.user = user
        result = offerDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Aclaraciones', result.content)


class UserProfileEditViewTest(TestCase):
    def test_POST_should_redirect_to_home_when_the_given_data_is_valid(self):
        
        factory = RequestFactory()
        user = UserFactory()

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
        user = UserFactory()

        request = factory.get('/edit_profile/')
        request.user = user
        result = userProfileEditView(request)

        self.assertEqual(result.status_code, 200)


class CreatePositionViewTest(TestCase):
    def test_POST_save_should_redirect_to_positions_list_when_the_given_data_is_valid(self):
        
        factory = RequestFactory()
        user = UserFactory()

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
        
        user = UserFactory()

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

    def test_GET_should_render_the_create_position_template(self):
        
        user = UserFactory()

        company = CompanyFactory()
        user.userprofile.company = company

        factory = RequestFactory()
        request = factory.get('/positions/create/')
        request.user = user
        result = createPositionView(request)

        self.assertEqual(result.status_code, 200)

    def test_GET_should_display_the_number_of_public_offers_published_by_the_users_company(self):

        from django.db import connection
        connection.cursor().execute("INSERT INTO auth_user(username,password,last_login,is_superuser, first_name, last_name, email, is_staff, is_active, date_joined) VALUES ('admin', 'pass', '2013-6-14', '1', 'name1', 'lastname1', 'email@m.com', '0', '1', '2013-5-14');")

        user1 = UserFactory()

        user2 = UserFactory(username='tu', password=34343)

        company1= CompanyFactory()

        company2= CompanyFactory(name='apple', nit=1234)

        user1.userprofile.company = company1
        user1.userprofile.save()

        user2.userprofile.company = company2
        user2.userprofile.save()

        offer = OfferFactory(company=company1, state=2)

        factory = RequestFactory()
        request = factory.get('/positions/create/')
        request.user = user1
        result = createPositionView(request)

        self.assertIn('Tu tienes 1 oferta publicada', result.content)
        self.assertEqual(result.status_code, 200)


class TerminatePositionViewTest(TestCase):

    def test_GET_should_redirect_positions_list_when_user_company_equals_offer_company(self):
        offer = OfferFactory()

        user = UserFactory()
        user.userprofile.company = offer.company
        user.userprofile.save()

        factory = RequestFactory()
        request = factory.get('/positions/terminate/%s' % (offer.slug))
        request.user = user
        result = terminatePositionView(request, offer.slug)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/list')

    def test_GET_should_redirect_http_404_when_user_company_different_offer_company(self):
        
        company2 = CompanyFactory(name='apple', nit=444)        

        user = UserFactory()
        user.userprofile.company = company2

        offer = OfferFactory()

        factory = RequestFactory()
        request = factory.get('/positions/terminate/%s' % offer.slug)
        request.user = user
        result = terminatePositionView(request, offer.slug)

        self.assertEqual(result.status_code, 404)


class PositionsListViewTest(TestCase):
    def test_GET_should_render_the_positions_list_template(self):
        
        user = UserFactory()

        factory = RequestFactory()
        request = factory.get('/positions/list/')
        request.user = user
        result = positionsListView(request)

        self.assertEqual(result.status_code, 200)


class OldPositionListViewTest(TestCase):
    def test_GET_should_redirect_old_positions_list_template(self):
        
        user = UserFactory()

        factory = RequestFactory()
        request = factory.get('/positions/old/')
        request.user = user
        result = oldPositionsListView(request)

        self.assertEqual(result.status_code, 200)


class CompleteCompanyInfoViewTest(TestCase):
    def test_POST__should_redirect_to_positions_list_when_the_given_data_is_valid(self):
        
        user = UserFactory()

        factory = RequestFactory()
        request = factory.post('/company/complete/')
        request.user = user
        request.POST['nit'] = "123456789-9"
        request.POST['name'] = 'CompanyName'
        request.POST['locationCompany'] = 'Bogota'
        request.POST['website']='company.com'
        request.POST['email']='company@gmail.com'
        request.POST['phone']='(57)233-3433'
        result = completeCompanyInfoView(request)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/list')

    def test_GET_should_render_the_complete_company_info_template(self):
        
        user = UserFactory()

        factory = RequestFactory()
        request = factory.get('/company/complete/')
        request.user = user
        result = completeCompanyInfoView(request)

        self.assertEqual(result.status_code, 200)    


class PlansAndPricingTest(TestCase):
    def test_GET_should_render_plans_and_pricing_page(self):
        request = HttpRequest()
        request.method = 'GET'
        result = plansAndPricingView(request)

        self.assertEqual(result.status_code, 200)


class DashBoardTest(TestCase):
    def test_GET_should_render_position_dash_board(self):
        offer = OfferFactory()

        user = UserFactory()
        user.userprofile.company = offer.company

        factory = RequestFactory()
        request = factory.get('/positions/dashboard/%s' % offer.slug)
        request.user = user
        result = positionDashBoardView(request, offer.slug)

        self.assertEqual(result.status_code, 200)

    def test_GET_should_redirect_http_404_when_user_company_different_offer_company(self):
        
        company2 = CompanyFactory(name='Apple', nit=444)        

        user = UserFactory()
        user.userprofile.company = company2

        offer = OfferFactory()

        factory = RequestFactory()
        request = factory.get('/positions/dashboard/%s' % offer.slug)
        request.user = user
        result = positionDashBoardView(request, offer.slug)

        self.assertEqual(result.status_code, 404)

class SuccessfulApplicationTest(TestCase):
    def test_GET_should_render_activation_success_when_applicant_access_to_the_correct_link_and_applicant_apply_successfully_to_an_offer(self):

        offerApplicant = OfferApplicantFactory()

        request = HttpRequest()
        request.method = 'GET'
        result = successfulApplicationView(request, offerApplicant.token)

        valid_applications = OfferApplicant.objects.filter(state=True, token='Mytoken1234567')

        self.assertEqual(result.status_code, 200)
        self.assertEqual(valid_applications.count(), 1)

class PositionDetailViewTest(TestCase):
    def test_GET_should_render_position_details_template(self):
        offer = OfferFactory(state=State.draft)

        user = UserFactory()
        user.userprofile.company = offer.company

        factory = RequestFactory()
        request = factory.get('positions/details/%s' % offer.slug)
        request.user = user
        result = positionDetailsView(request, offer.slug)
        self.assertEqual(result.status_code, 200)

    def test_GET_should_redirect_http_404_when_user_company_different_offer_company(self):
        
        company2 = CompanyFactory(name='Apple', nit=444)        

        user = UserFactory()
        user.userprofile.company = company2

        offer = OfferFactory()

        factory = RequestFactory()
        request = factory.get('/positions/preview/%s' % offer.slug)
        request.user = user
        result = positionDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 404)

    def test_GET_should_redirect_clarifications_when_position_is_published(self):
        user = UserFactory()
        offer = OfferFactory(state=State.published)
        factory = RequestFactory()
        request = factory.get('/positons/details/%s' % offer.slug)
        request.user = user
        result = positionDetailsView(request, offer.slug)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/clarifications/%s' % offer.slug)


class PurchaseSuccessViewTest(TestCase):
    def test_GET_should_render_the_purchase_success_template(self):
        
        offer = OfferFactory(state=State.draft)

        user = UserFactory()
        user.userprofile.company = offer.company

        factory = RequestFactory()
        request = factory.get('/purchase/success/%s' % offer.slug)
        request.user = user
        result = purchaseSuccessView(request, offer.slug)

        self.assertEqual(result.status_code, 200)

class PurchaseFailViewTest(TestCase):
    def test_GET_should_render_the_purchase_fail_template(self):
        offer = OfferFactory(state=State.draft)

        user = UserFactory()
        user.userprofile.company = offer.company

        factory = RequestFactory()
        request = factory.get('/purchase/fail/%s' % offer.slug)
        request.user = user
        result = purchaseFailView(request, offer.slug)

        self.assertEqual(result.status_code, 200)

class PositionPreviewViewTest(TestCase):
    def test_GET_should_render_position_preview_template_with_correct_button_when_user_have_published_offers(self):

        company = CompanyFactory()

        offer = OfferFactory(offer_valid_time = datetime.now(), state=State.published, job_title='oferta1',company=company)

        offer2 = OfferFactory(offer_valid_time = datetime.now(), state=State.draft, job_title= 'oferta2', company=company)

        user = UserFactory()
        user.userprofile.company = company

        factory = RequestFactory()
        request = factory.get('/positions/preview/%s' % offer2.slug)
        request.user = user
        result = positionPreviewView(request, offer2.slug)
        self.assertIn('Pagar y publicar', result.content)
        self.assertEqual(result.status_code, 200)

    def test_GET_should_render_position_preview_template_with_correct_button_when_user_dont_have_published_offers(self):

        offer2 = OfferFactory(state=State.draft)

        user = UserFactory()
        user.userprofile.company = offer2.company

        factory = RequestFactory()
        request = factory.get('/positions/preview/%s' % offer2.slug)
        request.user = user
        result = positionPreviewView(request, offer2.slug)
        self.assertIn('Publicar Gratis', result.content)
        self.assertEqual(result.status_code, 200)

class PositionClarificationsViewTest(TestCase):
    def test_GET_should_render_position_clarifications_view_template(self):
        offer = OfferFactory(state=State.published)

        user = UserFactory()
        user.userprofile.company = offer.company

        factory = RequestFactory()
        request = factory.get('positions/clarifications/%s' % offer.slug)
        request.user = user
        result = positionClarificationsView(request, offer.slug)
        self.assertEqual(result.status_code, 200)

    def test_GET_should_redirect_http_404_when_user_company_different_offer_company(self):
        
        company2 = CompanyFactory(name='Apple', nit=444)        

        user = UserFactory()
        user.userprofile.company = company2

        offer = OfferFactory()

        factory = RequestFactory()
        request = factory.get('/positions/clarifications/%s' % offer.slug)
        request.user = user
        result = positionClarificationsView(request, offer.slug)

        self.assertEqual(result.status_code, 404)

    def test_GET_should_redirect_http_404_when_offer_state_is_not_published(self):
        
        company2 = CompanyFactory(name='Apple', nit=444)        

        user = UserFactory()
        user.userprofile.company = company2

        offer = OfferFactory(state=State.draft)

        factory = RequestFactory()
        request = factory.get('/positions/clarifications/%s' % offer.slug)
        request.user = user
        result = positionPreviewView(request, offer.slug)

        self.assertEqual(result.status_code, 404)

    def test_POST__should_redirect_to_the_same_offer_clarification_template(self):
        user = UserFactory()

        offer = OfferFactory(state=State.published)

        factory = RequestFactory()
        request = factory.post('/positions/clarifications/%s' % offer.slug)
        request.user = user
        request.POST['aclaration']='This is a clarification'
        result = positionClarificationsView(request, offer.slug)

        self.assertEqual(result.status_code, 302)
        self.assertEqual(result['location'],'/positions/clarifications/%s' % offer.slug)

    def test_GET_should_render_the_correct_template_content_when_offer_has_a_clarification(self):
        offer = OfferFactory(state=State.published, clarification="A clarification")

        user = UserFactory()
        user.userprofile.company = offer.company
        user.userprofile.save()

        factory = RequestFactory()
        request = factory.get('/positions/clarifications/%s' % (offer.slug))
        request.user = user
        result = positionClarificationsView(request, offer.slug)

        self.assertEqual(result.status_code, 200)
        self.assertIn('Aclaraciones', result.content)

TEST_INDEX = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'test_index',
    },
}

class HomeSearchViewTest(FastFixtureTestCase):
    @classmethod
    def setUpClass(cls):
        haystack.connections.reload('default')
        super(HomeSearchViewTest,cls).setUpClass()

    def test_GET_should_render_the_correct_info_when_there_are_highlighted_offers(self):
        offer = OfferFactory(highlighted=True, state=State.published)
        call_command('rebuild_index', interactive=False)

        factory = RequestFactory()
        request = factory.get('/')
        result = homeSearch(request)
        self.assertEqual(result.status_code, 200)
        self.assertIn('higlighted-offer', result.content)

    def test_GET_should_render_the_correct_info_when_there_are_ordinary_offers(self):
        offer = OfferFactory(highlighted=False, state=State.published)
        call_command('rebuild_index', interactive=False)

        factory = RequestFactory()
        request = factory.get('/')
        result = homeSearch(request)
        self.assertEqual(result.status_code, 200)
        self.assertIn('ordinary-offer', result.content)

    def test_GET_should_render_the_correct_info_when_there_are_not_published_offers(self):
        call_command('rebuild_index', interactive=False)
        factory = RequestFactory()
        request = factory.get('/')
        result = homeSearch(request)
        self.assertEqual(result.status_code, 200)        
        self.assertIn('No hay ofertas Publicadas', result.content)
