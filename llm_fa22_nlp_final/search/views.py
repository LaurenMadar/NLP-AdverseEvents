from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
import pandas as pd

from .models import AllSearch
theSearch = AllSearch()
totalCorp = len(theSearch.corpuslist)

class IndexView(generic.TemplateView):
    template_name = 'search/search.html'
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['numcorp'] = totalCorp
            return context

class ResultsAllView(generic.TemplateView):
    template_name = 'search/resultsall.html'
    print("Initializing result view...")
    limit = 10
    def get_context_data(self, **kwargs):
        print("Getting result context...")
        context = super().get_context_data(**kwargs)
        self.limit = context['limit'] #grab from the URL
        df = theSearch.getResults(self.limit)
        context['numsearched'] = len(df)
        context['results'] = df.loc[df["potentialae"]== True , ]
        context['numae'] = len(context['results'])
        return context

class MedVocab(generic.TemplateView):
    template_name = 'search/medvocab.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medvocab'] = theSearch.medvocab
        return context

class SymVocab(generic.TemplateView):
    template_name = 'search/symvocab.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['symvocab'] = theSearch.symvocab
        return context
