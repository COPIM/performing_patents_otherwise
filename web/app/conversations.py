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
    return render_template('conversations-overview.html', text=text)

# route for Martha Gowans page
@conversations.route('/conversations/i-martha-gowans')
def martha():
    with open('content/section_2/I-Martha-gowans.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for Sewing the Archive page
@conversations.route('/conversations/sewing-the-archive')
def sewing():
    with open('content/section_2/sewing-the-archive.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for Caribbean Quiilt page
@conversations.route('/conversations/caribbean-quilt')
def caribbean():
    with open('content/section_2/caribbean-quilt.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)

# route for Women on the Move page
@conversations.route('/conversations/women-on-the-move')
def women():
    with open('content/section_2/women-on-the-move.md', 'r') as f:
        text = f.read()
        text = markdown.markdown(text)
    return render_template('text.html', text=text)