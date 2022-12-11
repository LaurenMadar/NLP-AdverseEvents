


# Initialize matcher patterns, including the items in the med vocabulary and the symptom vocabulary.
med_sym_matcher = Matcher(nlp.vocab)

for med in med_vocab:
    pattern = [[{"TEXT": med}]]
    med_sym_matcher.add("MED_" + med, pattern)

for sym in symptom_vocab:
    pattern = [[{"TEXT": sym}]]
    med_sym_matcher.add("SYM_" + sym, pattern)

# try out the matchers...
doc = nlp("I am not sick but I may have taken valium once or twice when I had a headache and insomnia")

matches = med_sym_matcher(doc)


def get_matched_terms(doc, matches):
    matched_terms = []
    for ma in matches:
        match_id, start, end = ma
        # Get the matched span
        matched_span = doc[start:end]
        matched_terms.append(matched_span.text)
    return matched_terms

get_matched_terms(doc, matches)


results = []
result_terms = []
# How many? Replace with all or pass in parameters.
entries = patnotes_df['norm_corpus'].head(3000)

for patient_note in entries:
    pn_doc = nlp(patient_note)
    pn_matches = med_sym_matcher(pn_doc)
    pn_terms = get_matched_terms(pn_doc, pn_matches)
    results.append(len(pn_matches)>0)
    result_terms.append(pn_terms)
    if len(results)%100 == 0:
        print('Finished item ',len(results))