"""
Title: Word importance for book genres
Author: Gabriel Høst Andersen
Date: 14/12/22
"""

import numpy as np
import matplotlib.pyplot as plt
import operator
from matplotlib_venn import venn2
from csv_func import pruning_csv, create_underscore_string, get_corpus_from_genre_index

# stopwords(), tokenizer(), word_count(), and intersection() were provided by KLN during the semester. I've made slight altercations to the stopwords, and removed the lowercase option from the tokenizer
def stopwords():
    return ["","a","about","above","after","again","against","ain","all","am","an","and","any","are","aren","aren't","as","at","be","because","been","before","being","below","between","both","but","by","can","couldn","couldn't","d","did","didn","didn't","do","does","doesn","doesn't","doing","don","don't","down","during","each","few","for","from","further","had","hadn","hadn't","has","hasn","hasn't","have","haven","haven't","having","he","her","here","hers","herself","him","himself","his","how","i","if","in","into","is","isn","isn't","it","it's","its","itself","just","ll","m","ma","me","mightn","mightn't","more","most","mustn","mustn't","my","myself","needn","needn't","no","nor","not","now","o","of","off","on","once","only","or","other","our","ours","ourselves","out","over","own","re","s","same","shan","shan't","she","she's","should","should've","shouldn","shouldn't","so","some","such","t","than","that","that'll","the","their","theirs","them","themselves","then","there","these","they","this","those","through","to","too","under","until","up","ve","very","was","wasn","wasn't","we","were","weren","weren't","what","when","where","which","while","who","whom","why","will","with","won","won't","wouldn","wouldn't","y","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves","could","he'd","he'll","he's","here's","how's","i'd","i'll","i'm","i've","let's","ought","she'd","she'll","that's","there's","they'd","they'll","they're","they've","we'd","we'll","we're","we've","what's","when's","where's","who's","why's","would","able","abst","accordance","according","accordingly","across","act","actually","added","adj","affected","affecting","affects","afterwards","ah","almost","alone","along","already","also","although","always","among","amongst","announce","another","anybody","anyhow","anymore","anyone","anything","anyway","anyways","anywhere","apparently","approximately","arent","arise","around","aside","ask","asking","auth","available","away","awfully","b","back","became","become","becomes","becoming","beforehand","begin","beginning","beginnings","begins","behind","believe","beside","besides","beyond","biol","brief","briefly","c","ca","came","cannot","can't","cause","causes","certain","certainly","co","com","come","comes","contain","containing","contains","couldnt","date","different","done","downwards","due","e","ed","edu","effect","eg","eight","eighty","either","else","elsewhere","end","ending","enough","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","except","f","far","ff","fifth","first","five","fix","followed","following","follows","former","formerly","forth","found","four","furthermore","g","gave","get","gets","getting","give","given","gives","giving","go","goes","gone","got","gotten","h","happens","hardly","hed","hence","hereafter","hereby","herein","heres","hereupon","hes","hi","hid","hither","home","howbeit","however","hundred","id","ie","im","immediate","immediately","importance","important","inc","indeed","index","information","instead","invention","inward","itd","it'll","j","k","keep","keeps","kept","kg","km","know","known","knows","l","largely","last","lately","later","latter","latterly","least","less","lest","let","lets","like","liked","likely","line","little","'ll","look","looking","looks","ltd","made","mainly","make","makes","many","may","maybe","mean","means","meantime","meanwhile","merely","mg","might","million","miss","ml","moreover","mostly","mr","mrs","much","mug","must","n","na","name","namely","nay","nd","near","nearly","necessarily","necessary","need","needs","neither","never","nevertheless","new","next","nine","ninety","nobody","non","none","nonetheless","noone","normally","nos","noted","nothing","nowhere","obtain","obtained","obviously","often","oh","ok","okay","old","omitted","one","ones","onto","ord","others","otherwise","outside","overall","owing","p","page","pages","part","particular","particularly","past","per","perhaps","placed","please","plus","poorly","possible","possibly","potentially","pp","predominantly","present","previously","primarily","probably","promptly","proud","provides","put","q","que","quickly","quite","qv","r","ran","rather","rd","readily","really","recent","recently","ref","refs","regarding","regardless","regards","related","relatively","research","respectively","resulted","resulting","results","right","run","said","saw","say","saying","says","sec","section","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sent","seven","several","shall","shed","shes","show","showed","shown","showns","shows","significant","significantly","similar","similarly","since","six","slightly","somebody","somehow","someone","somethan","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specifically","specified","specify","specifying","still","stop","strongly","sub","substantially","successfully","sufficiently","suggest","sup","sure","take","taken","taking","tell","tends","th","thank","thanks","thanx","thats","that've","thence","thereafter","thereby","thered","therefore","therein","there'll","thereof","therere","theres","thereto","thereupon","there've","theyd","theyre","think","thou","though","thoughh","thousand","throug","throughout","thru","thus","til","tip","together","took","toward","towards","tried","tries","truly","try","trying","ts","twice","two","u","un","unfortunately","unless","unlike","unlikely","unto","upon","ups","us","use","used","useful","usefully","usefulness","uses","using","usually","v","value","various","'ve","via","viz","vol","vols","vs","w","want","wants","wasnt","way","wed","welcome","went","werent","whatever","what'll","whats","whence","whenever","whereafter","whereas","whereby","wherein","wheres","whereupon","wherever","whether","whim","whither","whod","whoever","whole","who'll","whomever","whos","whose","widely","willing","wish","within","without","wont","words","world","wouldnt","www","x","yes","yet","youd","youre","z","zero","a's","ain't","allow","allows","apart","appear","appreciate","appropriate","associated","best","better","c'mon","c's","cant","changes","clearly","concerning","consequently","consider","considering","corresponding","course","currently","definitely","described","despite","entirely","exactly","example","going","greetings","hello","help","hopefully","ignored","inasmuch","indicate","indicated","indicates","inner","insofar","it'd","keep","keeps","novel","presumably","reasonably","second","secondly","sensible","serious","seriously","sure","t's","third","thorough","thoroughly","three","well","wonder", "â", "la", "de", "doesnt", 'isnt']

