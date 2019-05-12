from django.urls import path, include
from django.conf.urls import url
from . import views
from . import views as core_views
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    #path('', include('django.contrib.auth.urls')),
    #path('signup/', views.SignUp.as_view(), name='signup'),
    path('signup/', views.register, name='signup'),
    path('<int:user_id>/profile/', views.user_profile_view, name='profile'),
    path('<int:user_id>/profile/edit/', views.edit_profile_view, name='edit_profile'),

    #path('account_activation_sent/', core_views.account_activation_sent, name='account_activation_sent'),
    #path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', core_views.activate, name='activate'),

    url(r'^account_activation_sent/$', core_views.account_activation_sent, name='account_activation_sent'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        core_views.activate, name='activate'),
]
