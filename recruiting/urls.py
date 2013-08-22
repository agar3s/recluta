from django.conf.urls.defaults import patterns, include, url
from empleo_desarrolladores.views import  UserProfileEditView, UserProfileDetailView
from empleo_desarrolladores.views import CompanyList, CompanyCreate, CompanyUpdate, CompanyDelete, CompanyUpdate
from django.contrib.auth.decorators import login_required as auth
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('empleo_desarrolladores.urls')),
    url(r'^',include('search.urls')),
    url(r'^company/list$', CompanyList.as_view(), name='company_list'),
    url(r'^company/add/$', CompanyCreate.as_view(), name='company_add'),
    url(r'company/(?P<pk>\d+)/$', CompanyUpdate.as_view(), name='company_update'),
    url(r'company/(?P<pk>\d+)/delete/$', CompanyDelete.as_view(), name='company_delete'),

    # Registration Urls

    url(r"^login/$", "django.contrib.auth.views.login",{"template_name": "registration/login.html"}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include("registration.urls")),
    # Aun falta editar la vista de edicion de la cuenta
    url(r'edit_profile/$', auth(UserProfileEditView.as_view()),name="edit_profile"),
)
