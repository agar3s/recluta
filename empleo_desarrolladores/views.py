from models import Offer, Company, Applicant, OfferApplicant
from forms import CompanyForm, ApplicantForm, CreateOfferForm, UserEditForm
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404


def error404(request):
    template = loader.get_template('404.html')
    html = template.render(Context())

    return HttpResponseNotFound(html)

def plansAndPricingView(request):
    return render_to_response('plans_and_pricing.html')

def offerDetailsView(request, slug_offer):
    offer = get_object_or_404( Offer, slug=slug_offer)
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
            return error404(request)
        form = ApplicantForm()
    ctx = {'form': form, 'offer': offer}
    return render_to_response('offer_detail.html', ctx, context_instance=RequestContext(request))

@login_required()
def userProfileEditView(request):
    user = request.user
    if request.method== 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            return HttpResponseRedirect("/")
    else:
        form = UserEditForm(initial={
            'first_name':user.first_name,
            'last_name':user.last_name,
            'email':user.email,
            })
    ctx = {'form':form}
    return render_to_response('edit_profile.html',ctx,context_instance=RequestContext(request))


@login_required()
def createPositionView(request):

    user = request.user.userprofile
    company = user.company
    if not company:
        return HttpResponseRedirect('/positions/list')
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
            offer.offer_valid_time = datetime.now() + timedelta(days=30)
            skills = form.cleaned_data['skills']
            offer.job_description = form.cleaned_data['job_description']
            offer.company = company
            offer.save()

            for skill in skills:
                offer.skills.add(skill)
            return HttpResponseRedirect("/positions/list")
    else:
        form = CreateOfferForm()
    offers = len(Offer.objects.filter(company=company,state=2))
    ctx = {'form': form, 'offers':offers}
    return render_to_response('createPosition.html', ctx, context_instance=RequestContext(request))



@login_required()
def positionDetailsView(request, slug_offer):
    user = request.user.userprofile
    company = user.company
    offer = get_object_or_404(Offer, slug=slug_offer)
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
            offer.offer_valid_time = datetime.now() + timedelta(days=30)
            skills = form.cleaned_data['skills']
            offer.job_description = form.cleaned_data['job_description']
            offer.company = company
            offer.save()
            for skill in skills:
                offer.skills.add(skill)
            return HttpResponseRedirect("/positions/list")
    if request.method == "GET":
        if offer.company != user.company:
            return error404(request)

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
    offers = len(Offer.objects.filter(company=company,state=2))
    ctx = {'form': form, 'offer': offer, 'applicants': applicants, 'offers':offers}
    return render_to_response('position_detail.html', ctx, context_instance=RequestContext(request))


@login_required()
def terminatePositionView(request, slug_offer):
    user = request.user.userprofile
    offer = get_object_or_404(Offer, slug=slug_offer)
    if offer.company != user.company:
        return error404(request)
    offer.state = 1
    offer.save()
    return HttpResponseRedirect('/positions/list')


@login_required()
def positionsListView(request):
    user = request.user.userprofile
    if user.company:
        company = Company.objects.get(id=user.company.id)
        offers = Offer.objects.filter(company=company).order_by('-state')
    else:
        offers = []
    ctx = {'offers': offers}
    return render_to_response('positions.html', ctx, context_instance=RequestContext(request))


@login_required()
def oldPositionsListView(request):
    user = request.user.userprofile
    offers = Offer.objects.filter(state=1, company=user.company)
    ctx = {'offers': offers}
    return render_to_response('old_positions.html', ctx, context_instance=RequestContext(request))

@login_required()
def completeCompanyInfoView(request):
    user = request.user.userprofile
    company = Company()
    if request.method=='POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company.nit = form.cleaned_data['nit']
            company.name = form.cleaned_data['name']
            company.location = form.cleaned_data['locationCompany']
            company.website = form.cleaned_data['website']
            company.email = form.cleaned_data['email']
            company.phone = form.cleaned_data['phone']
            company.save()
            user.company = company
            user.save()
            return HttpResponseRedirect('/positions/list')
    else:
        form = CompanyForm()
    ctx = {'form':form}
    return render_to_response('company_form.html', ctx, context_instance=RequestContext(request))

@login_required()
def companyDetailView(request):
    user = request.user.userprofile
    company = user.company
    if request.method=='POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company.nit = form.cleaned_data['nit']
            company.name = form.cleaned_data['name']
            company.location = form.cleaned_data['locationCompany']
            company.website = form.cleaned_data['website']
            company.email = form.cleaned_data['email']
            company.phone = form.cleaned_data['phone']
            company.save()
            return HttpResponseRedirect('/positions/list')
    else:
        form = CompanyForm(initial={
                'nit':company.nit,
                'name':company.name,
                'locationCompany':company.location,
                'website':company.website,
                'email':company.email,
                'phone':company.phone,
            })
    ctx={'form':form, 'company':company}
    return render_to_response('company_edit.html', ctx, context_instance=RequestContext(request))

def positionDashBoardView(request, offer_slug):
    offer = Offer.objects.get(slug=offer_slug)
    ctx = {'offer':offer}
    return render_to_response('position_dashboard.html', ctx, context_instance=RequestContext(request))

def processorUrlSite(request):
    ctx = {
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }
    return ctx
