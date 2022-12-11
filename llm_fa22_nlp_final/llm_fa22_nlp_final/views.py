from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic

#from .models import Corpus

class Home(generic.TemplateView):
    template_name = 'home.html'
   
class Resources(generic.TemplateView):
    template_name = 'resources.html'
   
class Footer(generic.TemplateView):
    template_name = 'footer.html'
   
class Headernav(generic.TemplateView):
    template_name = 'headernav.html'
   
class Resources(generic.TemplateView):
    template_name = 'resources.html'
   
class Contactinfo(generic.TemplateView):
    template_name = 'contactinfo.html'
   
class Sidebar(generic.TemplateView):
    template_name = 'sidebar.html'
   
class Overview(generic.TemplateView):
    template_name = 'overview.html'
   
