# @name: main.py
# @creation_date: 2022-09-07
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: Main route for index page, contents, frontmatter, and other miscellaneous pages
# @acknowledgements:
# https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
# https://www.reddit.com/r/flask/comments/k1bvw4/password_protect_pages/

from flask import Blueprint, render_template, session, request, redirect, url_for, flash
import markdown
import os
from functools import wraps

main = Blueprint('main', __name__)

site_password = os.getenv('SITE_PASSWORD')

# custom decorator to check password
def check_pw(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        status = session.get('status')
        if status != "good":
            return redirect(url_for('main.login'))
        return func(*args, **kwargs)

    return decorated_function

# route for index page
@main.route('/')
@check_pw
def index():
    return render_template('index.html')

# route for site login page
@main.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        req = request.form
        password = req.get("password")
    
        if password != site_password:
            flash('wrong password! try again...')
            return redirect(request.url)
        
        session["status"] = 'good'
        return redirect(url_for("main.index"))

    return render_template('login.html')

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