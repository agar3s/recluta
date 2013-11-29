from models import Offer, Company, OfferApplicant
from forms import CompanyForm, ApplicantForm, CreateOfferForm, UserEditForm, CreateOfferFormLoader, CompanyFormLoader, UserEditFormLoader, ClarificationForm
from django.shortcuts import render_to_response
from django.template import RequestContext, Context, loader
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import get_object_or_404
from messaging_handler import OfferApplicantMessage
from django.template import defaultfilters
from models_factory import ApplicantFactory, OfferApplicantFactory, UserProfileFactory, OfferFactory, CompanyFactory, State
from datetime import datetime
from django.http import HttpResponse

def error404(request):
    template = loader.get_template('404.html')
    html = template.render(Context())

    return HttpResponseNotFound(html)

def plansAndPricingView(request):
    return render_to_response('plans_and_pricing.html')

def offerDetailsView(request, slug_offer):
    offer = get_object_or_404( Offer, slug=slug_offer)

    if request.method == "POST":
        form = ApplicantForm(request.POST, request.FILES)
        if form.is_valid():

            applicant_factory = ApplicantFactory()
            applicant = applicant_factory.get_instance_form(form=form)            

            offer_applicant_factory = OfferApplicantFactory()
            offer_applicant = offer_applicant_factory.get_instance_form(applicant=applicant, offer=offer, form=form)

            offer_applicant_message = OfferApplicantMessage()
            offer_applicant_message.send(offer_applicant)

            return HttpResponseRedirect("/")
    if request.method == "GET":
        if offer.is_finished() or offer.is_draft():
            return error404(request)
        form = ApplicantForm()
    applicants_number = OfferApplicant.objects.filter(offer=offer, state=True).count()
    ctx = {'form': form, 'offer': offer, 'applicants_number':applicants_number}
    return render_to_response('offer_detail.html', ctx, context_instance=RequestContext(request))

@login_required()
def userProfileEditView(request):
    user = request.user
    if request.method== 'POST':
        form = UserEditForm(request.POST)
        if form.is_valid():
            user_profile_factory = UserProfileFactory()
            user_profile_factory.save_instance_form(form=form, user=user)
            return HttpResponseRedirect("/")
    else:
        form_loader = UserEditFormLoader()
        form = form_loader.load_initial_data(user)
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
            offer_slug = defaultfilters.slugify(company.name+'-'+form.cleaned_data['job_title'])            

            offer_factory = OfferFactory()
            offer = offer_factory.get_instance_form(company=company, offer_slug=offer_slug, form=form)

            return HttpResponseRedirect("/positions/preview/%s" % (offer.slug))
    else:
        form = CreateOfferForm()
    offers = len(Offer.objects.filter(company=company,state=State.published))
    ctx = {'form': form, 'offers':offers}
    return render_to_response('createPosition.html', ctx, context_instance=RequestContext(request))

@login_required()
def positionPreviewView(request, slug_offer):
    offer = get_object_or_404( Offer, slug=slug_offer)
    user = request.user.userprofile
    if request.method == "GET":
        if offer.company != user.company:
            return error404(request)
    if request.method == "POST":
        if '_free_publish' in request.POST:
            offer.set_state('published')
            offer.save()
            return HttpResponseRedirect('/purchase/success/%s' % offer.slug)
    published_offers = Offer.objects.filter(state=State.published, company=user.company).count()
    ctx = {'offer': offer, 'published_offers': published_offers}
    return render_to_response('position_preview.html', ctx, context_instance=RequestContext(request))


@login_required()
def positionDetailsView(request, slug_offer):
    user = request.user.userprofile
    company = user.company
    offer = get_object_or_404(Offer, slug=slug_offer)
    applicants = OfferApplicant.objects.filter(offer=offer)

    if offer.is_published():
        return HttpResponseRedirect("/positions/clarifications/%s" % (offer.slug))

    if request.method == 'POST':
        form = CreateOfferForm(request.POST)
        if form.is_valid():
            offer_factory = OfferFactory()
            offer_factory.update_instance_form(offer=offer, form=form, company=company)

            return HttpResponseRedirect("/positions/preview/%s" % (offer.slug))
    if request.method == 'GET':
        if offer.company != user.company:
            return error404(request)

        form_loader = CreateOfferFormLoader()
        form = form_loader.load_initial_data(offer)

    offers = len(Offer.objects.filter(company=company,state=State.published))
    ctx = {'form': form, 'offer': offer, 'applicants': applicants, 'offers':offers}
    return render_to_response('createPosition.html', ctx, context_instance=RequestContext(request))

