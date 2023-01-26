"""
Title: Naive bayes binary- and multiclass classification
Author: Gabriel Høst Andersen
Date: 14/12/22
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from csv_func import pruning_csv, get_only_first_element_from_list, drop_row_by_value_count, get_column_values

def train_classification_model(df, genres, title='', file_name='', visualize=True, pred_user_desc=False, do_cv=True, test_df=None):
    # created workaround for having to define idxs_total, since the script would repeatedly fail when attempting to define the shape of idxs_total
    for genre in genres:
        if genre == genres[0]:
            idxs = df['genre'] == genre
            idxs_total = idxs
        else:
            idxs = df['genre'] == genre
            idxs_total += idxs.values

    x = df['desc'].loc[idxs_total].values
    y = df['genre'].loc[idxs_total].values

    X_train, X_test, y_train, y_test = train_test_split(
        x, y, 
        test_size=.20,
        random_state=24,
    )
    # instantiate vectorizer, only vectorize X_train to avoid incorporating X_test during training, preventing data leakage, and for applying new test set
    vectorizer = CountVectorizer()
    X_train_cv = vectorizer.fit_transform(X_train)

    classifier = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    classifier.fit(X_train_cv, y_train)

    if pred_user_desc:
        ny_test_blabla = vectorizer.transform(test_df['desc'])
        y_new_pred = classifier.predict(ny_test_blabla)
        print(f'\n[RESULTS] The predicted genre for your description is {y_new_pred}')
    else:
        X_test_cv = vectorizer.transform(X_test)
        y_pred = classifier.predict(X_test_cv)
        print(f'\n---Printing results for {title}---')
        print(f'[RESULTS] Relative Accuracy: {accuracy_score(y_test, y_pred)}')
        if do_cv:
            cv_accuracies = cross_val_score(estimator = classifier, X = X_train_cv, y = y_train, cv = 10)
            print(f'[RESULTS] Cross-validation mean score: {cv_accuracies.mean()}')
            print(f'[RESULTS] Cross-validation standard deviation: {cv_accuracies.std()}') 

    if visualize:
        cm = confusion_matrix(y_test, y_pred)
        vis = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classifier.classes_)
        vis.plot(cmap='magma')
        plt.savefig(f'figures/confusion_matrix/{file_name}.png')
        plt.close()
        print(f'[INFO] The confusion matrix has been visualized and saved in the figures folder as {file_name}.png.')

def user_desc_prompt():
    confirmation = input('\nWould you like to write a description for the model to classify? [y/n]\n')

    if str(confirmation).lower() == 'y':
        return user_write_desc()
    elif str(confirmation).lower() == 'n':
        print("That's too bad. Have a nice day!")
        return None
    else: 
        print("Incorrect format. Please either input 'y' or 'n'.")
        return user_desc_prompt()

def user_write_desc():
    desc = input('Please write your description below:\n')
    print('\nThank you! Please hold while the model attempts to classify which genre your description would belong to.')
    return pd.DataFrame({'desc':[str(desc).lower()],'genre': np.nan})

def main():
    df_binary = pruning_csv('GoodReads_100k_books', 'csv', columns_to_tokenize=[{'column':'genre', 'split':','}])
    df_binary['genre'] = get_only_first_element_from_list(df_binary, 'genre')
    df_multi = pruning_csv('GoodReads_100k_books', 'csv', columns_to_tokenize=[{'column':'genre', 'split':','}])
    df_multi['genre'] = get_only_first_element_from_list(df_multi, 'genre')
    df_multi = drop_row_by_value_count(df_multi, 'genre', 500)
    df_prediction_example = pd.read_csv('data/prediction_example.csv')

    train_classification_model(df=df_binary, genres=['fantasy', 'science fiction'], file_name='binary_fantasy_science_fiction',title='binary classification between fantasy and science fiction genres')
    train_classification_model(df=df_binary, genres=['fantasy', 'nonfiction'], file_name='binary_fantasy_nonfiction', title='binary classification between fantasy and nonfiction genres')
    train_classification_model(df=df_multi, genres=get_column_values(df_multi, 'genre'), visualize=False, title='multiclass classification of 36 top occuring genres')
    print("\nPrediction of Brandon Sanderson's 'The Final Empire' based on its description:")
    train_classification_model(df=df_multi, genres=get_column_values(df_multi, 'genre'), visualize=False, pred_user_desc=True, test_df=df_prediction_example)

    df_user_prediction = user_desc_prompt()

    if df_user_prediction is not None:
        train_classification_model(df=df_multi, genres=get_column_values(df_multi, 'genre'), visualize=False, pred_user_desc=True, test_df=df_user_prediction)

if __name__ == '__main__':
    main()