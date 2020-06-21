from flask import render_template,redirect,url_for, flash,request
from . import auth
from ..models import User, Team, Fixture
from .. import db
from flask_login import login_user,logout_user,login_required,current_user
from .forms import LoginForm,RegistrationForm, FixtureForm
from ..email import mail_message, request_status
from itsdangerous.exc import SignatureExpired
from itsdangerous.url_safe import URLSafeTimedSerializer


s = URLSafeTimedSerializer('ebd2bf5d0f89d250ba9755f6ab75e9ff')

@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or Password')

    title = "SPORTS APP login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))
        title = "New Account"
    return render_template('auth/register.html', registration_form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))   

@auth.route('/fixture/<team_id>', methods=['GET', 'POST'])
@login_required
def book_fixture(team_id):
    fixture_form = FixtureForm()
    title = 'Book a Fixture'
    team = Team.query.filter_by(id=team_id).first() #team on template
    manager= team.user.username
    address = team.user.email
    requesting= Team.query.filter_by(manager=current_user.id).first() #requesting team
    print(requesting.team_name)
    print(team.team_name)
    if fixture_form.validate_on_submit():
        '''
        view page that returns fixture page with its data
        '''
        fixture= Fixture(date=fixture_form.Date.data,time=fixture_form.Time.data,location=fixture_form.Location.data, opponent=team.team_name, requester=requesting.team_name, confirmed=0, declined=0)
        db.session.add(fixture)
        db.session.commit()
        token = s.dumps(address, salt = 'fixture-confirm')
        link = url_for('auth.view_fixture', fixture_id=fixture.id, requesting_id=requesting.id, requested_id=team.id, token=token, _external=True)
        mail_message("ATHLETIQ: Fixture request","email/book_fixture",address,fixture=fixture, manager=manager, requesting=requesting, requested=team, link=link)
        flash('Your fixture has been posted! Please wait as we process your request', 'success')
        return redirect(url_for('auth.view_fixture',fixture_id=fixture.id, requesting_id=requesting.id, requested_id=team.id, token=token, title=title, team_id=team_id))

    return render_template('fixture.html', title=title, fixture_form=fixture_form)

@auth.route('/fixtures/<fixture_id>/<requesting_id>vs<requested_id>/<token>', methods=['GET'])
@login_required
def view_fixture(fixture_id,requesting_id,requested_id,token):
    fixture=Fixture.query.filter_by(id=fixture_id).first()
    requested=Team.query.filter_by(id=requested_id).first() #team on template
    requesting= Team.query.filter_by(manager=current_user.id).first() #name of requesting team
    print(fixture.requester)
    email= requested.user.email
    try:
        email = s.loads(token, salt='fixture-confirm', max_age=172800)
    except SignatureExpired:
        abort(404)
    title = requested.team_name +" vs " + requesting.team_name
    return render_template('view_fixture.html', fixture_id=fixture.id, requested_id=requested.id, fixture=fixture, title=title, requested=requested, requesting=requesting)

@auth.route('/confirm/<fixture_id>')
def confirm (fixture_id):
    fixture=Fixture.query.filter_by(id=fixture_id).first()
    confirmation = fixture.confirmed + 1
    heading = 'Confirmed'
    team = Team.query.filter_by(team_name=fixture.requester).first()
    recepient = team.user.email

    fixture.confirmed = confirmation
    db.session.commit()

    request_status("ATHLETIQ: Fixture status", "email/fixture_status", recepient, fixture=fixture, heading=heading,team=team)
    return redirect(url_for('main.index'))

@auth.route('/decline/<fixture_id>')
def decline (fixture_id):
    fixture=Fixture.query.filter_by(id=fixture_id).first()
    declined = fixture.declined + 1
    heading = 'Declined'
    team = Team.query.filter_by(team_name=fixture.requester).first()
    recepient = team.user.email

    fixture.declined = declined
    db.session.commit()
    request_status("ATHLETIQ: Fixture status", "email/fixture_status", recepient, fixture=fixture, heading=heading,team=team)
    return redirect(url_for('main.index'))

    