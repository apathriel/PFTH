# Assignment 2 - Word Importance

By Gabriel Høst Andersen, PFTH, 2022.

Code was discussed with my group.

Group members: Albin Sand, Gabriel Høst Andersen, Lissa Bui, Victor Rasmussen.
  
## Problem 1: With or without function words

After completing the prerequisites specificed in the assignment, I was able to successfully retrieve the most frequent occuring words by calling the word_count function, which was in turn called through the calling of the main function. 

Our first focus was to find a method that was able to retrieve a range from the returned dictionary of occurances.  Even though the dictionary had been sorted using the sorted method.

 ````py

def  word_count(text, sort = True, stopword=False):

#count words, with optional sorting and stopwords

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

![Console output of Problem 1 is dispalyed](https://lh3.googleusercontent.com/fNBeRWBq5NORGifBSboYneOR39USl0vYOhLmAMUyMjHp0D8TnYh_IjjqewpAztDeW9M1lPo3e8-bZIXVrbTy6FKVgkGwJxKntneqUZaOaKpSY7cfZsx5WNXpPDWOM3jXB8JfMYnqjPJfv9KfTFILxr6ac8DyMbHgOOXnychaNa8hSuESBasrxvyK09cL1sSM6KZBlvTD_XFH4rbU5hZxkp6FMF3zY_nZLaByEa4NH66NCG_5rr1nCgWx4WJJXGkE8r-RBLUIoI0Su8xqAPBI7C4RdtQ2UOfPFCNDkuK0wrhNgCFmwk_Q1tC7cxYUCDN3DyzClXcr3PNaVdjCdeO8B9pIBe_8mobW1ConQ-Z9MHMMtXFF9mpagLbezE0jxFQmiKwp_mB2Ow5nimjyJnHt25Y7yI3MeLtwyhqY_ZBK-MsPezmRPmTENwau-ngZaY_C2qcynQO8fSDM90kmyQJbxaln0E1fRpJTI4rPwtgdutOSYQ7t0j3cnoEC20XDwgmXVpQ3tjCG7Bp-1QBR_osWyhF0ePLlENMNMYaKUG9zcIH8nabBO36qPArVz1ZtPUoq5ywmbE2w8M91pjl1xAn7gcCb-iPr_fhL-xP7_pe91jOEoOtWp0z7eXwax_vtT-kcW05umJ_00Xhh-WX2fMQFpgyO5DaQdZisTCkA8P2rdm2DU8DhkSKTv8lwYMihg99fQHgdqvByAKqYetC_6insdfUz5pzhzGNrEP9Nz90KJlguEzd2sREfElnqbtmiHv3xZIBVP9wyX8V3bzL_mcxZCM7hxdIsVEGbKztq0tl2hd36mI0LC4tIZJ3mSXDNytCdLItnziFYVpad-lHfX1Opbs0kLqrdwMxLl9sZbquiIo0Pf-wvJDSVrfZuBloSiahrG9lvDYcbMKRWZiptcnvsTDy9LzlccP_wCEzPCqGcOuvDGh64xN02ng8-pqGvecELwSpsZV0S03PZ3q14kTV2mYeX67be6nBip70ThBM2zRJAP7Y=w1475-h300-no?authuser=0)

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

![Results from comparing zodiac sign horoscopes](https://lh3.googleusercontent.com/vASi-MrJQfGAmldVwAb2nz0kYPgzAzMs-L45zpyyDAr32LuDY6BM5VZQu8XRpbN5hIhiVSXb59Yz09clRR8xL7DX1809en_OJ2ScVWYJFgDKKl9pQj6hu-m-36O4j8vExizsVoVEMeBnRtEupqczGBO351SWEkujNTBu5mv57EVDzSgXTq7k9xTyoAJi7DWgLnXQztT68u6MSFVHNLg56kDvkpZCTvtppCCMxvo8Yy-qkXmlrD1KmsIDLEugTFM7MJJPFW2GEg4-l1WqIclc-Em4Jb5umVyeWs8uAcc5JDSvZugZYygZfScF6WJOCHuBfUAdxS0vseRJf_XYzYZKKv5YPoYPVjATtCq8vR-kUasgXOIRXFYj7w-T4jT9w-OnqEP3h69ZUpbEnZJoD3FcQs_7gGQ5aewzkGppRFEhoFlwNW4xEBDahf8l9SDhs02ixrgDLj-sJuGN6QIoZNPReZ_OBPOfqabrLguaAndZNtfbaj5ljnePhdqyFRSxIkuHjGDki6zxdukIUwlJKv3WEwzUChBtYBA10yo937gSs2w-d-xOQTzLl3dX81Cp--L0V-EltwNBZZe9i-phpZe6V4JTpVpakLrrjBeCY65pSBIqpC_Ddrl6swTFKzQS09o2Afv6J7dTaDBaoePtDyFC_ldtNh9covn7mAVWnCuzHuxsxAREu246PhQ5v7QRncNixTFjfF4c59X_sTHeD_4MZnROJxYb_aXt4-e2DDX2Bkv2MGR9oRTqludglMlQrLzS4ZLBlgZxbA440utYVdlEWGqQW8rm684pdfAIieOpLJ0nm52Boy68yUDpYQ1Lmc20F9M9=w1486-h480-no?authuser=0)

The question posed is: ***Are there any apparent characteristics/distinct differences between the signs?***

The most obvious conclusions to draw from these results, is that cancer and aries are the most similiar, whilst capricorn and aries are the most different. This can be done be the simple eye-test of the list lengths (and can be confirmed by printing the len of the difference). 

Another obvious conclusion to draw is that the differences are few, compared to the 200 words that we pulled. This obviously means that there's a large intersection between the specific horoscopes, speaking to the normative nature of these horoscopes. 

You can also look at the adjectives used, in order to analyze which "profiles" that are associated with the specific signs.

Obviously the characteristics produced by the result are a product of the specific sign's relation to the other signs we chose. One could also look at intersections between present in aries but not in capricorn and present in aries but not in cancer. Thus, you'd be able to find the which characteristics not present in aries, that neither occur in capricorn nor cancer. Thus defining the relationship between cancer and capricorn based on- or in relation to, their differences to aries.

