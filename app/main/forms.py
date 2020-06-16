from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SelectField,SubmitField,ValidationError
from wtforms.validators import Required,Email,Length
import email_validator

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [Required()])
    submit = SubmitField('Submit')


class TeamForm(FlaskForm):
    team_name = StringField('Team name',validators=[Required()])    
    category = SelectField('Category', validators=[Required()], choices=[('football','Football'),('hockey','Hockey'),('rugby','Rugby'),('cricket','Cricket'),('basketball','Basketball')])
    submit = SubmitField('Create team')
    