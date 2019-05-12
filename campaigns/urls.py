from django.urls import path
from . import views


app_name = 'campaigns'
urlpatterns = [
    path('', views.index, name='index'),
    path('posted_campaigns', views.posted_campaigns, name='posted_campaigns'),
    path('<int:campaign_id>', views.details, name='details'),
    path('<int:campaign_id>/vote', views.vote, name='vote'),
    path('<int:open_campaign_id>/add_campaign', views.add_campaign, name='add_campaign'),
    # path('<int:id>/results', views.results, name='results'),
]
