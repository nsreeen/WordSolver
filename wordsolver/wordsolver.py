import requests
import re


# GET POTENTIAL MATCHES
def get_matches(target):
    length = len(target)
    matches = []

    word_list = open('wordsolver/word_list.txt', 'r') #wordsolver/
    len_word_list = 0

    for word in word_list:
        word = word.strip()
        len_word_list += 1

        if len(word) == length:
            matching = True

            for i, letter in enumerate(word):
                if letter != "_" and target[i] == "_" or \
                   target[i] != "?" and letter != target[i]:
                    matching = False

            if matching == True:
                matches.append(word)

    word_list.close()
    return matches


# GET WORD MEANING
def get_meanings(matches):
    matches_and_meanings = {}

    for word in matches:
        extract = get_wikipedia_extract(word)
        disambiguation = get_wikipedia_disambiguation_page(word)
        #definition = get_wiktionary_meaning(word) # won't use this for now

        extract = clean(extract)
        #disambiguation = clean(disambiguation) # unnecessary

        if 'may refer to:' in extract:
            meaning = extract.split(' . ')
            meaning = meaning[1:]
        else:
            meaning = [extract]

        matches_and_meanings[word] = meaning

    return matches_and_meanings


def clean(text):
    text = re.sub('\n\n\n', '', text)
    text = re.sub('\n\n', '', text)
    text = re.sub('\n', '', text)
    text = re.sub('<li>.+?,', ' . ', text)
    text = re.sub('<.+?>', '', text)
    text = re.sub(r'\[(edit)\]', '', text) #<-- this line breaks it
    return text


def get_wikipedia_extract(word):
    try:
        query = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&redirects=1&format=json&titles=' + word
        r = requests.get(query)
        result_object = r.json()
        key = list(result_object['query']['pages'].keys())[0]
        if key != None:
            extract = result_object['query']['pages'][key]['extract']
            if word + ' may refer to:' not in extract:
                return extract
        return ''
    except:
        return ''


def get_wikipedia_disambiguation_page(word):
    try:
        query = 'https://en.wikipedia.org/wiki/' + word
        #try here?
        result = requests.get(query)
        text = result.text

        start = re.search(' may refer to:</p>', text)
        end = re.search('<span class="mw-headline" id="See_also">', text)

        text = text[start.end():end.start()]

        return text
    except:
        return ''


def get_wiktionary_meaning(word):
    query = 'https://en.wiktionary.org/wiki/' + word
    result = requests.get(query) #urllib.request.urlopen(query).read()
    text = result.text
    #print('\n\n', word, ' wiktionary: ', text)
    try:
        start = re.search('id="Translations', text) #(.+?)style="text-align:left;">
        text = text[start.end():]
        start = re.search('style="text-align:left;">', text)
        text = text[start.end():]
        end = re.search("</div>", text)
        text = text[:end.start()]
        return meaning
    except:
        return ''


# RATE MEANINGS BASED ON CLUES TO FIND THE BEST MATCHES
def get_score(meaning, clues):
    score = 0
    for clue_word in clues:
        for item in meaning:
            if clue_word in item:
                score = score + 1
    return score


def get_good_matches(matches_meanings_dict, clue_string):
    scores_dict = {} # might use this later to give better suggestions

    clues = clue_string.split()

    for word, meaning in matches_meanings_dict.items():
        score = get_score(meaning, clues)
        scores_dict[word] = score

    matches = scores_dict.keys()
    ordered_matches = sorted(matches, reverse=True, key=lambda word: scores_dict[word])

    return ordered_matches


"""word = "?ye"
clues = "vision sight see light"
matches = get_matches(word)
meaningsdict = get_meanings(matches)
ordered_matches = get_good_matches(meaningsdict, clues)"""
