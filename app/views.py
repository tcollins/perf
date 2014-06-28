# Flask imports
from flask import render_template, url_for

from app import app

# Front page
@app.route('/index')
@app.route('/')
def index():
    return render_template("hello.html")

@app.route('/tim')
def tim():
    return "TIM"