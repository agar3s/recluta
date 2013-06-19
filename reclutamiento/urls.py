from django.conf.urls import patterns, include, url
from empleo_desarrolladores.views import DeveloperList, DeveloperCreate, DeveloperUpdate, DeveloperDelete, DeveloperUpdate
from empleo_desarrolladores.views import  UserProfileEditView, UserProfileDetailView
from empleo_desarrolladores.views import CompanyList, CompanyCreate, CompanyUpdate, CompanyDelete, CompanyUpdate
from empleo_desarrolladores.views import OfferList, OfferCreate, OfferUpdate, OfferDelete, OfferUpdate
from django.contrib.auth.decorators import login_required as auth
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', OfferList.as_view(), name='home'),
    url(r'^developer/list$', DeveloperList.as_view(), name='developer_list'),
    url(r'^developer/add/$', DeveloperCreate.as_view(), name='developer_add'),
    url(r'developer/(?P<pk>\d+)/$', DeveloperUpdate.as_view(), name='developer_update'),
    url(r'developer/(?P<pk>\d+)/delete/$', DeveloperDelete.as_view(), name='developer_delete'),

    url(r'^company/list$', CompanyList.as_view(), name='company_list'),
    url(r'^company/add/$', CompanyCreate.as_view(), name='company_add'),
    url(r'company/(?P<pk>\d+)/$', CompanyUpdate.as_view(), name='company_update'),
    url(r'company/(?P<pk>\d+)/delete/$', CompanyDelete.as_view(), name='company_delete'),

    url(r'^offer/list$', OfferList.as_view(), name='offer_list'),
    url(r'^offer/add/$', OfferCreate.as_view(), name='offer_add'),
    url(r'offer/(?P<pk>\d+)/$', OfferUpdate.as_view(), name='offer_update'),
    url(r'offer/(?P<pk>\d+)/delete/$', OfferDelete.as_view(), name='offer_delete'),
    
    url(r"^login/$", "django.contrib.auth.views.login",
    {"template_name": "registration/login.html"}, name="login"),
    url(r"^logout/$", "django.contrib.auth.views.logout_then_login",
    name="logout"),

    url(r"^accounts/", include("registration.backends.simple.urls")),

    url(r"^users/(?P<slug>\w+)/$", UserProfileDetailView.as_view(),
        name="profile"),
    
    url(r"edit_profile/$", auth(UserProfileEditView.as_view()),
        name="edit_profile")
    
    # url(r'^$', 'Reclutamiento.views.home', name='home'),
    # url(r'^Reclutamiento/', include('Reclutamiento.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
