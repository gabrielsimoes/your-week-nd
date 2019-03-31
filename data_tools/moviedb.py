#!/usr/bin/env python3
import sys
from nltk.stem import SnowballStemmer
import pandas as pd

genres = ["action", "adventure", "comedy", "superhero", "drama", "horror", "musical", "sci-fi", "westerns", "romance", "classic", "animated"]

def compare(genre): 
    for g in genres:
        if g in genre:
            return 'True'
    return 'False'

def clean(genre):
    for g in genres:
        if g in genre:
            return g
raw = pd.read_csv(sys.argv[1])
raw['Genre'] = raw['Genre'].astype(str)
raw['cut'] = raw['Genre'].apply(compare)
raw = raw[raw.cut == "True"]
raw['Genre'] = raw['Genre'].apply(clean)

raw = raw[['Genre', 'Plot']]

out = pd.DataFrame.from_dict(raw)
out.to_csv(sys.argv[2], index = False)
