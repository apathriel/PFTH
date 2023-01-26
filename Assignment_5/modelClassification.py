"""
Title: Binary classification model
Author: Gabriel Høst Andersen
Date: 05/12/22
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

def get_stopwords():
    return ["","a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder", "zone", "10", "100", "12", "yourself", "zodiac", "13th", "16th", "18th"]

def get_signs(dataset, data_format):
    df = pd.read_csv(f'data/{dataset}.{data_format}')
    return list(set(df['sign'].values))

def shorten_strings_in_list(list_to_shorten, character=3):
    if type(list_to_shorten) is list:
        list_to_shorten.sort() # sorting to match actual labels
        new_list = []
        for item in list_to_shorten:
            new_list.append(item[0:character])
        return new_list
    else:
        print('Argument was not of appropriate data type (list)')
        return None # for clarification

# Create a function to edit csv file (only needs to be done once, not a non-destructive change, because of the to_csv method call)
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

def train_naive_bayes_model(dataset, data_format, signs, stop_word_list=None, df_max=1.0, df_min=1, visualize_cm=False, cm_name='figure', cm_labels='', baseline=0.5):
    df = pd.read_csv(f'data/{dataset}.{data_format}') # No duplicates found under deduplication, thus omitted.

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

    # idxs series is used to check whether the horoscope belongs to the given sign(s) as a bool, since its tabular data every horoscope has an associated sign.

    # uses loc syntax, which takes the argument of our idxs boolean array, in order to extract the data that matches the given signs.
    corpus = df['horoscope'].loc[idxs_total].values
    y = df['sign'].loc[idxs_total].values

    # CountVectorizer is used to convert text to numerical data, it returns the input as a document-term matrix (numpy.ndarray here), tokenizes each word, and depicts frequency of every tokenized word for each horoscope. 
    vectorizer = CountVectorizer(stop_words=stop_word_list, max_df=df_max, min_df=df_min)
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

    if not cm_labels:
        cm_labels = classifier.classes_

    # Visualizing confusion matrix, changing cmap for readability. 
    if visualize_cm:
        vis = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=cm_labels)
        vis.plot(cmap='inferno')
        plt.savefig(f'figures/{cm_name}.png')
        plt.close()
        print(f'The confusion matrix has been visualized and saved in the figures folder as {cm_name}.png.')

    # Uses the classifier model to do k-fold cross validation, cv is used to define it as 10 k-folds. 
    cv_accuracies = cross_val_score(estimator = classifier, X = X_train, y = y_train, cv = 10)
    zero_rate_accuracy = baseline
    performance_difference = (cv_accuracies.mean() - zero_rate_accuracy)
    performance_difference_percentage = (performance_difference / zero_rate_accuracy) * 100

    print(f'Relative Accuracy: {accuracy_score(y_test, y_pred)}')
    print(f'Accuracy in instances (True positives + True negatives): {accuracy_score(y_test, y_pred, normalize=False)}')
    print(f'Cross-validation mean score: {cv_accuracies.mean()}')
    print(f'Cross-validation standard deviation: {cv_accuracies.std()}')
    print(f'Performance difference from zero rate: {"%.3f" % performance_difference}')
    print(f'That correlates to a {"%.1f" % performance_difference_percentage}% relative change')


def main():
    print('Results from model without preprocessing:')
    train_naive_bayes_model(dataset='horoscopes', data_format='csv', signs=['aries', 'capricorn'], visualize_cm=True, cm_name='confusion_matrix', baseline=0.5)
    print('\nResults from model with preprocessed dataset:')
    train_naive_bayes_model(dataset='horoscopes', data_format='csv', signs=['aries', 'capricorn'], df_max=0.7, baseline=0.5)
    print('\nResults from multi classification model:')
    train_naive_bayes_model(dataset='horoscopes', data_format='csv', signs=get_signs(dataset='horoscopes', data_format='csv'), visualize_cm=True, cm_name='confusion_matrix_multi', cm_labels = shorten_strings_in_list(get_signs(dataset='horoscopes', data_format='csv'), character=3), baseline=0.084)
    print('\nResults from zodiac element classification model')
    zodiac_classification_csv_replace(dataset='edited_horoscopes', data_format='csv')
    train_naive_bayes_model(dataset='edited_horoscopes', data_format='csv', signs=get_signs(dataset='edited_horoscopes', data_format='csv'), visualize_cm=True, cm_name='confusion_matrix_element', baseline=0.25) 

if __name__ == '__main__':
    main()