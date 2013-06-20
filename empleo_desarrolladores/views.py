from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView 
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from models import Developer, Offer, Company, UserProfile
from forms import DeveloperForm, CompanyForm, OfferForm, UserProfileForm
from django.contrib.auth import get_user_model
from django.views.generic.base import View
from django.shortcuts import render_to_response

class Home(View):
    def get(self, request):
        ofertas = Offer.objects.all()
        return render_to_response('home.html', {'ofertas': ofertas})

class DeveloperList(ListView):
    model = Developer
    template_name = 'developer_list.html'

class DeveloperCreate(CreateView):
    model = Developer
    form_class = DeveloperForm
    template_name = 'developer_create.html'
    success_url = reverse_lazy('developer_list')

class DeveloperUpdate(UpdateView):
    model = Developer
    template_name = 'developer_create.html'
    success_url = reverse_lazy('developer_list')

class DeveloperDelete(DeleteView):
    model = Developer
    template_name = 'developer_delete.html'
    success_url = reverse_lazy('developer_list')

class CompanyList(ListView):
    model = Company
    template_name = 'company_list.html'

class CompanyCreate(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company_create.html'
    success_url = reverse_lazy('company_list')

class CompanyUpdate(UpdateView):
    model = Company
    template_name = 'company_create.html'
    success_url = reverse_lazy('company_list')

class CompanyDelete(DeleteView):
    model = Company
    template_name = 'company_delete.html'
    success_url = reverse_lazy('company_list')

class OfferList(ListView):
    model = Offer
    template_name = 'offer_list.html'

class OfferCreate(CreateView):
    model = Offer
    form_class = OfferForm
    template_name = 'offer_create.html'
    success_url = reverse_lazy('offer_list')

class OfferUpdate(UpdateView):
    model = Offer
    template_name = 'offer_create.html'
    success_url = reverse_lazy('offer_list')

class OfferDelete(DeleteView):
    model = Offer
    template_name = 'offer_delete.html'
    success_url = reverse_lazy('offer_list')

class OfferDetailsView(DetailView):
    template_name = 'offer_detail.html'
    model = Offer

class UserProfileDetailView(DetailView):
    model = get_user_model()
    slug_field = "username"
    template_name = "user_detail.html"
    
    def get_object(self, queryset=None):
        user = super(UserProfileDetailView, self).get_object(queryset)
        UserProfile.objects.get_or_create(user=user)
        return user

class UserProfileEditView(UpdateView):
    model = UserProfile
    form_class = UserProfileForm
    template_name = "edit_profile.html"
    
    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]
    
    def get_success_url(self):
        return reverse("profile", kwargs={"slug": self.request.user})
