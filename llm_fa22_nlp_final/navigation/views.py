from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

#from .models import Corpus

class IndexView(generic.TemplateView):
    template_name = 'navigation/index.html'
   
