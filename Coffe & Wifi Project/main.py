from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,URLField,TimeField,SelectField
from wtforms.validators import DataRequired, URL
import csv
import os
from dotenv import load_dotenv
'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''
load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location_url = URLField('Location URL/Google Maps', validators=[DataRequired(), URL()])
    opening= StringField('Opening Time', validators=[DataRequired()])
    closing= StringField('Closing Time', validators=[DataRequired()])
    coffe= SelectField('Coffe Rating',choices=[('✘','✘'),('☕','☕'),('☕☕','☕☕'),('☕☕☕','☕☕☕'),('☕☕☕☕','☕☕☕☕'),('☕☕☕☕☕','☕☕☕☕☕')])
    wifi=SelectField('Wifi Rating',choices=[('✘','✘'),('🔌','🔌'),('🔌🔌','🔌🔌'),('🔌🔌🔌','🔌🔌🔌'),('🔌🔌🔌🔌','🔌🔌🔌🔌'),('🔌🔌🔌🔌🔌','🔌🔌🔌🔌🔌')])
    power= SelectField('power outlet rating',choices=[('✘','✘'),('💪','💪'),('💪💪','💪💪'),('💪💪💪','💪💪💪'),('💪💪💪💪','💪💪💪💪'),('💪💪💪💪💪','💪💪💪💪💪')])
    submit = SubmitField('Submit')


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add',methods=['GET','POST'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv','a', encoding='utf-8',newline='') as file:
            writer=csv.writer(file)
            row=[form.cafe.data,form.location_url.data,form.opening.data,form.closing.data,form.coffe.data,form.wifi.data,form.power.data]
            writer.writerow(row)
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = [row for row in csv_data]
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
