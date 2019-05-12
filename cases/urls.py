from django.urls import path
from . import views


app_name = 'cases'
urlpatterns = [
    path('', views.index, name='index'),
    path('new', views.add_case, name='new_case')
]
