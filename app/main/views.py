from flask import render_template, request, redirect,url_for,abort
from . import main
from flask_login import login_required,current_user
from ..models import User,Team,Player
from .forms import UpdateProfile,TeamForm,PlayerForm
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
    check_team=Team.query.filter_by(user=manager).first()
    if check_team:
        return redirect(url_for('main.team_exists'))
      
    if form.validate_on_submit():

        team_name = form.team_name.data
        category=  form.category.data  
        location = form.location.data        

        # Updated team instance
        this_team = Team(team_name=team_name, category=category, user=manager,location=location, wins=0, draws=0, losses=0)

        # save comment method
        this_team.save_team()
        return redirect(url_for('.add_players'))  
    
    
    title = 'Create team'
    return render_template('create_team.html',title = title, team_form=form)  



@main.route('/team_exists')
def team_exists():
    
    return render_template("team_exists.html")  


@main.route('/add_players', methods=['GET', 'POST'])
@login_required
def add_players():
    manager=current_user
    form = PlayerForm()
    team=Team.query.filter_by(user=manager).first()
    players =Player.query.filter_by(player_team=team)  
      
    if form.validate_on_submit():

        name = form.name.data
        position= form.position.data          

        # Updated player instance
        this_player = Player(name=name, playing_position=position, player_team=team)

        # save player method
        this_player.save_player()
        return redirect(url_for('.add_players'))

    title = 'Add players'
    return render_template('add_players.html',title = title, player_form=form, team=team, players=players)



@main.route('/teams', methods=['GET'])
def teams():
    football=Team.query.filter_by(category='football').all()
    basketball=Team.query.filter_by(category='basketball').all()
    cricket=Team.query.filter_by(category='cricket').all()              
    hockey=Team.query.filter_by(category='hockey').all()
    rugby=Team.query.filter_by(category='rugby').all()

    title='Teams'
    return render_template('teams.html', title=title, football=football, cricket=cricket, basketball=basketball, hockey=hockey, rugby=rugby)



@main.route('/teams/<team_id>', methods=['GET'])
def view_team(team_id):
    team=Team.query.filter_by(id=team_id).first()
    players=Player.query.filter_by(player_team=team)

    title=team.team_name
    return render_template('view_team.html', team=team, players=players)

# @main.route('/fixture', methods=['GET', 'POST'])
# @login_required
# def book_fixture():

#     form = FixtureForm()
#     '''
#     view page that retunrs fixture page with its data
#     '''
    
#     title = 'Book a Fixture'


#     return render_template('fixture.html', title=title, fixture_form=form)