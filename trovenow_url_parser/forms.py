from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class TroveForm(FlaskForm):
    url = StringField('Enter full URL here', validators=[DataRequired()])
    submit = SubmitField('Submit')