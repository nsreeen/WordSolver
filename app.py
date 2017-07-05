import sys
from flask import Flask, render_template, session, request, jsonify
from wordsolver.wordsolver import get_matches, get_meanings, get_good_matches, get_meaning
from forms import WordForm

app = Flask(__name__)

app.secret_key = 'test'

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WordForm()

    if request.method == 'POST': 
        print(request)
        target = form.target.data
        form.target.data = ""

        matches = get_matches(target)
        print(matches)
        return render_template('results.html', target=target, form=form, matches=matches)
    else:
        return render_template('index.html', target='', form=form, matches='')

@app.route('/results', methods=['GET', 'POST'])
def results():
        return render_template('results.html', target=target, clue='', matches=matches)

@app.route('/getmeaning', methods=['POST'])
def getmeaning():
    word = request.form['word']
    meaning = get_meaning(word)
    return jsonify(meaning=meaning)

if __name__ == '__main__':
    port = int(sys.argv[1])
    app.run(host='0.0.0.0', port=port)




"""@app.route('/', methods=['GET', 'POST'])
def index():
    form = WordForm()

    if request.method == 'POST': #this should be GET! also maybe I should make a database for the synonyms? or a hashtable?? for crossword solver part of it, how would that work?
        print(request)
        target = form.target.data
        clue = form.clue.data

        matches = get_matches(target)
        print(matches)
        matches_and_meanings = get_meanings(matches)
        ordered_matches = get_good_matches(matches_and_meanings, clue)
        return render_template('index.html', target=target, clue='', form=form, matches_and_meanings=matches_and_meanings, ordered_matches=ordered_matches)
    else:
        return render_template('index.html', target='', clue='', form=form, matches_and_meanings='', ordered_matches='')
"""
