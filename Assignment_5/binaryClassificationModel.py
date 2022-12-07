"""
Title: Binary classification model
Author: Gabriel Høst Andersen
Date: 05/12/22
"""

import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

def train_naive_bayes_model(dataset, data_format, sign1, sign2):
    df = pd.read_csv(f'data/{dataset}.{data_format}') # No duplicates found under deduplication, thus omitted.

    # idxs series is used to check whether the horoscope belongs to the given sign(s) as a bool, since its tabular data every horoscope has an associated sign.
    idxs_sign1 = df['sign'] == sign1
    idxs_sign2 = df['sign'] == sign2
    idxs = idxs_sign1 + idxs_sign2

    # uses loc syntax, which takes the argument of our idxs boolean array, in order to extract the data that matches the given signs.
    corpus = df['horoscope'].loc[idxs].values
    y = df['sign'].loc[idxs].values

    # CountVectorizer is used to convert text to numerical data, it returns the input as a document-term matrix (numpy.ndarray here), tokenizes each word, and depicts frequency of every tokenized word for each horoscope. 
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(corpus).toarray()

    # Randomly splits the dataset in to training, which is used to train the model, while the test is used to test the algorithm (on data it hasn't been trained on). Used random_state to set a static seed, normalizing results for easier testing.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, 
        test_size=.20,
        random_state=24
        )

    # Instanties the model, and then trains it through the calling of the .fit method. Model will be trained to predict the y-label for given X-feature based on word count. Calculates the probability for each sign, and outputs the most likely sign.
    classifier = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=True)
    classifier.fit(X_train , y_train)

    # Uses the model which was instantiated and trained early to classify the y-label for each array (horoscope) in the test dataset.  
    y_pred = classifier.predict(X_test)

    # Compares the results garnered from the model's classification, which was saved to y_pred, with the ground truth in y_test. Returns the True negatives, false positives, false negatives, and true positives in an array (since its a binary classification).
    cm = confusion_matrix(y_test, y_pred)

    # Visualizing confusion matrix, changing cmap for readability. 
    vis = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=classifier.classes_)
    vis.plot(cmap='inferno')
    plt.savefig('figures/confusion_matrix.png')
    plt.close()

    # Uses the classifier model to do k-fold cross validation, cv is used to define it as 10 k-folds. 
    cv_accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
    zero_rate_accuracy = 0.50
    performance_difference = (cv_accuracies.mean() - zero_rate_accuracy)
    performance_difference_percentage = (performance_difference / zero_rate_accuracy) * 100

    print('The confusion matrix has been visualized and saved in the figures folder.')
    print(f'Relative Accuracy: {accuracy_score(y_test, y_pred)}')
    print(f'Accuracy in instances (True positives + True negatives): {accuracy_score(y_test, y_pred, normalize=False)}')
    print(f'Cross-validation mean score: {cv_accuracies.mean()}')
    print(f'Cross-validation standard deviation: {cv_accuracies.std()}')
    print(f'Performance difference from zero rate: {"%.3f" % performance_difference}')
    print(f'That correlates to a {"%.1f" % performance_difference_percentage}% relative change')


def main():
    train_naive_bayes_model(dataset='horoscopes', data_format='csv', sign1='aries', sign2="capricorn")

if __name__ == '__main__':
    main()