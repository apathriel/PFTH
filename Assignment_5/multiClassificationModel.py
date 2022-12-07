"""
Title: Multi classification model
Author: Gabriel Høst Andersen
Date: 06/12/22
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB 
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

df = pd.read_csv('data/horoscopes.csv')

def get_signs():
    return list(set(df['sign'].values))

def shorten_strings_in_list(list_to_shorten, character=3):
    if type(list_to_shorten) is list:
        new_list = []
        for item in list_to_shorten:
            new_list.append(item[0:character])
        return new_list
    else:
        print('Argument was not of appropriate data type (list)')
        return None # for clarification

def train_naive_bayes_model(signs):
    try:
        signs.sort()
    except AttributeError:
        print("Please input a list object for the 'signs' argument")
    except: 
        print('Undiagnosed error')
    else:
        idxs_total = np.empty(shape=len(df['sign'] == signs[0]), dtype='bool')
        for sign in signs:
            idxs = df['sign'] == sign
            idxs_total += idxs.values
 
    corpus = df['horoscope'].loc[idxs_total].values
    y = df['sign'].loc[idxs_total].values

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=.20,
        random_state=24
    )    

    classifier = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    classifier.fit(X_train , y_train)

    y_pred = classifier.predict(X_test)

    cm = confusion_matrix(y_test, y_pred)
    cm_labels = shorten_strings_in_list(signs, character=3) 

    vis = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=cm_labels)
    vis.plot(cmap='inferno')
    plt.savefig('figures/confusion_matrix_multi.png')
    plt.close()

    cv_accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
    
    zero_rate_accuracy = 0.084
    relative_accuracy = accuracy_score(y_test, y_pred)
    performance_difference = (cv_accuracies.mean() - zero_rate_accuracy)
    performance_difference_percentage = (performance_difference / zero_rate_accuracy) * 100

    print('The confusion matrix has been visualized and saved as confusion_matrix_multi in the figures folder.')
    print(f'Zero Rate accuracy: {zero_rate_accuracy}')
    print(f'Relative Accuracy: {"%.3f" % relative_accuracy}')
    print(f'Accuracy in instances (True positives + True negatives): {accuracy_score(y_test, y_pred, normalize=False)}')
    print(f'Cross-validation mean score: {cv_accuracies.mean()}')
    print(f'Cross-validation standard deviation: {cv_accuracies.std()}') 
    print(f'Performance difference from zero rate: {"%.3f" % performance_difference}')
    print(f'That correlates to a {"%.1f" % performance_difference_percentage}% relative change')

def main():
    train_naive_bayes_model(signs=get_signs())

if __name__ == '__main__':
    main()