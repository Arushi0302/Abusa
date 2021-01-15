# -*- coding: utf-8 -*-
"""model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZKTs5I8B6176_AB2Z0kOYx4xntfAydq6
"""

from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.layers import Bidirectional, GlobalMaxPool1D
from keras.models import Model
from keras import initializers, regularizers, constraints, optimizers, layers
import codecs
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re
import sys
import warnings
import pickle
from bs4 import BeautifulSoup
warnings.filterwarnings("ignore")
nltk.download('stopwords')

model = load_model('/app/Model/toxic.h5')

def decontracted(phrase):
    # specific
    phrase = re.sub(r"won't", "will not", phrase)
    phrase = re.sub(r"can\'t", "can not", phrase)
    # general
    phrase = re.sub(r"n\'t", " not", phrase)
    phrase = re.sub(r"\'re", " are", phrase)
    phrase = re.sub(r"\'s", " is", phrase)
    phrase = re.sub(r"\'d", " would", phrase)
    phrase = re.sub(r"\'ll", " will", phrase)
    phrase = re.sub(r"\'t", " not", phrase)
    phrase = re.sub(r"\'ve", " have", phrase)
    phrase = re.sub(r"\'m", " am", phrase)
    return phrase

def cleanPunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned

def clear_sentance(sentance):
    sentance= re.sub(r"http\S+", "", sentance)
    sentance = decontracted(sentance)
    sentance = cleanPunc(sentance)
    sentance = re.sub("\S*\d\S*", "", sentance).strip()
    sentance = re.sub('[^A-Za-z]+', ' ', sentance)
    stop_words = set(stopwords.words('english'))
    stop_words.update(['zero','one','two','three','four','five','six','seven','eight','nine','ten','may','also','across','among','beside','however','yet','within'])
    sentance = ' '.join(e.lower() for e in sentance.split() if e.lower() not in  stopwords.words('english'))
    return sentance.strip()

def tokenize(sentance):
    MAX_SEQUENCE_LENGTH = 400
    with open('/app/Model/tokenizer.pickle', 'rb') as handle:
                    tokenizer = pickle.load(handle)
    test_sequences = tokenizer.texts_to_sequences([sentance])
    test_data = pad_sequences(test_sequences, maxlen=MAX_SEQUENCE_LENGTH)
    return test_data

def model_predict(test_data):    
    prediction=model.predict(test_data)
    return prediction

def get_prediction(sentance):
    clear_text=clear_sentance(sentance)
    test_data=tokenize(clear_text)
    predicted_array=model_predict(test_data)
    predicted_values={'Hate':round(predicted_array[0][0]),'Insult':round(predicted_array[0][1]), 'Obscene':round(predicted_array[0][2]), 'Severe Toxic':round(predicted_array[0][3]), 'Threat':round(predicted_array[0][4]), 'Toxic':round(predicted_array[0][5])}
    result=0
    for key in predicted_values:
        if(predicted_values[key]==1.0):
            result+=1
    if result == 0:
      return 0
    else:
      return 1

def run_model(mydictList):
    #manupulations here.
    for di in mydictList:
      r = ' '.join(di["data"])
      di["p"] = get_prediction(r)
    manupulated_data = mydictList
    return manupulated_data

def getData(data):
    return run_model(data)