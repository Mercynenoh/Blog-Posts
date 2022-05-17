from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,SubmitField, SelectField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):

    category = StringField(' Blog Title',validators=[DataRequired()])
    pitch = TextAreaField('Blog Content',validators=[DataRequired()])
    link = StringField(' Add link',validators=[DataRequired()])
    submit = SubmitField('Post')

class CommentForm(FlaskForm):
    text = TextAreaField('Text',validators=[DataRequired()])
    submit = SubmitField('Post')

class UpdateProfile(FlaskForm):
    bio = TextAreaField('Tell us about you.',validators = [DataRequired()])
    submit = SubmitField('Submit')
