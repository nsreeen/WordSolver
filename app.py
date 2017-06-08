from flask import Flask, render_template, session, request
from wordsolver.wordsolver import get_matches, get_meanings, get_good_matches
#from testimport import name
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form['target']
        clue_string = request.form['clue']
        clues = clue_string.split()
        matches = get_matches(target)
        matches_and_meanings = get_meanings(matches)
        print('\n matches_and_meanings : \n', matches_and_meanings)
        good_matches = get_good_matches(matches_and_meanings, clues)
        return render_template('index.html', target=target, clue='', matches_and_meanings=matches_and_meanings, good_matches=good_matches) #session['target'], clue=session['clue'])
    else:
        return render_template('index.html', target='', clue='', matches_and_meanings='', good_matches='')

app.secret_key = 'test'


if __name__ == '__main__':
    app.run()
