from flask import Flask, render_template, session, request
from wordsolver.wordsolver import get_matches, get_meanings, get_good_matches
#from testimport import name
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form['target']
        clue = request.form['clue']

        matches = get_matches(target)
        matches_and_meanings = get_meanings(matches)
        ordered_matches = get_good_matches(matches_and_meanings, clue)

        return render_template('index.html', target=target, clue='', matches_and_meanings=matches_and_meanings, ordered_matches=ordered_matches) #session['target'], clue=session['clue'])
    else:
        return render_template('index.html', target='', clue='', matches_and_meanings='', ordered_matches='')

app.secret_key = 'test'


if __name__ == '__main__':
    app.run()
