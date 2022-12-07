"""
Title: Zodiac element classification model
Author: Gabriel Høst Andersen
Date: 07/12/22
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score

# Create a function to edit csv file (only needs to be done once, not a non-destructive change)
def zodiac_classification_csv_replace(dataset, data_format):
    df = pd.read_csv(f'data/{dataset}.{data_format}')

    df['sign'] = df['sign'].replace({'aries': 'fire'})
    df['sign'] = df['sign'].replace({'sagittarius': 'fire'})
    df['sign'] = df['sign'].replace({'leo': 'fire'})
    df['sign'] = df['sign'].replace({'cancer': 'water'})
    df['sign'] = df['sign'].replace({'scorpio': 'water'})
    df['sign'] = df['sign'].replace({'pisces': 'water'})
    df['sign'] = df['sign'].replace({'gemini': 'air'})
    df['sign'] = df['sign'].replace({'libra': 'air'})
    df['sign'] = df['sign'].replace({'aquarius': 'air'})
    df['sign'] = df['sign'].replace({'taurus': 'earth'})
    df['sign'] = df['sign'].replace({'virgo': 'earth'})
    df['sign'] = df['sign'].replace({'capricorn': 'earth'})

    df.to_csv(f'data/{dataset}.{data_format}', index=False)

def train_naive_bayes_model(dataset, data_format):
    df = pd.read_csv(f'data/{dataset}.{data_format}') 

    idxs_fire_signs = df['sign'] == 'fire'
    idxs_air_signs = df['sign'] == 'air'
    idxs_water_signs = df['sign'] == 'water'
    idxs_earth_signs = df['sign'] == 'earth'

    idxs_total = idxs_fire_signs + idxs_air_signs + idxs_water_signs + idxs_earth_signs
    # uses loc syntax, which takes the argument of our idxs boolean array, in order to extract the data that matches the given signs.
    corpus = df['horoscope'].loc[idxs_total].values
    y = df['sign'].loc[idxs_total].values

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
    vis = ConfusionMatrixDisplay(confusion_matrix=cm)
    vis.plot(cmap='inferno')
    plt.savefig('figures/confusion_matrix_element.png')
    plt.close()

    cv_accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)

    zero_rate_accuracy = 0.25
    relative_accuracy = accuracy_score(y_test, y_pred)
    performance_difference = (cv_accuracies.mean() - zero_rate_accuracy)
    performance_difference_percentage = (performance_difference / zero_rate_accuracy) * 100

    print('The confusion matrix has been visualized and saved in the figures folder.')
    print(f'Relative Accuracy: {relative_accuracy}')
    print(f'Accuracy in instances (True positives + True negatives): {accuracy_score(y_test, y_pred, normalize=False)}')
    print(f'Cross-validation mean score: {cv_accuracies.mean()}')
    print(f'Cross-validation standard deviation: {cv_accuracies.std()}')
    print(f'Performance difference from zero rate: {"%.3f" % performance_difference}')
    print(f'That correlates to a {"%.1f" % performance_difference_percentage}% relative change')


def main():
    zodiac_classification_csv_replace(dataset='edited_horoscopes', data_format='csv')
    train_naive_bayes_model(dataset='edited_horoscopes', data_format='csv')

if __name__ == '__main__':
    main()