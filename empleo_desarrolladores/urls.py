from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('empleo_desarrolladores.views',
    url(r'^offer/(?P<slug_offer>[-\w]+)/$', 'offerDetailsView', name="offer_details_view"),
    url(r'^offer/application/(?P<offer_applicant_token>.*)$', 'successfulApplicationView', name="successful_applicant_view"),
    url(r'^positions/list$', 'positionsListView', name="position_list_view"),
    url(r'^positions/details/(?P<slug_offer>[-\w]+)/$', 'positionDetailsView', name="position_detail_view"),
    url(r'^positions/dashboard/(?P<slug_offer>[-\w]+)/$', 'positionDashBoardView', name="position_dashboard_view"),
    url(r'^positions/create/$', 'createPositionView', name='create_position_view'),
    url(r'^positions/preview/(?P<slug_offer>[-\w]+)$', 'positionPreviewView', name='position_preview_view'),
    url(r'^positions/terminate/(?P<slug_offer>[-\w]+)/$', 'terminatePositionView', name='terminate_position_view'),
    url(r'^positions/old/$', 'oldPositionsListView', name='old_positions_list_view'),
    url(r'edit_profile/$', 'userProfileEditView',name="edit_profile"),
    url(r'plans_and_pricing/$', 'plansAndPricingView',name="plans_and_pricing"),
    url(r'^company/complete$', 'completeCompanyInfoView',name="complete_company"),
    url(r'^company/details$', 'companyDetailView',name="company_detail"),
    url(r'^user/card$', 'cardDataView',name="card_data_view"),
    url(r'^purchase$', 'purchaseResultView',name="purchase_result_view"),

)
