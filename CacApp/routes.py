from CacApp import fcp
from dotenv import load_dotenv
import os     
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_login import UserMixin
import requests
from CacApp.models import user

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
class Login(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        address = StringField('Username', validators=[DataRequired()])
        city = StringField('Username', validators=[DataRequired()])
        state = SelectField("State")
        submit = SubmitField('Sign In')


API_KEY = ''
API_KEY = os.getenv('api_key')        
url = f'https://www.googleapis.com/civicinfo/v2/representatives?key={API_KEY}'

def configure():
        load_dotenv()
        

@fcp.route('/')
def index():
        return "Hello World"

@fcp.route('/signup')
def signUp():
        form = Login
        if form.validate_on_submit():
                username = form.username
                password_hash = form.password
                address = form.address +", "
                city = form.city + ", "
                state = form.state
                params = {'address': address + city + state}
                response = requests.get(url, params=params)
                data = ""
                if response.status_code == 200:
                        data = response.json()
                else:
                        return("404 ERROR") 
                senators = [i for i in data["offices"][i]["officeIndices"] if data["offices"][i]["name"] == "U.S. Senator"]
                president = [i for i in data["offices"][i]["officeIndices"] if data["offices"][i]["name"] == "President of the United States"]
                vp = [i for i in data["offices"][i]["officeIndices"] if data["offices"][i]["name"] == "Vice President of the United States"]
                fed_rep = [i for i in data["offices"][i]["officeIndices"] if data["offices"][i]["name"] == "U.S. Representative"]
                governor = [i for i in data["offices"][i]["officeIndices"] if data["offices"][i]["name"] == "Governor of Florida"]

                senators_name=[]
                for i in senators:
                        senators_name[i]= data["officials"][i]["name"]
                president_name = data["officials"][president[0]]["name"]
                vp_name = data["officials"][vp[0]]["name"]
                fed_rep_name = data["officials"][fed_rep[0]]["name"]
                governor_name = data["officials"][governor[0]]["name"]
                


                
                
                

                
                
                        
                        
                
                        
        
