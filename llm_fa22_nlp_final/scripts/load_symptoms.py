import os, django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "llm_fa22_nlp_final.settings")
django.setup()

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

from explore.models import Symptom



def run():
    HTMLFile = open("./data/SymptomsIndex_DiseasesDB.html", "r")
    symptomcode = HTMLFile.read()
    soup = bs(symptomcode, 'lxml')
    
    symptomlist_html = soup.select("li strong a")
    symptomlist_parsed = []
    symptomlist_urls = []
    symptomlist_split = []
    for li in symptomlist_html:
        symptomlist_parsed.append(li.get_text().lower())
        symptomlist_urls.append(li['href'])
        symptomlist_split.append(li.get_text().lower().split(' '))

    symptom_df = pd.DataFrame()
    symptom_df['symptom'] = symptomlist_parsed
    symptom_df['desc_url'] = symptomlist_urls
    symptom_df['wordlist'] = symptomlist_split

    # Normalize the symptoms
    norm_symptoms = tn.normalize_corpus(corpus=symptom_df['symptom'], html_stripping=True, contraction_expansion=True, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=True, remove_digits=True, 
                                    stopword_removal=True)

    symptom_df['norm_symptom'] = norm_symptoms

    # Cleanup ordinal endings from some symptom names
    ordinal_endings = ["st", "nd", "rd", "th"]
    norm_wordlist = []
    norm_name = []
    for symp in symptom_df['norm_symptom']:
        wordlist = symp.split(" ")
        norm_wordlist_item = [w for w in wordlist if not w in ordinal_endings]
        norm_name_item = " ".join(norm_wordlist_item)
        norm_name.append(norm_name_item)
        norm_wordlist.append(str(norm_wordlist_item))

    symptom_df["norm_name"]= norm_name
    symptom_df["norm_wordlist"] = norm_wordlist
    symptom_df.dropna(inplace=True)
    symptom_df.drop_duplicates(subset=["norm_name"],keep='first', inplace=True)


    # Loop through the rows and create DB instances for each symptom entry.
    for sym in symptom_df.itertuples():
        new_s = Symptom(
            name = sym.symptom, 
            name_norm = sym.norm_name,
            description= sym.symptom, 
            url=sym.desc_url, 
            wordlist=sym.norm_wordlist)
        new_s.save()


    #symptom_vocab = [] 
    #for wordl in symptom_df["norm_wordlist"]:
    #    symptom_vocab.extend(wordl)
        
    #symptom_vocab = list(dict.fromkeys(symptom_vocab)) #get rid of duplicates
