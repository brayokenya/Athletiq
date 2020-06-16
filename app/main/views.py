from flask import render_template, request, redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Team
from .forms import UpdateProfile,TeamForm
from .. import db,photos


#views
@main.route('/')
def index():
    '''
    view root page that retunrs index page with its data
    '''
    title = 'SPORTS APP'

    return render_template('index.html', title=title)

@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username = uname).first()

    if user is None:
        abort(404)

    return render_template("profile/profile.html", user=user)

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html', form=form)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile', uname=uname))


@main.route('/create_team', methods=['GET', 'POST'])
@login_required
def create_team():
    manager=current_user
    form = TeamForm()
    check_team=Team.query.filter_by(manager=manager).first()
    if check_team:
        abort(404)
      
    if form.validate_on_submit():

        team_name = form.team_name.data
        category=  form.category.data          

        # Updated team instance
        this_team = Team(team_name=team_name, category=category, manager=manager, wins=0, draws=0, losses=0)

        # save comment method
        this_team.save_team()
        return redirect(url_for('.index'))  
    
    
    title = 'Create team'
    return render_template('create_team.html',title = title, team_form=form)    
                