def tokenizer(text, stopword=True):
    if stopword:
        stopwordlist = stopwords()
        tokens = [token for token in text.lower().split(' ') if token not in stopwordlist]
    
    else:
        tokens = text.split()
    
    return tokens

def word_count(text, sort = True, stopword=False):
    counter = {}
    for word in tokenizer(text, stopword=stopword):
        counter.setdefault(word, 0)
        counter[word] = counter[word] + 1
    
    if sort:
        counter = dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))

    return counter

def get_top_words_for_genre(df, genre_top, num_words=100, useStopword = True):
    # create mask for boolean indexing using anonymous callback function, since tokenization returned a list, checks for 'fantasy' in each element in the genre column (x)
    corpus = get_corpus_from_genre_index(df, genre_top, 'desc')
    topWordList = []
    wc = word_count(' '.join(corpus), stopword = useStopword)
    topWord = list(wc.keys())
    for i in range(0, num_words):
        topWordList.append(topWord[i])
    return topWordList

def get_frequency_top_words(corpus, genre_top):
    top_word_frequency = []
    for desc in corpus:
        top_word_frequency.append(sum(el in genre_top for el in desc))
    return np.asarray(top_word_frequency)

def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

def venn_diagram_visualization(genre1, genre1_label, genre2, genre2_label):
    plt.figure(figsize=(10,8))
    venn2([set(genre1), set(genre2)], set_labels=(genre1_label, genre2_label), set_colors=('blue', 'green'), alpha=0.7)
    plt.title(f'Top 100 most frequent words intersection between the {genre1_label} and {genre2_label} genres')
    plt.savefig(f'figures/venn_diagram/{create_underscore_string(genre1_label)}_{create_underscore_string(genre2_label)}_intersection.png')
    print(f'\nThe intersection has been visualized as a venn diagram, and has been saved as {create_underscore_string(genre1_label)}_{create_underscore_string(genre2_label)}_intersection.png')

def main():
    dataframe = pruning_csv('GoodReads_100k_books', 'csv', columns_to_tokenize=[{'column':'genre', 'split':','}])
    fantasy_genre = get_top_words_for_genre(df=dataframe, genre_top='fantasy')
    science_fiction_genre = get_top_words_for_genre(df=dataframe, genre_top='science fiction')
    nonfiction_genre = get_top_words_for_genre(df=dataframe, genre_top='nonfiction')
    print(f'\n[RESULTS] The top 100 most frequent words occuring in book descriptions for books belonging to the fantasy genre can be seen below: \n{fantasy_genre}')
    print(f'\n[RESULTS] The intersection between Fantasy and Science Fiction can be seen below: \n{intersection(fantasy_genre, science_fiction_genre)}')
    print(f'\n[RESULTS] The intersection between Fantasy and Nonfiction can be seen below: \n{intersection(fantasy_genre, nonfiction_genre)}')
    venn_diagram_visualization(fantasy_genre, 'Fantasy', science_fiction_genre, 'Science Fiction')
    venn_diagram_visualization(fantasy_genre, 'Fantasy', nonfiction_genre, 'Nonfiction')
    venn_diagram_visualization(science_fiction_genre, 'Science Fiction', nonfiction_genre, 'Nonfiction')
    
if __name__ == '__main__':
    main()