import sys
from nltk import ngrams
import textstat
textstat.set_lang('es')
import spacy
nlp = spacy.load('es_core_news_md')


def getRepeatedKeywords(context, keywords):
    amount = 0
    document = nlp(context)
    documentlength = len(context.split())
    finalvalue = 0
    keys = keywords.copy()
    for token in document:
        if token.text in keys and token.tag_ != 'PUNCT':
            keys.remove(token.text)
            amount = amount + 1  
    return amount

def getRepeatedDerivedWords(context, keywords):
    amount = 0
    document = nlp(context)
    documentlength = len(context.split())
    finalvalue = 0
    keys = keywords.copy()
    for token in document:
        if token.lemma_ in keys:
            keys.remove(token.lemma_)
            amount = amount + 1  
    return amount

def getSentenceContainedinContext(context, text):
    result = 0
    textlength = len(text.split())
    ngramscontext = ngrams(context.split(), textlength)
    for grams in ngramscontext:
        if grams == tuple(text.split()):
            result = result + 1
    return result


def getReadability(context):
    value = 0
    finalvalue = 0
    value = textstat.fernandez_huerta(context)
    if value < 0: 
        value = 0
    if value > 121.22:
        value = 121.22
    finalvalue = (121.22 - value) / (121.22 - 0)    
    return finalvalue

def getLength(context):
    document = nlp(context)
    difference = 0
    documentlength = len(context.split())
    finalvalue = 0
    if documentlength > 45: 
        difference = documentlength - 45
        finalvalue = difference/45
        if finalvalue > 1:
            finalvalue = 1
    return finalvalue

def getTextSimilarity(context, text):
    result = 0
    contextList = context.split(".")
    for c in contextList:
        s1 = nlp(c)
        s2 = nlp(text)
        similarity = s1.similarity(s2)
        if similarity > result:
            result = similarity
    return result

def normalisekeywords(repeated):
    min = 0
    max = 3
    result = 0
    if repeated > 3:
        result = (repeated - min)/ (max - min)
    else:
        result = repeated
    return result

def linearComb(repeatedKeywords, repeatedDerivedWords, sentenceinContext, readability, length, similarity):
    cons = 1/6
    result = (repeatedKeywords * cons) + (repeatedDerivedWords * cons) + (sentenceinContext * cons) + (readability * cons) + (length*cons) + (similarity* cons)
    return result

def main():
    # Check if all the values are provided
    if len(sys.argv) != 6:
        print("Usage: python cats.py <premise_sentence> <keyword1> <keyword2> <keyword3> <context>")
        sys.exit(1)
    
    # Get the data from the command line argument
    premisesentence = sys.argv[1]
    keyword1 = sys.argv[2]
    keyword2 = sys.argv[3]
    keyword3 = sys.argv[4]
    context = sys.argv[5]
    keywords = [keyword1, keyword2, keyword3]
   
    # Print the data
    print(f"Premise sentence: {premisesentence}")
    print(f"Keyword 1: {keyword1}")
    print(f"Keyword 2: {keyword2}")
    print(f"Keyword 3: {keyword3}")
    print(f"Contexts: {context}")

    #Get the values for each parameter
    nlp = spacy.load('es_core_news_md')
    repeatedKeywords = getRepeatedKeywords(context, keywords)
    repeatedDerivedWords = getRepeatedDerivedWords(context, keywords)
    sentenceinContext = getSentenceContainedinContext(context, premisesentence)
    readability = getReadability(context)
    length = getLength(context)
    similarity = getTextSimilarity(context, premisesentence)
    repeatedKeywords = normalisekeywords(repeatedKeywords)
    repeatedDerivedWords = normalisekeywords(repeatedDerivedWords)

    #Perform the linear combination
    result = linearComb(repeatedKeywords, repeatedDerivedWords, sentenceinContext, readability, length, similarity)

    #Print the score of CATS
    print(f"--------------------------------------------------------------------------------------------------------")
    print(f"CATS Score: {result}")



if __name__ == "__main__":
    main()