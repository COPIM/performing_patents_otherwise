# @name: conversations.py
# @creation_date: 2022-10-27
# @license: The MIT License <https://opensource.org/licenses/MIT>
# @author: Simon Bowie <ad7588@coventry.ac.uk>
# @purpose: conversations route for Section 2: Archive Conversations
# @acknowledgements:

from flask import Blueprint, render_template
import markdown

conversations = Blueprint('conversations', __name__)

@conversations.route('/conversations/')
def index():
    with open('content/section_2/conversations.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('conversations.html', text=text)

# route for Martha Gowans page
@conversations.route('/conversations/martha')
def martha():
    with open('content/section_2/I-Martha-gowans.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('conversations.html', text=text)