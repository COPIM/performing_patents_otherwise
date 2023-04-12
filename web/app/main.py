# @name: main.py
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Main route for index page, contents, frontmatter, and other miscellaneous pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login

from flask import Blueprint, render_template
import markdown

main = Blueprint('main', __name__)

# route for index page
@main.route('/')
def index():
    return render_template('index.html')

# route for table of contents page
@main.route('/contents/')
def contents():
    with open('content/TOC.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('toc.html', text=text)

# route for introduction page
@main.route('/introduction/')
def foreword():
    with open('content/introduction.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for frontmatter page
@main.route('/frontmatter/')
def frontmatter():
    with open('content/frontmatter.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)