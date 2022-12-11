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

from explore.models import Medication
def run():

    # Load the medication data.
    drug_df = pd.read_csv('./data/product.txt', sep='\t', encoding='latin1')

    # package_df =  pd.read_csv('./data/package.txt', sep='\t', encoding='latin1')

    # Drop attributes that we won't be using.
    drug_df.drop(['PROPRIETARYNAMESUFFIX', 'STARTMARKETINGDATE', 'ENDMARKETINGDATE', 'DEASCHEDULE', 'NDC_EXCLUDE_FLAG', 'LISTING_RECORD_CERTIFIED_THROUGH'], axis=1, inplace=True)
    print(drug_df.columns)

    
    # Dedupe and normalize. We will be discarding some different products within the same drug name, but that's ok because we're not getting into specifying which particular dosage is being reported.
    drug_df.drop_duplicates(subset=["NONPROPRIETARYNAME","SUBSTANCENAME","LABELERNAME"],keep='first', inplace=True)
    drug_df.dropna(inplace=True,thresh=6)
 

    generic_norm = tn.normalize_corpus(corpus=drug_df['NONPROPRIETARYNAME'], html_stripping=True,contraction_expansion=False, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=False, remove_digits=False, 
                                    stopword_removal=False)
    drug_df['generic_norm'] = generic_norm;

    brand_norm = tn.normalize_corpus(corpus=drug_df['PROPRIETARYNAME'], html_stripping=True,contraction_expansion=False, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=False, remove_digits=False, 
                                    stopword_removal=False)
    drug_df['brand_norm'] = brand_norm;

    labeler_norm = tn.normalize_corpus(corpus=drug_df['LABELERNAME'], html_stripping=True,contraction_expansion=False, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=False, remove_digits=False, 
                                    stopword_removal=False)
    drug_df['labeler_norm'] = labeler_norm;

    compound_norm = tn.normalize_corpus(corpus=drug_df['SUBSTANCENAME'], html_stripping=True,contraction_expansion=False, 
                                    accented_char_removal=True, text_lower_case=True, text_lemmatization=False, 
                                    text_stemming=False, special_char_removal=False, remove_digits=False, 
                                    stopword_removal=False)
    drug_df['compound_norm'] = compound_norm;


    drug_df = drug_df.applymap(lambda s: s.lower() if type(s) == str else s)

    # Remove commas and periods unless between numbers.
    drug_df = drug_df.applymap(lambda s: re.sub('(?<=\D)[.,]|[.,](?=\D)', ' ', s) if type(s) == str else s)
    drug_df = drug_df.applymap(lambda s: s.replace('(', ' ') if type(s) == str else s)
    drug_df = drug_df.applymap(lambda s: s.replace(')', ' ') if type(s) == str else s)
    drug_df = drug_df.applymap(lambda s: s.replace(';', ' ') if type(s) == str else s)
    drug_df = drug_df.applymap(lambda s: s.replace('-', ' ') if type(s) == str else s)
    drug_df.columns = map(str.lower, drug_df.columns)
    drug_df.dropna(inplace=True,thresh=6)

    drug_df.drop(drug_df[drug_df.substancename == 'nan'].index, inplace=True)
    drug_df.drop(drug_df[drug_df.compound_norm == 'nan'].index, inplace=True)
    

    for drug in drug_df.itertuples():
        new_d = Medication(brand_name=drug.proprietaryname,compound_norm=drug.compound_norm, brand_norm=drug.brand_norm, compound_name=drug.substancename, generic_norm=drug.generic_norm,labeler_norm=drug.labeler_norm,
            generic_name=drug.nonproprietaryname, type=drug.producttypename, source="Open FDA DB", 
            labeler=drug.labelername, ndc_id=drug.productndc, pharm_class=drug.pharm_classes, description=drug.dosageformname )
        new_d.save()
