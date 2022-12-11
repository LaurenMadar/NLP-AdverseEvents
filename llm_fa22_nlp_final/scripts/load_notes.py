import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm_fa22_nlp_final.settings")
django.setup()

import pandas as pd
import datetime
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

from explore.models import Corpus
def run():
    patnotes_df = pd.read_csv('./data/patient_notes.csv') # simpler, larger dataset

    mtsamples_df = pd.read_csv('./data/mtsamples.csv') # more complex but smaller dataset.
    
    print("Imported notes, now beginning normalization...")
    # Normalize the corpus data and remove NaN rows.

    mtcorpus = mtsamples_df['description']
    mtsamples_df['corpus'] = mtcorpus
    mtsamples_df.dropna(inplace=True,thresh=3)
    norm_mtcorpus = tn.normalize_corpus(corpus=mtsamples_df['description'], 
                                    html_stripping=True, contraction_expansion=True, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=False, remove_digits=True, 
                                    stopword_removal=True)
    
    ptcorpus = patnotes_df['pn_history']
    patnotes_df['corpus'] = ptcorpus
    patnotes_df.dropna(inplace=True,thresh=3)
    norm_ptcorpus = tn.normalize_corpus(corpus=patnotes_df['pn_history'], 
                                    html_stripping=True, contraction_expansion=True, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=False, remove_digits=True, 
                                    stopword_removal=True)

    mtsamples_df['norm_corpus'] = norm_mtcorpus
    patnotes_df['norm_corpus'] = norm_ptcorpus

    mtsamples_df = mtsamples_df.applymap(lambda s: s.replace('-', ' ') if type(s) == str else s)
    patnotes_df = patnotes_df.applymap(lambda s: s.replace('-', ' ') if type(s) == str else s)
    mtsamples_df = mtsamples_df.applymap(lambda s: s.replace('(', '') if type(s) == str else s)
    patnotes_df = patnotes_df.applymap(lambda s: s.replace(')', '') if type(s) == str else s)
    
    print("Finished normalization, now writing to database...")
    
    for corp in mtsamples_df.itertuples():
        metadata = {'description': corp.description,
                    'samplename': corp.sample_name,
                    'keywords': corp.keywords}
        new_c = Corpus( title=corp.sample_name, 
                        source="MT Samples", new=False, 
                        imported_by="lmadar", safe=True, 
                        import_date= datetime.datetime.now(),
                        corpus = corp.corpus,
                        corpus_norm = corp.norm_corpus, 
                        medspecialty=corp.medical_specialty, 
                        metadata=metadata)
        new_c.save()

    for corp in patnotes_df.itertuples():
        title = 'Patient Number: ' + str(corp.pn_num)
        metadata = {'pn_num': corp.pn_num, 'case_num': corp.case_num}
        new_c = Corpus( title=title, 
                        source="Patient Notes", 
                        new=False, imported_by="lmadar", 
                        safe=True, import_date= datetime.datetime.now(),
                        corpus=corp.corpus, 
                        corpus_norm=corp.norm_corpus,
                        medspecialty='N/A', 
                        metadata=metadata)
        new_c.save()
