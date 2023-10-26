import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nltk
from nltk.stem import WordNetLemmatizer
import re
import wn
from wn.morphy import Morphy
import sklearn.metrics
from sklearn.metrics import DistanceMetric
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
# from sklearn.ensemble import RandomForestClassifier
# from sklearn import tree
# from sklearn.ensemble import AdaBoostClassifier
# from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
# import tensorflow as tf
# from tensorflow import keras
import joblib
# import tensorflow_hub as hub
# from transformers import TFBertModel, BertTokenizer
# from tensorflow.keras.utils import to_categorical
# from sklearn.linear_model import LogisticRegression, SGDClassifier



class Model():

    __model = any
    en = wn.Wordnet('oewn:2021', lemmatizer=Morphy())
    stop_words = []
    def __init__(self) -> None:

        self.__model = joblib.load('cb_sgd_final.sav')

        with open("stop.txt","r") as file:
            contents = file.read()
            self.stop_words = contents.split("\n")


    def predict(self,data):

        data = [self.preprocess(doc.text) for doc in data]
        cv = CountVectorizer(max_features=100)
        data = cv.transform(data)
        res = self.__model.predict(data)
        predictions = []

        for pred in res:

            if(pred[0]>pred[1]):

                predictions.append((round(pred[0]*100,2),'NO HATE SPEECH'))

            else:

                predictions.append((round(pred[1]*100,2),'HATE SPEECH'))
                
        return predictions



    def replace(self,pattern,string,v=''):
        pattern = re.compile(pattern)
        return re.sub(pattern,v,string)


    def preprocess(self,text):
        
        #lowering
        text = text.lower()
        
        #removing usernames
        text = self.replace(r'@[\w\-]+',text)
        
        
        giant_url_regex =  re.compile('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
                '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        
        #removing hyperlinks (https://....)
        text = self.replace(giant_url_regex, text)
        
        #removing symbols
        punctuation_signs = list("+=?:!.,`;&()%&^\\/?|~'\"")
        for punct_sign in punctuation_signs:   
            text = text.replace(punct_sign, '')
        
        #removing usernames
        text = self.replace(r'@[\w\-\_]+',text)
        
    #     print(i)
    #     i+=1
        #removing nextlines
        text = self.replace(r'\n',text)
        
        
        #striping extra spaces and word rt(retweet)
        text = self.replace(r'rt',text).rstrip().lstrip()
        text= self.replace(r' +', text,' ')
        
        text= self.replace(r'\d+(\.\d+)?',text,'numbr')
        
        #removing stopwords and lemmatizing
        
        text = text.split()
        res = []
        
        for word in text:
            
            if word not in self.stop_words:
                
                temp = self.en.words(word)
                if len(temp)==0:
                    res.append(word)
                else:
                    res.append(temp[0].lemma())
                    
        return ' '.join(res)