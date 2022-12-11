from django.urls import path

from . import views
app_name = 'search'

urlpatterns = [
    path('', views.IndexView.as_view(), name='search'),
    path('results/<int:limit>/', views.ResultsAllView.as_view(), name='results'),
    path('medvocab/', views.MedVocab.as_view(), name='medvocab'),
    path('symvocab/', views.SymVocab.as_view(), name='symvocab'),
]

