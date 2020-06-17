from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from datetime import datetime
from . import db
from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    password_secure = db.Column(db.String(255))
    team = db.relationship('Team',backref = 'user',lazy = "dynamic")

    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_secure = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_secure,password)

    def __repr__(self):
        return f'{self.email}'



class Team(db.Model):
    __tablename__ = 'teams'
    id = db.Column(db.Integer,primary_key = True)
    team_name=db.Column(db.String)
    category=db.Column(db.String)
    created_at = db.Column(db.DateTime,default=datetime.utcnow)    
    manager = db.Column(db.Integer,db.ForeignKey("users.id"))
    team_pic_path = db.Column(db.String) 
    wins = db.Column(db.Integer)
    draws= db.Column(db.Integer)
    losses=db.Column(db.Integer)
    player_team=db.relationship('Player',backref = 'player_team',lazy = "dynamic")
    

    def save_team(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.team_name}'


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer,primary_key = True)
    name=db.Column(db.String)
    playing_position=db.Column(db.String)       
    prof_pic_path = db.Column(db.String) 
    team = db.Column(db.Integer,db.ForeignKey("teams.id"))
    

    def save_player(self):
        db.session.add(self)
        db.session.commit()

    
    def __repr__(self):
        return f'{self.name}'