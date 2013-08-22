from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import DetailView
from models import Offer, Company, UserProfile, Applicant, OfferApplicant
from forms import CompanyForm, OfferForm, UserProfileForm, ApplicantForm, MySearchForm, CreateOfferForm
from django.contrib.auth import get_user_model
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

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


def offerDetailsView(request, id_offer):
    offer = Offer.objects.get(id=id_offer)
    offerApplicant = OfferApplicant()

    if request.method == "POST":
        form = ApplicantForm(request.POST)
        if form.is_valid():
            mail = form.cleaned_data['mail']
            a = Applicant()
            a.first_name = form.cleaned_data['first_name']
            a.last_name = form.cleaned_data['last_name']
            a.mail = mail

            if not Applicant.objects.filter(mail=a.mail).exists():
                a.save()
            offerApplicant.applicant = Applicant.objects.get(mail=mail)
            offerApplicant.offer = offer
            offerApplicant.observation = form.cleaned_data['observation']
            offerApplicant.save()
            return HttpResponseRedirect("/")
    if request.method == "GET":
        if offer.state == 1 or offer.state == 0:
            return HttpResponseRedirect("/")
        form = ApplicantForm()
    ctx = {'form': form, 'offer': offer}
    return render_to_response('offer_detail.html', ctx, context_instance=RequestContext(request))


@login_required()
def createPositionView(request):
    user = UserProfile.objects.get(id=request.user.id)
    company = user.company
    if request.method == 'POST':
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer = Offer()
            offer.job_title = form.cleaned_data['job_title']
            offer.location = form.cleaned_data['location']
            offer.type_contract = form.cleaned_data['type_contract']
            offer.salary = form.cleaned_data['salary']
            if '_save' in request.POST:
                offer.state = 0
            elif '_publish' in request.POST:
                offer.state = 2
            offer.offer_valid_time = form.cleaned_data['offer_valid_time']
            skills = form.cleaned_data['skills']
            offer.job_description = form.cleaned_data['job_description']
            offer.company = company
            offer.save()

            for skill in skills:
                offer.skills.add(skill)
            return HttpResponseRedirect("/positions/list")
    else:
        form = CreateOfferForm()
    ctx = {'form': form}
    return render_to_response('createPosition.html', ctx, context_instance=RequestContext(request))


@login_required()
def positionDetailsView(request, id_offer):
    user = UserProfile.objects.get(id=request.user.id)
    company = user.company
    offer = Offer.objects.get(id=id_offer)
    applicants = OfferApplicant.objects.filter(offer=offer)
    if request.method == "POST":
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer.job_title = form.cleaned_data['job_title']
            offer.location = form.cleaned_data['location']
            offer.type_contract = form.cleaned_data['type_contract']
            offer.salary = form.cleaned_data['salary']
            if '_save' in request.POST:
                offer.state = 0
            elif '_publish' in request.POST:
                offer.state = 2
            offer.offer_valid_time = form.cleaned_data['offer_valid_time']
            skills = form.cleaned_data['skills']
            offer.job_description = form.cleaned_data['job_description']
            offer.company = company
            offer.save()
            for skill in skills:
                offer.skills.add(skill)
            return HttpResponseRedirect("/positions/list")
    if request.method == "GET":
        if offer.company != user.company:
            return HttpResponseRedirect("/positions/list")

        s = []
        for skill in offer.skills.all():
            s.append(skill.name)

        form = CreateOfferForm(initial={
            'job_title': offer.job_title,
            'location': offer.location,
            'type_contract': offer.type_contract,
            'salary': offer.salary,
            'offer_valid_time': offer.offer_valid_time,
            'skills': ','.join(s),
            'job_description': offer.job_description,
        })
    ctx = {'form': form, 'offer': offer, 'applicants': applicants}
    return render_to_response('position_detail.html', ctx, context_instance=RequestContext(request))


@login_required()
def terminatePositionView(request, id_offer):
    user = UserProfile.objects.get(id=request.user.id)
    offer = Offer.objects.get(id=id_offer)
    if offer.company != user.company:
            return HttpResponseRedirect("/positions/list")
    offer.state = 1
    offer.save()
    return HttpResponseRedirect('/positions/list')


@login_required()
def positionsListView(request):
    user = UserProfile.objects.get(user=request.user)
    company = Company.objects.get(id=user.company.id)
    offers = Offer.objects.filter(company=company)
    ctx = {'offers': offers}
    return render_to_response('positions.html', ctx, context_instance=RequestContext(request))


@login_required()
def oldPositionsListView(request):
    user = UserProfile.objects.get(id=request.user.id)
    offers = Offer.objects.filter(state=1, company=user.company)
    ctx = {'offers': offers}
    return render_to_response('old_positions.html', ctx, context_instance=RequestContext(request))
