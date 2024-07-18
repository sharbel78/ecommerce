from django.urls import path
from . import views

urlpatterns = [

    path('',views.SearchResult,name='SearchResult'),

]