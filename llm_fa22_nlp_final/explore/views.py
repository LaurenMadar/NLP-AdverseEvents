from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic


from .models import Corpus, Medication, Symptom

class ExploreHome(generic.TemplateView):
    template_name = 'explore/explorehome.html'
    #context_object_name = 'corphome'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['countcorp'] = Corpus.objects.count()
        context['countmed'] = Medication.objects.count()
        context['countsym'] = Symptom.objects.count()
        context['corphome'] = Corpus.objects.order_by('id')[:5]
        context['medhome'] = Medication.objects.order_by('id')[:8]
        context['symhome'] = Symptom.objects.order_by('id')[:8]
        return context
  

class Expworkspace(generic.TemplateView):
    template_name = 'explore/expworkspace.html'
  

class Expsidebar(generic.TemplateView):
    template_name = 'explore/expsidebar.html'
    

class CorpHomeView(generic.ListView):
    template_name = 'explore/corphome.html'
    context_object_name = 'corphome'
    paginate_by = 20
    def get_queryset(self):
        return Corpus.objects.order_by('id')

class CorpListView(generic.ListView):
    template_name = 'explore/corplist.html'
    context_object_name = 'corplist'
    paginate_by = 25

    def get_queryset(self):
        return Corpus.objects.order_by('title')

class CorpusDetailView(generic.DetailView):
    model = Corpus
    template_name = 'explore/corpusdetail.html'


class MedsView(generic.ListView):
    template_name = 'explore/meds.html'
    context_object_name = 'medlist'
    paginate_by = 50
    
    def get_queryset(self):
        return Medication.objects.order_by('generic_norm')


class MedTable(generic.ListView):
    template_name = 'explore/medtable.html'
    context_object_name = 'medlist'
    paginate_by = 50

    def get_queryset(self):
        return Medication.objects.order_by('generic_norm')


class MedDetailView(generic.DetailView):
    model = Medication
    template_name = 'explore/meddetail.html'


class SymptomsView(generic.ListView):
    template_name = 'explore/symptoms.html'
    context_object_name = 'symptomlist'
    paginate_by = 20

    def get_queryset(self):
        return Symptom.objects.order_by('name_norm')

class SymptomTable(generic.ListView):
    template_name = 'explore/symtable.html'
    context_object_name = 'symptomlist'
    paginate_by = 50

    def get_queryset(self):
        return Symptom.objects.order_by('name_norm')


class SymptomDetailView(generic.DetailView):
    model = Symptom
    template_name = 'explore/symptomdetail.html'
