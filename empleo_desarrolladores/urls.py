from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('empleo_desarrolladores.views',
    url(r'^offer/(?P<id_offer>.*)/$', 'offerDetailsView', name="offer_details_view"),
    url(r'^positions/list$', 'positionsListView', name="position_list_view"),
    url(r'^positions/details/(?P<id_offer>.*)/$', 'positionDetailsView', name="position_detail_view"),
    url(r'^positions/create/$', 'createPositionView', name='create_position_view'),
    url(r'^positions/terminate/(?P<id_offer>.*)/$', 'terminatePositionView', name='terminate_position_view'),
    url(r'^positions/old/$', 'oldPositionsListView', name='old_positions_list_view'),
)
