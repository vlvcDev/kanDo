from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, StringField, PasswordField, TextAreaField, DateField, SubmitField, validators, SelectField, IntegerField, FormField, FieldList
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class SignInForm(FlaskForm):
    id = StringField('Id', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Confirm')

class ItemForm(FlaskForm):
    product = SelectField('Product', coerce=int)
    quantity = IntegerField('Quantity', default=0)

class OrderForm(FlaskForm):
    items = FieldList(FormField(ItemForm), min_entries=1)

class ProductForm(FlaskForm):
    code = StringField('Product Code')
    price = FloatField('Price')
    type = SelectField('Type', choices=[('Window', 'Window'), ('Door', 'Door')])
    description = TextAreaField('Description')
    available = BooleanField('Available')
    submit = SubmitField('Add Product')