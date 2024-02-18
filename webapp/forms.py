from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, FloatField
from wtforms.validators import InputRequired, NumberRange


class DataForm(FlaskForm):
    pregnancies = FloatField('Pregnancies', validators=[InputRequired(), NumberRange(min=0)])
    glucose = FloatField('Glucose', validators=[InputRequired(), NumberRange(min=0)])
    blood_pressure = FloatField('Blood Pressure', validators=[InputRequired(), NumberRange(min=0)])
    skin_thickness = FloatField('Skin Thickness', validators=[InputRequired(), NumberRange(min=0)])
    insulin = FloatField('Insulin', validators=[InputRequired(), NumberRange(min=0)])
    bmi = FloatField('BMI', validators=[InputRequired(), NumberRange(min=0)])
    diabetes_pedigree_function = FloatField('Diabetes Pedigree Function', validators=[InputRequired(), NumberRange(min=0)])
    age = FloatField('Age', validators=[InputRequired(), NumberRange(min=0)])
    outcome = IntegerField('Outcome', validators=[InputRequired(), NumberRange(min=0, max=1)])
    submit = SubmitField('Submit')
