import markdown
from flask import Flask
from flask import render_template
from flask import Markup
from flask import request
from flask import abort, redirect, url_for
import os
import glob

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.realpath(__file__))
DEBUG = True



@app.route('/')
def home():
    content = """#  Mymark

        markdown app
    """
    title ="mymark"
    return render_template('index.html', content=Markup(markdown.markdown(content)), title=title)



@app.route('/<md>')
def index(md):
    try:
        content = Markup(markdown.markdown(''.join(open('markdown/' + md + '.md', 'r').readlines())))
    except Exception, e:
        return redirect(md + '/edit')

    title = md
    return render_template('index.html', content=content, title=md)

@app.route('/<md>/edit', methods=['GET', 'POST'])
def edit(md = 'index'):
    if request.method == 'POST':
        f = open('markdown/' + md + '.md', "w")
        f.write(request.form['text'])
        f.close()
        return redirect(md)
    else:

        try:
            content = ''.join(open('markdown/' + md + '.md', 'r').readlines())
        except Exception, e:
            content = "# " + md

        return render_template('form.html', content=content)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)
