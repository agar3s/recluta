from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^',include('empleo_desarrolladores.urls')),
    url(r'^',include('search.urls')),
    # Registration Urls
    url(r"^login/$", "django.contrib.auth.views.login",{"template_name": "registration/login.html"}, name="login"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^accounts/', include("registration.urls")),
    
)

