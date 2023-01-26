# Assignment 2 - Word Importance

<p> <strong> By Gabriel Høst Andersen, PFTH, 2022. </strong> </p>

Code was discussed with my group.

Group members: Albin Sand, Gabriel Høst Andersen, Lissa Bui, Victor Rasmussen.

<h2> How to  execute </h2>

<p> Ensure that the dependencies  are correctly installed. </p>

```
pip  install  -r  requirements.txt
```
<p>  Then execute the script (example for win below)

````
python ./word_importance.py
````
  
## Problem 1: With or without function words

After completing the prerequisites specificed in the assignment, I was able to successfully retrieve the most frequent occuring words by calling the word_count function, which was in turn called through the calling of the main function. 

Our first focus was to find a method that was able to retrieve a range from the returned dictionary of occurances.  Even though the dictionary had been sorted using the sorted method.

 ````py

def  word_count(text, sort = True, stopword=False):

counter = {}

for  word  in  tokenizer(text, stopword=stopword):

	counter.setdefault(word, 0)

	counter[word] = counter[word] + 1

if  sort:

	counter = dict(sorted(counter.items(), key=operator.itemgetter(1), reverse=True))

return  counter

  ````
  
 Although the dictionary had been sorted, we were not able to found a sufficient method that would easily allow us to slice the returned dictionary. Instead we opted to incorporate the following function.
````py

def  topWords(useStopword = True):

horoscopeClean = df['horoscope-clean']

topWordList = []

wc = word_count(' '.join(horoscopeClean), sort = True, stopword = useStopword)

for  i  in  range(0, 100):

	topWord = list(wc.keys())[i]

	topWordList.append(topWord)

return  topWordList

````

By using this method, we were able to utilize the dictionary having been ordered, by iterating through the keys specified in the range, and using the list method .append(), in order to create our lists.

We included the parameter, so we could create two seperate lists, with and without stopwords.

We used the stopWordsList that was included in /src/word_importance.py [stopWordsList](https://github.com/CHCAA-EDUX/Programming-for-the-Humanities-E22/blob/main/src/word_importance.py)

Then we used the accompanying intersection() and difference() functions to retrieve the desired data.

Thus we arrive at the question: ***What seems to be the most striking differences?***

![Console output of Problem 1 is dispalyed](P1_IMG.PNG)

I was initially surprised by the low frequency of intersection between the two lists, though this is largely a testament to the thoroughness of the stopwordList in stopwords() (and perhaps the predictability of the english language). 

The most striking thing about these results is the necessity for incorporating stopwords in your analysis. If one's intent is to perform data analysis on these horoscopes through word frequencies / word importance, one would have to say the results from the difference occuring in the stopwords list would prove more beneficial to such an analysis. 

Of course, a use-case for this comparison would be the intersection. None of the words returned from the intersection() function occur in the stopwordList, which highlights their large frequency within the text, since they were able to still be included in the list without stopwords. Potentially this could also be utilized to surmise additions or evaluate excisting lists of stopwords in specific contexts (in this case horoscopes). 

---
## Problem 2 - Sign-specific indexing

We started by using the specificed methods for extracting the horoscopes for individual zodiac signs. 
We incorporated these selectors in the topWords() function we created earlier:

````py


specificZodiac = df['sign'] == sign

horoscopeSpecific = df['horoscope-clean'].loc[specificZodiac].values

````

We added the sign parameter, so we could easily pass multiple different signs as arguments. We also modified the for loop to iterate through the 200 most frequent words.

![Results from comparing zodiac sign horoscopes](P2_IMG.PNG)

The question posed is: ***Are there any apparent characteristics/distinct differences between the signs?***

The most obvious conclusions to draw from these results, is that cancer and aries are the most similiar, whilst capricorn and aries are the most different. This can be done be the simple eye-test of the list lengths (and can be confirmed by printing the len of the difference). 

Another obvious conclusion to draw is that the differences are few, compared to the 200 words that we pulled. This obviously means that there's a large intersection between the specific horoscopes, speaking to the normative nature of these horoscopes. 

You can also look at the adjectives used, in order to analyze which "profiles" that are associated with the specific signs.

Obviously the characteristics produced by the result are a product of the specific sign's relation to the other signs we chose. One could also look at intersections between present in aries but not in capricorn and present in aries but not in cancer. Thus, you'd be able to find the which characteristics not present in aries, that neither occur in capricorn nor cancer. Thus defining the relationship between cancer and capricorn based on- or in relation to, their differences to aries.

