from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class CreateCategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])


class CreateProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    price = StringField('Price', validators=[DataRequired()])
    weight = StringField('Weight', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    refundable = StringField('Refundable [1|0]', validators=[DataRequired()])
    category_id = StringField('Category ID', validators=[DataRequired()])
    image = StringField('image', validators=[DataRequired()])
