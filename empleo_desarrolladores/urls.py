from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('empleo_desarrolladores.views',
    url(r'^offer/(?P<id_offer>.*)/$', 'offerDetailsView', name="offer_details_view"),
    url(r'^positions/list$', 'positionsListView', name="position_list_view"),
    url(r'^positions/details/(?P<id_offer>.*)/$', 'positionDetailsView', name="position_detail_view"),
    url(r'^positions/create/$', 'createPositionView', name='create_position_view'),
    url(r'^positions/terminate/(?P<id_offer>.*)/$', 'terminatePositionView', name='terminate_position_view'),
    url(r'^positions/old/$', 'oldPositionsListView', name='old_positions_list_view'),
    url(r'edit_profile/$', 'userProfileEditView',name="edit_profile"),
    url(r'plans_and_pricing/$', 'plansAndPricingView',name="plans_and_pricing"),
    url(r'^company/complete$', 'completeCompanyInfoView',name="complete_company"),
    url(r'^company/details$', 'companyDetailView',name="company_detail"),

)
