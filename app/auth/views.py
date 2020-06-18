from flask import render_template,redirect,url_for, flash,request
from . import auth
from ..models import User, Team, Fixture
from .. import db
from flask_login import login_user,logout_user,login_required
from .forms import LoginForm,RegistrationForm, FixtureForm
from ..email import mail_message


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
    team = Team.query.filter_by(id=team_id).first()
    address = team.user.email
    print(address)
    if fixture_form.validate_on_submit():
        '''
        view page that retunrs fixture page with its data
        '''

        fixture= Fixture(date=fixture_form.Date.data,time=fixture_form.Time.data,location=fixture_form.Location.data)
        db.session.add(fixture)
        db.session.commit()


        
        mail_message("Welcome to Sports","email/book_fixture",address,fixture=fixture)

        
        return redirect(url_for('auth.book_fixture', title=title, team_id=team_id))


    return render_template('fixture.html', title=title, fixture_form=fixture_form)