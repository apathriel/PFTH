"""
    Title: Word importance (With or without function words)
    Authors: Albin Sand, Gabriel Høst Andersen, Lissa Bui, Victor Rasmussen.
    Date: 03/10/22
"""

import operator
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm

df = pd.read_csv('data/horoscopes.csv')

horoscopeClean = df['horoscope-clean']

def stopwords():
    # list of stopwords for filtering out of strings.
    return ["","a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder"]

def tokenizer(text, lower=True, stopword=True):
    # string tokenization (splitting string into individual words), with optional case lowering and optional stopword filtering.
    if stopword:
        stopwordlist = stopwords()
        tokens = [token for token in text.lower().split(' ') if token not in stopwordlist]

    elif lower:
        tokens = text.lower().split()
    
    else:
        tokens = text.split()
    
    return tokens

def word_count(text, sort = True, stopword=False):
    #count words, with optional sorting and stopwords
    counter = {}
    for word in tokenizer(text, stopword=stopword):
        counter.setdefault(word, 0)
        counter[word] = counter[word] + 1
    
    if sort:
        counter = dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))

    return counter

def topWords(useStopword = True):
    horoscopeClean = df['horoscope-clean']
    topWordList = []
    wc = word_count(' '.join(horoscopeClean), sort = True, stopword = useStopword)
    for i in range(0, 100):
        topWord = list(wc.keys())[i]
        topWordList.append(topWord)
    return topWordList

def topWordsSign(sign):
    specificZodiac = df['sign'] == sign
    horoscopeSpecific = df['horoscope-clean'].loc[specificZodiac].values
    topWordList = []
    wc = word_count(' '.join(horoscopeSpecific))
    for i in range(0, 200):
        topWord = list(wc.keys())[i]
        topWordList.append(topWord)
    return topWordList

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def difference(lst1, lst2):
    return list(set(lst1).difference(set(lst2)))

def differenceZodiac(sign1, sign2, sign3):
    print('Words that occur in ' + sign1 + ' but not in ' + sign2 + ':')
    print(difference(topWordsSign(sign1), topWordsSign(sign2)))
    print('\nWords that occur in ' + sign2 + ' but not in ' + sign1 + ':')
    print(difference(topWordsSign(sign2), topWordsSign(sign1)))
    print('\nWords that occur in ' + sign2 + ' but not in ' + sign3 + ':')
    print(difference(topWordsSign(sign2), topWordsSign(sign3)))
    print('\nWords that occur in ' + sign1 + ' but not in ' + sign3 + ':')
    print(difference(topWordsSign(sign1), topWordsSign(sign3)))
    print('\nWords that occur in ' + sign3 + ' but not in ' + sign1 + ':')
    print(difference(topWordsSign(sign3), topWordsSign(sign1)))
    print('\nWords that occur in ' + sign3 + ' but not in ' + sign2 + ':')
    print(difference(topWordsSign(sign3), topWordsSign(sign2)))

def main():
    print('Problem 1 - With or without function words')
    print('The intersection between the lists consists of:')
    print(intersection(topWords(), topWords(False)))
    print('\nThe differences that occur in list with stopwords, and not in list without stopwords:')
    print(difference(topWords(), topWords(False)))
    print('\nThe differences that occur in list without stopwords, and not in list with stopwords')
    print(difference(topWords(False), topWords()))
    print('\nProblem 2 - Sign-specific indexing')
    differenceZodiac('cancer', 'aries', 'capricorn')

if __name__=="__main__":
    main()