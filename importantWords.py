#!/usr/bin/env python3
import sys
import pandas as pd
import string
from nltk.corpus import stopwords
import re

stop_words = set(stopwords.words('english'))
def internal(text): 
    text = str(text)
    text = text.lower()
    text = ' '.join(word for word in text.split() if word not in stop_words if word not in string.punctuation)
    text = re.compile('[/(){}\[\]\|@,;]^0-9a-z #+_.').sub(' ', text)
    return text

def clean(source):
    raw = pd.read_json(source)
    raw.cleaned = raw.desc.apply(lambda x: internal(x))

    return pd.DataFrame.from_dict(raw)
