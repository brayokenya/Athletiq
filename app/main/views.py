from flask import render_template, request, redirect,url_for,abort
from . import main


#views
@main.route('/')
def index():
    '''
    view root page that retunrs index page with its data
    '''
    title = 'SPORTS APP'

    return render_template('index.html', title=title)    