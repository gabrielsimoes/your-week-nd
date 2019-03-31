#!/usr/bin/env python3
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import sys
import pickle
import importantWords as pre
import pandas as pd
from gensim.models import Doc2Vec
import numpy as np
from gensim.models.doc2vec import TaggedDocument

def label_sentences(corpus, label_type):
    """ 
    Gensim's Doc2Vec implementation requires each document/paragraph to have a label associated with it.
    We do this by using the TaggedDocument method. The format will be "TRAIN_i" or "TEST_i" where "i" is
    a dummy index of the post.
    """
    labeled = []
    for i, v in enumerate(corpus):
        label = label_type + '_' + str(i)
        labeled.append(TaggedDocument(v.split(), [label]))
    return labeled

week_movies = "yourweek.json"

df = pre.clean(week_movies)
x = df.cleaned
x_wow = label_sentences(x, 'Train')
model = Doc2Vec(x_wow, dm=0, vector_size=300, negative=5, min_count=1, alpha=0.065, min_alpha=0.065)

def get_vectors(model, corpus_size, vectors_size, vectors_type):
    """ 
    Get vectors from trained doc2vec model
    :param doc2vec_model: Trained Doc2Vec model
    :param corpus_size: Size of the data
    :param vectors_size: Size of the embedding vectors:wq
    :param vectors_type: Training or Testing vectors
    :return: list of vectors
    """
    vectors = np.zeros((corpus_size, vectors_size))
    for i in range(0, corpus_size):
        prefix = vectors_type + '_' + str(i)
        vectors[i] = model.docvecs[prefix]
    return vectors

train_vectors_dbow = get_vectors(model, len(x_wow), 300, 'Train')

with open('trained_movies', 'rb') as training_model:
    model = pickle.load(training_model)

y_pred = model.predict(train_vectors_dbow)
y_pred2 = model.predict_proba(train_vectors_dbow)
df["pred"] = pd.DataFrame(y_pred)
prob = [max(x) for x in y_pred2]
df["prob"] = pd.DataFrame(prob)
df.sort_values(by=["prob"])
df.drop(colums=['cleaned','prob'])
df.to_json(r'your_week_ordered.json')

