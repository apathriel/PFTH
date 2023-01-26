"""
Title: Examining relationships of datasets through linear regression
Author: Gabriel Høst Andersen
Date: 14/12/22 
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression 
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from matplotlib import pyplot as plt
from csv_func import pruning_csv, drop_row_by_empty_cell, create_underscore_string, get_corpus_from_column, get_corpus_from_genre_index
from word_importance import get_top_words_for_genre, get_frequency_top_words

def get_converted_array(arr1, arr2):
    converted_array = np.vstack((arr1, arr2)).transpose()
    return converted_array

def create_linear_regression_model(x_to_train, y_to_train, independant_label='', dependant_label='', standardize=True):
    if standardize:
        X = get_converted_array(x_to_train, y_to_train)
        scaler = StandardScaler()
        scaler.fit(X)
        X_sd = scaler.transform(X)
        x = X_sd[:,0].reshape(-1, 1)
        y = X_sd[:,1].reshape(-1, 1)
    else:
        x = x_to_train.reshape(-1, 1)
        y = y_to_train.reshape(-1, 1)
    
    X_train, X_test, y_train, y_test = train_test_split(
    x, y,
    test_size=0.20,
    random_state=18
    )

    lin_reg = LinearRegression()
    lin_reg.fit(X_train, y_train)
    y_pred = lin_reg.predict(X_test)
    cv_accuracies = cross_val_score(estimator = lin_reg, X = X_train, y = y_train, cv = 10)

    plt.scatter(X_test, y_test, s=3, color='#88c999')
    plt.plot(X_test, y_pred)
    plt.title(f'{dependant_label} vs. {independant_label}', pad=15, fontsize=14)
    plt.xlabel(independant_label)
    plt.ylabel(dependant_label)
    plt.legend(['Test data', 'Regression'])
    plt.savefig(f'figures/lin_reg/{create_underscore_string(dependant_label)}_vs_{create_underscore_string(independant_label)}.png')
    plt.close()

    print(f'\n---Printing results for {dependant_label} vs. {independant_label}---')
    print(f'[RESULTS] Coefficients: {lin_reg.coef_}')
    print(f'[RESULTS] Mean squared error: {mean_squared_error(y_test, y_pred)}')
    print(f'[RESULTS] Coefficient of determination (r2): {r2_score(y_test, y_pred)}')
    print(f'[RESULTS] 10 K-fold cross validation mean: {cv_accuracies.mean()}')
    print(f'[RESULTS] 10 K-fold cross validation standard deviation: {cv_accuracies.std()}')

def main():
    genre_to_model = 'fantasy'
    df_amazon = pd.read_csv('data/amazon_data_science_books.csv')
    df_amazon = drop_row_by_empty_cell(df=df_amazon, columns=['pages', 'price'])

    df_rating = pd.read_csv('data/GoodReads_100k_books.csv')
    df_rating = drop_row_by_empty_cell(df=df_rating, columns=['totalratings', 'reviews'])

    df_linreg = pruning_csv('GoodReads_100k_books', 'csv', columns_to_tokenize=[{'column':'genre', 'split':','}, {'column':'desc', 'split':' '}], remove_punctuation=False)
    df_word_importance = pruning_csv('GoodReads_100k_books', 'csv', columns_to_tokenize=[{'column':'genre', 'split':','}])
    
    genre_top = get_top_words_for_genre(df=df_word_importance, genre_top=genre_to_model, num_words=50)
    top_word_occurances_in_desc = get_frequency_top_words(get_corpus_from_genre_index(df_linreg, genre_to_model, 'desc'), genre_top=genre_top)

    create_linear_regression_model(top_word_occurances_in_desc, get_corpus_from_genre_index(df_linreg, genre_to_model, 'rating'), independant_label='Top word occurances', dependant_label='Rating')
    create_linear_regression_model(get_corpus_from_column(df_rating,'reviews'), get_corpus_from_column(df_rating, 'totalratings'), independant_label='Reviews', dependant_label='Total Ratings')
    create_linear_regression_model(get_corpus_from_column(df_amazon,'pages'), get_corpus_from_column(df_amazon, 'price'), independant_label='Pages', dependant_label='Price')

if __name__ == '__main__':
    main()