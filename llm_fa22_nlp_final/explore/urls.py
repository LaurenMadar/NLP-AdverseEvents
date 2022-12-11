from django.urls import path

from . import views 
app_name = 'explore'

urlpatterns = [

    path('', views.ExploreHome.as_view(), name='explorehome'),

    path('', views.Expworkspace.as_view(), name='expworkspace'),


    path('', views.Expsidebar.as_view(), name='expsidebar'),

    path('corps/', views.CorpHomeView.as_view(), name='corphome'),

    path('corps/list/', views.CorpListView.as_view(), name='corplist'),

    path('corpus/<int:pk>/', views.CorpusDetailView.as_view(), name='corpusdetail'),

    path('meds/', views.MedsView.as_view(), name='meds'),
    path('meddetail/<int:pk>/', views.MedDetailView.as_view(), name='meddetail'),

    path('symptoms/', views.SymptomsView.as_view(), name='symptoms'),
    path('symptomdetail/<int:pk>/', views.SymptomDetailView.as_view(), name='symptomdetail'),

    
   
]

