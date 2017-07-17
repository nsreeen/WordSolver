import requests
import re

# open list of words
with open('wordsolver/word_list.txt') as f:
    words = set(f.read().splitlines())

# GET POTENTIAL MATCHES
def get_matches(target):
    target = target.lower()
    len_target = len(target)
    matches = []

    length_matches = [word for word in words if len(word) == len_target]

    for word in length_matches:
        matching = True

        for i, letter in enumerate(word):
            if letter != "_" and target[i] == "_" or \
               target[i] != "?" and letter != target[i]:
                matching = False

        if matching == True:
            matches.append(word)

    return matches


# GET WORD MEANINGS
def get_meanings(matches):
    matches_and_meanings = {}

    for word in matches:
        meaning = get_meaning(word)
        matches_and_meanings[word] = meaning

    return matches_and_meanings

def get_meaning(word):
    extract = get_wikipedia_extract(word)
    if 'may refer to:' in extract:
        extract = clean_disambiguation(extract, word)
    else:
        extract = clean(extract)
    return extract

def clean(text):
    patterns = [r'\n\n\n', r'\n\n', r'\n', r'<.+?>', r'\[(edit)\]']
    for pattern in patterns:
        text = re.sub(pattern, '', text)
    return text

def clean_disambiguation(text, word):
    cut = text.find('may refer to:') + len('may refer to:')
    start = text[:cut]
    text = text[cut:]
    text = re.sub(r'</dt>', '', text)
    text = re.sub(r'<dt>', '', text)
    text = re.sub(r'</dl>', '', text)
    text = re.sub(r'<dl>', '<br>', text)
    text = start + text
    return text

def get_wikipedia_extract(word):
    try:
        query = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&redirects=1&format=json&titles=' + word
        r = requests.get(query)
        result_object = r.json()
        key = list(result_object['query']['pages'].keys())[0]
        if key != None:
            extract = result_object['query']['pages'][key]['extract']
            return extract
        return ''
    except:
        return ''


def get_wikipedia_disambiguation_page(word):
    try:
        query = 'https://en.wikipedia.org/wiki/' + word
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
    result = requests.get(query)
    text = result.text
    try:
        start = re.search('id="Translations', text)
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


def sort_matches(matches_meanings_dict, clues):
    scores_dict = {}

    for word, meaning in matches_meanings_dict.items():
        score = get_score(meaning, clues)
        if score > 0:
            scores_dict[word] = score

    matches = scores_dict.keys()
    ordered_matches = sorted(matches, reverse=True, key=lambda word: scores_dict[word])

    return ordered_matches



# TERMINAL TOOL

def print_match_and_meaning(match, meaning=None, full_meaning=False):
    print("\n", match)
    if len(meaning) == 1 and full_meaning == False:
        print(meaning[:200])
    elif len(meaning) == 1 and full_meaning == True:
        print(meaning)
    else:
        print("; ".join(meaning))
    print('\n')





if __name__ == "__main__":

    with open('wordsolver/stopwords.txt') as stopwordsfile:
        stopwords = [word.strip() for word in stopwordsfile]

    print("\nWelcome to wordsolver!")
    target = input("\nType target word pattern. Use '?' for unknown letters eg.'?y?'\n>>")
    clue = input("\nPlease type the clue\n>>")

    print("\n Please wait while matches are found\n")

    matches = get_matches(target)
    meanings_dict = get_meanings(matches)

    print("-----------------------------------------")

    for match, meaning in meanings_dict.items():
        print_match_and_meaning(match, meaning)

    print("-----------------------------------------")

    print("To sort the list and see the most likely matches, type 'sort'")
    print("To get the full meaning of a word, type the word")
    print("To quit, type 'q'")

    running = True

    while running:

        user_input = input(">>")

        if user_input == "q":
            running = False

        elif user_input == "sort":
            clues = [word for word in clue.split(" ") if word not in stopwords]
            sorted_matches = sort_matches(meanings_dict, clues)
            for match in sorted_matches:
                meaning = meanings_dict.get(match, None)
                print_match_and_meaning(match, meaning)

        else:
            meaning = meanings_dict.get(user_input, None)
            print_match_and_meaning(user_input, meaning, full_meaning=True)
