import requests
import re


# GET POTENTIAL MATCHES

def get_matches(target):
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



# GET WORD MEANING

def get_meanings(matches):
    matches_and_meanings = {}

    for word in matches:
        meaning = get_wikipedia_extract(word)
        if meaning == None:
            meaning = '/' + get_wikipedia_disambiguation_page(word)
        if meaning == None:
            meaning = get_wictionary_meaning(word)

        #meaning = clean(meaning)
        matches_and_meanings[word] = meaning

    return matches_and_meanings


def clean(text):
    #remove double line breaks
    text = re.sub('\n\n\n', '\n', text)
    text = re.sub('\n\n', '\n', text)
    #remove html tags
    text = re.sub('<.+?>', '', text)
    return text


def get_wikipedia_extract(word):
    query = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&redirects=1&format=json&titles=' + word
    r = requests.get(query)
    result_object = r.json()
    key = list(result_object['query']['pages'].keys())[0]
    if key != None:
        extract = result_object['query']['pages'][key]['extract']
        if '</b> may refer to:</p>' not in extract:
            return extract
    return None


def get_wikipedia_disambiguation_page(word):
    query = 'https://en.wikipedia.org/wiki/' + word
    #try here?
    result = requests.get(query)
    text = result.text

    start = re.search(' may refer to:</p>', text)
    end = re.search('<span class="mw-headline" id="See_also">', text)

    text = text[start.end():end.start()]

    return text


def get_wictionary_meaning(word):
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
        return meaning
    except:
        return None



# RATE MEANINGS BASED ON CLUES TO FIND THE BEST MATCHES

def get_score(meaning, clues):
    score = 0
    for clue_word in clues:
        if clue_word in meaning:
            score = score + 1
    return score


def get_good_matches(matches_meanings_dict, clues):
    scores_dict = {} # might use this later to give better suggestions
    good_matches = []

    for word, meaning in matches_meanings_dict.items():
        score = get_score(meaning, clues)
        scores_dict[word] = score
        if score > 0:
            good_matches.append(word)
        print(word, score)

    return good_matches
