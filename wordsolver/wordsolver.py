
import requests
#import pprint
#import urllib.request
#from bs4 import BeautifulSoup
import re

"""target = '????s??'
clue_words = ['accumulate', 'accumulates']
length = len(target)"""


def get_matches(target):
    ########### FIND POTENTIAL MATCHES ###########
    length = len(target)
    matches = []

    word_list = open('wordsolver/word_list.txt', 'r')
    len_word_list = 0

    for word in word_list:
        word = word.strip()
        len_word_list += 1

        if len(word) == length:
            matching = True

            for i, letter in enumerate(word):
                if target[i] != "?" and letter != target[i]:
                    matching = False

            if matching == True:
                matches.append(word)

    word_list.close()
    return matches

    """########### GET SUMMARY FOR EACH POTENTIAL MATCH ###########

    wiki_texts = [[] for x in range(len(matches))]
    #pp = pprint.PrettyPrinter(indent=3)
    #print('\n\nLooking for text ')
    for i, word in enumerate(matches):
        entries = []
        query = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&redirects=1&format=json&titles=' + word
        r = requests.get(query)
        result_object = r.json()

        key = list(result_object['query']['pages'].keys())[0]
        if key == '-1': # no result - look up in dictionary
            query = 'https://en.wiktionary.org/wiki/' + word
            result = requests.get(query) #urllib.request.urlopen(query).read()
            text = result.text
            try:
                start = re.search('id="Translations', text) #(.+?)style="text-align:left;">
                text = text[start.end():]
                start = re.search('style="text-align:left;">', text)
                text = text[start.end():]
                end = re.search("</div>", text)
                text = text[:end.start()]
                entries.append(text)
            except:
                entries.append('not found')
                wiki_texts[i].append(entries)

        else:
            extract = result_object['query']['pages'][key]['extract']

            if 'may refer to' in extract: # result is a disambiguation page

                try:
                    query = 'https://en.wikipedia.org/wiki/' + word
                    result = requests.get(query) #urllib.request.urlopen(query).read()
                    text = result.text

                    start = re.search(' may refer to:</p>', text)
                    end = re.search('<span class="mw-headline" id="See_also">', text)

                    text = text[start.end():end.start()]
                    text = re.sub('<.+?>', '', text)
                    text = re.sub('\n\n\n', '\n', text)
                    text = re.sub('\n\n', '\n', text)

                    entries = text.split('\n')

                except:
                    entries.append('not found')
                    wiki_texts[i].append(entries)


            else:
                entries.append(extract) #if it isn't a disambiguation page we want it


            wiki_texts[i].append(entries)#entries is a list with the final info for this word
            #print('appended for ', word)


    ########### FIND THE BEST MATCHES BY SUMMARY CONTENT ###########

    scores = [0 for x in matches]

    for i in range(len(matches)):
        for word in clue_words:
            for l in wiki_texts[i]:
                for w in l:
                    if word in w:
                            scores[i] = scores[i] + 1


    ########### ORDER THE RESULTS ###########

    results = []


    maxi = 1

    while len(scores) > 0 and maxi > 0:
        maxi = max(scores)
        if maxi > 0:
            ind = scores.index(maxi)
            result = [matches[ind], scores[i], wiki_texts[ind]]
            results.append(result)
            matches.pop(ind)
            scores.pop(ind)
            wiki_texts.pop(ind)"""

    """
    print('MATCHES FOR : "', target, '" (Clue words: ', clue_words, ' )\n')

    print('The most likely match: \n\n')


    for result in results:
        print(result[0])
        print(result[2], '\n')



    print('\nnOther potential matches are: \n')

    for i in range(len(matches)):
        print(matches[i])
        for entry in wiki_texts[i]:
            print(entry, '\n')"""