@login_required()
def positionClarificationsView(request, slug_offer):
    offer = get_object_or_404(Offer, slug=slug_offer)
    form = ClarificationForm()

    if offer.clarification:
        form = ClarificationForm(initial={
            'aclaration':offer.clarification})

    if request.method == 'POST':
        form = ClarificationForm(request.POST)
        if form.is_valid():
            offer.clarification = form.cleaned_data['aclaration']
            offer.save()
            return HttpResponseRedirect("/positions/clarifications/%s" % (offer.slug))

    user = request.user.userprofile
    if request.method == "GET":
        if not offer.is_published():
            return error404(request)
        if offer.company != user.company:
            return error404(request)

    ctx = {'form': form, 'offer':offer}
    return render_to_response('position_clarification.html', ctx, context_instance=RequestContext(request))

@login_required()
def terminatePositionView(request, slug_offer):

    user = request.user.userprofile
    offer = get_object_or_404(Offer, slug=slug_offer)

    if offer.company != user.company:
        return error404(request)
    offer.set_state('finished')
    offer.offer_valid_time = datetime.now()
    offer.save()
    return HttpResponseRedirect('/positions/list')


@login_required()
def positionsListView(request):
    user = request.user.userprofile
    if user.company:
        company = Company.objects.get(id=user.company.id)
        offers = Offer.objects.filter(company=company).order_by('-state')
        published_and_draft_offers = Offer.objects.filter(state=State.draft, company=company).count() + Offer.objects.filter(state = State.published, company=company).count()
    else:
        offers = []
        published_and_draft_offers = 0
    
    ctx = {'offers': offers, 'published_and_draft_offers': published_and_draft_offers}
    return render_to_response('positions.html', ctx, context_instance=RequestContext(request))


@login_required()
def oldPositionsListView(request):
    user = request.user.userprofile
    offers = Offer.objects.filter(state=State.finished, company=user.company)
    ctx = {'offers': offers}
    return render_to_response('old_positions.html', ctx, context_instance=RequestContext(request))

@login_required()
def completeCompanyInfoView(request):
    user = request.user.userprofile
  
    if request.method=='POST':
        form = CompanyForm(request.POST)
        if form.is_valid():
            company_factory = CompanyFactory()
            company_factory.save_instance_form(form=form, user=user)
            
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
            company_factory = CompanyFactory()
            company_factory.update_instance_form(form=form, company=company)
            
            return HttpResponseRedirect('/positions/list')
    else:
        form_loader = CompanyFormLoader()
        form = form_loader.load_initial_data(company)

    ctx={'form':form, 'company':company}
    return render_to_response('company_edit.html', ctx, context_instance=RequestContext(request))

@login_required()
def positionDashBoardView(request, slug_offer):
    user = request.user.userprofile
    offer = get_object_or_404( Offer, slug=slug_offer)
    
    applications = OfferApplicant.objects.filter(offer=offer)

    if user.company != offer.company:
        return error404(request)
    
    ctx = {'offer':offer, 'applications':applications}
    return render_to_response('position_dashboard.html', ctx, context_instance=RequestContext(request))

def successfulApplicationView(request, offer_applicant_token):
    offerApplicant = get_object_or_404(OfferApplicant, token=offer_applicant_token)
    offerApplicant.state = True
    offerApplicant.save()
    ctx ={'offerapplicant':offerApplicant}
    return render_to_response('offer_successful_application.html', ctx, context_instance=RequestContext(request))


@login_required()
def purchaseSuccessView(request, slug_offer):

    offer = get_object_or_404( Offer, slug=slug_offer)
    user = request.user.userprofile
    published_offers = Offer.objects.filter(company=user.company, state=State.published).count()
    
    if offer.company != user.company:
        return error404(request)

    ctx = {'published_offers':published_offers, 'offer': offer}
    return render_to_response('purchase_success.html', ctx, context_instance=RequestContext(request))

@login_required()
def purchaseFailView(request, slug_offer):

    offer = get_object_or_404( Offer, slug=slug_offer)
    user = request.user.userprofile
    published_offers = Offer.objects.filter(company=user.company, state=State.published).count()

    if offer.company != user.company:
        return error404(request)

    ctx = {'published_offers':published_offers, 'offer': offer}
    return render_to_response('purchase_fail.html', ctx, context_instance=RequestContext(request))

@login_required()
def resumeDownloadView(request, token):

    offer_applicant = get_object_or_404(OfferApplicant, token=token)
    user = request.user.userprofile

    if user.company != offer_applicant.offer.company:
        return error404(request)

    filename = offer_applicant.resume.name.split('/')[-1]
    response = HttpResponse(offer_applicant.resume, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def processorUrlSite(request):
    ctx = {
        'site_url': settings.SITE_URL,
        'site_name': settings.SITE_NAME,
    }
    return ctx
