from django.db import models
import ast

import pandas as pd
import nltk
import re
import numpy as np
from bs4 import BeautifulSoup as bs
from collections import Counter
import text_normalizer as tn 
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from spacy.matcher import Matcher
nlp = spacy.load("en_core_web_sm")

from explore.models import Corpus, Medication, Symptom


def get_matched_terms(doc, matches):
    matched_terms = []
    for ma in matches:
        match_id, start, end = ma
        # Get the matched span
        matched_span = doc[start:end]
        matched_terms.append(matched_span.text)
    return matched_terms
def performSearch(corp_df,med_df,sym_df, matcher1, matcher2):
        medresults = []
        medresult_terms = []
        medresultmeta = []
        symresults = []
        symresult_terms = []
        symresultmeta = []
        potentialae = []
        
        subsetM = med_df[['id','brand_norm','generic_norm', 'compound_norm', 'labeler']]
        
        entries = corp_df['corpus_norm']

        for patient_note in entries:
            pn_doc = nlp(patient_note)
            pn_medmatches = matcher1(pn_doc)
            pn_symmatches = matcher2(pn_doc)

            pn_medterms = get_matched_terms(pn_doc, pn_medmatches)
            pn_symterms = get_matched_terms(pn_doc, pn_symmatches)

            
            medresults.append(len(pn_medmatches)>0)
            medresult_terms.append(pn_medterms)
            
            filteredm = med_df.loc[(med_df["compound_norm"].isin(pn_medterms)) | (med_df["brand_norm"].isin(pn_medterms)) | (med_df["generic_norm"].isin(pn_medterms)) , ["id", "compound_norm", "brand_norm", "generic_norm", "labeler"]]
            
            medresultmeta.append(filteredm)

            symresults.append(len(pn_symmatches)>0)
            symresult_terms.append(pn_symterms)
            
            filtereds = sym_df.loc[sym_df["name_norm"].isin(pn_symterms) , ["id", "name_norm"]]
            #print(len(filtereds))
            symresultmeta.append(filtereds)

            isAE = ((len(filteredm)>0) & (len(filtereds)>0))
            potentialae.append(isAE)
        

        corp_df['medresults']= medresults
        corp_df['medresult_terms'] = medresult_terms
        corp_df['medresultmeta'] = medresultmeta
        corp_df['symresults'] = symresults
        corp_df['symresult_terms'] = symresult_terms
        corp_df['symresultmeta'] = symresultmeta
        corp_df['potentialae'] = potentialae
        return corp_df

def createMatchers( medvocab, symvocab):
        medmatcher = Matcher(nlp.vocab)
        for med in medvocab:
            pattern = [[{"TEXT": med}]]
            medmatcher.add("MED_" + med, pattern)

        symmatcher = Matcher(nlp.vocab)
        for sym in symvocab:
            pattern = [[{"TEXT": sym}]]
            symmatcher.add("SYM_" + sym, pattern)

        return medmatcher, symmatcher
def createSymVocab(sym_df): 
        symptom_vocab = [] 

        for wordl in sym_df["wordlist"]:
            wordlist = ast.literal_eval(wordl)
            symptom_vocab.extend(wordlist)
    
        
        symptom_vocab = list(dict.fromkeys(symptom_vocab)) #get rid of duplicates
        return symptom_vocab
def createMedVocab(med_df):
        med_vocab = [] 
        for wordl in med_df["generic_norm"]:
          if isinstance(wordl, str):
            w = wordl.split(" ")
            med_vocab.extend(w)
    
        for wordl in med_df["brand_norm"]:
            if isinstance(wordl, str):
                #w = wordl.split(" ") # Keep proprietary names as a whole term
                med_vocab.append(wordl)
            
        med_vocab = [word for word in med_vocab if len(word) > 3]

        med_vocab = list(dict.fromkeys(med_vocab)) #get rid of duplicates

        med_vocab = tn.normalize_corpus(corpus=med_vocab, html_stripping=True, contraction_expansion=True, 
                                        accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                        text_stemming=False, special_char_removal=True, remove_digits=True, 
                                        stopword_removal=True)

        med_vocab = list(filter(None, med_vocab)) # get rid of empty strings
        return med_vocab;
class AllSearch(models.Model):
    limit = 10
    medvocab = []
    symvocab = []

    title = "Search All"

    medmatcher = []
    symmatcher = []
    initialized = False

    corpuslist = Corpus.objects.order_by('id')
    medlist = Medication.objects.order_by('id')
    symlist = Symptom.objects.order_by('id')

    def initSearch(self, limit=250):
        print('Initializing search... ')
   

        self.corp_df = pd.DataFrame(list(self.corpuslist.values())).head(limit)
        self.med_df = pd.DataFrame(list(self.medlist.values()))
        self.sym_df = pd.DataFrame(list(self.symlist.values()))
        self.medvocab = createMedVocab(self.med_df)
        self.symvocab = createSymVocab(self.sym_df)
        self.medmatcher, self.symmatcher = createMatchers(self.medvocab,self.symvocab)
        return self

    def getResults(self, limit=250):
        if limit != self.limit:
            self.initialized = False
            self.limit = limit

        if (self.initialized == False):  
            self.initSearch(limit)
            print('Getting results... first ' + str(limit))
            #self.initialized = True
            self.results = performSearch(self.corp_df, self.med_df, self.sym_df, self.medmatcher, self.symmatcher)
            self.initialized = True
        else:
            print('Already ran search...')
  
        print('Results done.')
        return self.results

    def __str__(self):
        return self.title

    def fields(self):
        return self._meta.get_fields()

    

