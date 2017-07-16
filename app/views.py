import sys
from flask import render_template, session, request, jsonify
from wordsolver.wordsolver import get_matches, get_meaning
from app.forms import WordForm
from app import app

@app.route('/', methods=['GET', 'POST'])
def index():
    form = WordForm()

    if request.method == 'POST':
        target = form.target.data
        form.target.data = ""
        matches = get_matches(target)
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
    print('short meaning: ', meaning[:5])
    return jsonify(short_meaning=meaning[:5], long_meaning=meaning)
