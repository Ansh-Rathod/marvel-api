from flask import *
import requests
import os

app = Flask(__name__, template_folder='./templates')


@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)


def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path, endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search', methods=['POST', 'GET'])
def search():
    r = requests.get(
        'https://gateway.marvel.com/v1/public/characters?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c')
    if request.method == 'POST':
        if request.form['Search'] == '':
            print('please enter')
        else:
            Search = request.form['Search']
            r = requests.get(
                'https://gateway.marvel.com/v1/public/characters?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c&nameStartsWith='+Search)
            return render_template('search.html', result=json.loads(r.text))

    return render_template('search.html', result=json.loads(r.text))


@app.route('/char/<string>')
def char(string):
    r = requests.get('https://gateway.marvel.com/v1/public/characters/'+string +
                     '?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c')
    comic = requests.get('https://gateway.marvel.com/v1/public/characters/'+string +
                         '/comics?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c')

    return render_template('char.html', result=json.loads(r.text), comics=json.loads(comic.text))


@app.route('/char/page/<string>')
def page(string):

    r = requests.get('https://gateway.marvel.com/v1/public/characters?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c&limit=100&offset='+str(int(string)*100))
    read = json.loads(r.text)

    next = int(string)+1
    prev = int(string)-1

    return render_template('page.html', result=read, number=next, prev=prev)


@app.route('/comics/page/<string>')
def comics_page(string):
    r = requests.get('https://gateway.marvel.com/v1/public/comics?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c&limit=100&offset='+str(int(string)*100))
    read = json.loads(r.text)

    next = int(string)+1
    prev = int(string)-1
    return render_template('comic.html', comics=read, number=next, prev=prev)


@app.route('/comics/<string>')
def comics_id(string):
    r = requests.get('https://gateway.marvel.com/v1/public/comics/'+string +
                     '?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c')
    return render_template('comicinfo.html', result=json.loads(r.text))


@app.route('/comicsearch', methods=['GET', 'POST'])
def comicsearch():
    if request.method == 'POST':
        Search = request.form['Search']

        r = requests.get(
            'https://gateway.marvel.com/v1/public/comics?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c&titleStartsWith='+Search)
        return render_template('comicsearch.html', comics=json.loads(r.text))

    return render_template('comicsearch.html')


@app.route('/comicsearchyear', methods=['GET', 'POST'])
def comicsearchyear():
    if request.method == 'POST':
        Search = request.form['Search']
        year = request.form['Year']
        r = requests.get(
            'https://gateway.marvel.com/v1/public/comics?ts=1&apikey=690e3ac16286c2de4591eca37269eedb&hash=fcbd875beb64e407e41ea8088ed2cd0c&titleStartsWith='+Search+'&startYear='+year)
        return render_template('comicsearch.html', comics=json.loads(r.text))
    return render_template('comicsearch.html')


if __name__ == '__main__':

    app.run()
