from flask import Flask, render_template, session, request
from wordsolver.wordsolver import get_matches
#from testimport import name
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        target = request.form['target']
        #clue = request.form['clue']
        #session['target'] = request.form['target']
        #session['clue'] = request.form['clue']
        results = get_matches(target)
        print(results)
        return render_template('index.html', target=target, clue='', results=results) #session['target'], clue=session['clue'])
    else:
        return render_template('index.html', target='', clue='', results=[])

app.secret_key = 'test'


if __name__ == '__main__':
    app.run()
