from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField,ValidationError
from wtforms.validators import Required,Email,Length
import email_validator

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class TeamForm(FlaskForm):
    team_name = StringField('Team name',validators=[Required()])   
    location = StringField('Location',validators=[Required()])  
    category = SelectField('Category', validators=[Required()], choices=[('football','Football'),('hockey','Hockey'),('rugby','Rugby'),('cricket','Cricket'),('basketball','Basketball')])
    submit = SubmitField('Create team')

class PlayerForm(FlaskForm):
    name = StringField('Player\'s name',validators=[Required()])    
    position = StringField('Player\'s position',validators=[Required()])
    submit = SubmitField('Add player')
    
# class FixtureForm(FlaskForm):
#     Date = DateField('Fixture\'s Date',validators=[Required()], format='%d-%m-%Y')
#     Time = TimeField('Start Time',validators=[Required()], render_kw={"placeholder": "Format: 12.00"})    
#     Location = StringField('Game\'s Location',validators=[Required()], render_kw={"placeholder": "E.g: Nairobi"})
#     submit = SubmitField('Request Fixture')
    
