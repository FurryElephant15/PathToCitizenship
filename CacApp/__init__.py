from flask import Flask, render_template, request,session, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, login_user, login_required
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os     
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired
from flask_login import UserMixin, logout_user
import requests
import pandas as pd
import random
from CacApp.serve_questions import serveQuestions as sq
import json
from sqlalchemy.ext.mutable import MutableList
from datetime import datetime

fcp = Flask(__name__)
db = SQLAlchemy()
fcp.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
fcp.config['SECRET_KEY'] = 'password'


db.init_app(fcp)
migrate = Migrate(fcp, db)
login = LoginManager(fcp)
if __name__ == "__main__":      
    fcp.run()



class user(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True, autoincrement=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(128), index = True, unique = True)
    passwords: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    house: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    senator1: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    senator2: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    president: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    vp: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    governor: so.Mapped[str] = so.mapped_column(sa.String(128), index = True)
    state: so.Mapped[str] = so.mapped_column(sa.String(128), index = True, nullable = True)
    questionsAnswered: so.Mapped[int] = so.mapped_column(sa.Integer(),default = 0, index = True)
    correct: so.Mapped[int] = so.mapped_column(sa.Integer(), default = 0, index = True)
    wrong: so.Mapped[int] = so.mapped_column(sa.Integer(), default = 0, index = True)
    weights: so.Mapped[int] = so.mapped_column(sa.Text, index = True, default = json.dumps([10 for _ in range(108)]))
    responses: so.Mapped[list] = so.mapped_column(MutableList.as_mutable(sa.JSON), default=[])
    
    def password_create(self, password):
        self.passwords=generate_password_hash(password)
    def password_check(self, password):
        return check_password_hash(self.passwords, password)
    def __repr__(self):
            return f"<User {self.username}: House={self.house}, Senator1={self.senator1}, Senator2={self.senator2}, President={self.president}, VP={self.vp}, Governor={self.governor}>"


@login.user_loader
def load_user(id):
    return db.session.get(user, int(id))



class Signup(FlaskForm):
        states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        address = StringField('Address (Omit City and State)', validators=[DataRequired()])
        city = StringField('City', validators=[DataRequired()])
        state = SelectField("State", choices = states, validators=[DataRequired()])
        submit = SubmitField('Sign In')
class Login(FlaskForm):
        username = StringField('Username', validators=[DataRequired()])
        password = PasswordField('Password', validators=[DataRequired()])
        submit = SubmitField('Sign In')        


class question(FlaskForm):
        def __init__(self, answer1, answer2, answer3, answer4):
                self.answer1 = answer1
                self.answer2 = answer2
                self.answer3 = answer3
                self.answer4 = answer4
                answer = RadioField(choices=[self.answer1, self.answer2, self.answer3, self.answer4])
                submit = SubmitField('Submit Answer')        

        

API_KEY = 'AIzaSyCqhXWHJIYr7H1gpbvQw17EPrv9svHJTuw'
#API_KEY = os.getenv('api_key')        
url = f'https://www.googleapis.com/civicinfo/v2/representatives?key={API_KEY}'

def configure():
        load_dotenv()
        

@fcp.route('/')
@fcp.route('/home')
def index():
        return render_template("home.html")

@fcp.route('/logout')
def signup():
        logout_user()
        return redirect("/")

@fcp.route('/signup', methods =['GET', 'POST'])
def signUp():
        form = Signup()
        if form.validate_on_submit():
                username = form.username.data
                address = form.address.data +", "
                city = form.city.data + ", "
                state = form.state.data
                params = {'address': address + city + state}
                response = requests.get(url, params=params)
                data = ""
                if response.status_code == 200:
                        data = response.json()
                else:
                        return("404 ERROR") 
                senators = [i for i, office in enumerate(data["offices"]) if office["name"] == "U.S. Senator"]
                president = [i for i, office in enumerate(data["offices"]) if office["name"] == "President of the United States"]
                vp = [i for i, office in enumerate(data["offices"]) if office["name"] == "Vice President of the United States"]
                fed_rep = [i for i, office in enumerate(data["offices"]) if office["name"] == "U.S. Representative"]
                governor = [i for i, office in enumerate(data["offices"]) if office["name"] == f"Governor of {state}"]

                senators_name=[data["officials"][official_index]["name"] for index in senators for official_index in data["offices"][index]["officialIndices"]]

                president_name = data["officials"][president[0]]["name"]
                vp_name = data["officials"][vp[0]]["name"]
                fed_rep_name = data["officials"][fed_rep[0]+1]["name"]
                governor_name = data["officials"][governor[0]+1]["name"]
                addUser = user(
                        username=username,
                        house=fed_rep_name,
                        senator1=senators_name[0],
                        senator2=senators_name[1],
                        president=president_name,
                        vp=vp_name,
                        governor = governor_name,
                        state = form.state.data
                        )
                addUser.password_create(form.password.data)

                db.session.add(addUser)
                db.session.commit()
        return render_template("signup.html", form = form)

@fcp.route('/login', methods=['GET', 'POST'])
def logIn():
    form = Login()
    if form.validate_on_submit():
        user_instance = db.session.scalar(sa.select(user).where(user.username == form.username.data))
        if user_instance is None:
            return "User does not exist"
        if not user_instance.password_check(form.password.data):
            return "Password is incorrect"
        login_user(user_instance)
        return(redirect('/'))
    return render_template("login.html", form = form)




 
@fcp.route('/question', methods = ['GET', 'POST'])
@login_required
def renderQuestion():
        theUser = user.query.get(current_user.id)
        instance = sq(theUser.questionsAnswered, theUser.correct, theUser.wrong, theUser.weights, theUser.senator1, theUser.senator2, theUser.governor, theUser.state, theUser.house, theUser.president, theUser.vp) 

        questionIndex,questionToRender, correct, w1, w2, w3 = instance.deployQ()
        session['questionIndex'] = questionIndex
        randomNumber = random.randint(0,3)
        session['randomNumber'] = randomNumber
        if randomNumber == 0:
                        return render_template('renderQuestion.html', question=questionToRender, choice1=correct, choice2 = w1, choice3=w2, choice4=w3)
        elif randomNumber == 1:
                        return render_template('renderQuestion.html', question=questionToRender, choice1=w1, choice2 = correct, choice3=w2, choice4=w3)
        elif randomNumber == 2:
                        return render_template('renderQuestion.html', question=questionToRender, choice1=w1, choice2 = w2, choice3=correct, choice4=w3)
        elif randomNumber == 3:
                        return render_template('renderQuestion.html', question=questionToRender, choice1=w1, choice2 = w2, choice3=w3, choice4=correct)
                
def incWeight(questionIndex, weights, theUser):  
        weights = json.loads(weights)
        weights[questionIndex] += 5
        theUser.weights = json.dumps(weights)
        db.session.commit()  

        return weights
        
def decWeight(questionIndex,weights, theUser):
        weights = json.loads(weights)
        weights[questionIndex] -= 2
        if weights[questionIndex] < 1:
            weights[questionIndex] = 2
        theUser.weights = json.dumps(weights)
        db.session.commit()
        return weights



@fcp.route('/checkAnswer', methods =['GET'])
def checkAnswer():
        user_instance = db.session.get(user, current_user.id)
                                          
        answer = request.args.get("theAnswer")
        chosen = request.args.get("theResponse")

        randomNumber=session.get('randomNumber')
        questionIndex = session.get('questionIndex')
        weights = user_instance.weights
        questionIndexNo = questionIndex
        if randomNumber == 0:
                if answer=="answer1":
                        
                        weights = decWeight(questionIndexNo, weights,user_instance)
                        listToUpload = {"result": "correct", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()
                        return {"result": "correct", "randomNumber": randomNumber}

                else:
                        weights = incWeight(questionIndexNo,weights,user_instance)
                        listToUpload = {"result": "wrong", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()


                        return {"result": "incorrect", "randomNumber": randomNumber}
        if randomNumber == 1:
                if answer=="answer2":
                        
                        weights = decWeight(questionIndexNo,weights,user_instance)
                        listToUpload = {"result": "correct", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()

                        return {"result": "correct", "randomNumber": randomNumber}

                else:
                        listToUpload = {"result": "wrong", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()
                        weights = incWeight(questionIndexNo,weights,user_instance)


                        return {"result": "incorrect", "randomNumber": randomNumber}
        if randomNumber == 2:
                if answer=="answer3":
                        listToUpload = {"result": "correct", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()
                        weights = decWeight(questionIndexNo,weights,user_instance)

                        return {"result": "correct", "randomNumber": randomNumber}
 
                else:
                        listToUpload = {"result": "wrong", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()
                        weights = incWeight(questionIndexNo,weights,user_instance)


                        return {"result": "incorrect", "randomNumber": randomNumber}      
        if randomNumber == 3:
                if answer=="answer4":
                        listToUpload = {"result": "correct", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()
                        weights = decWeight(questionIndexNo,weights,user_instance)


                        return {"result": "correct", "randomNumber": randomNumber}

                else:
                        listToUpload = {"result": "wrong", "questionIndexNo": questionIndexNo, "dateAndTime": datetime.today().date().isoformat(), "answerChosen": chosen}
                        user_instance.responses.append(listToUpload)
                        db.session.commit()
                        weights = incWeight(questionIndexNo,weights,user_instance)
                        return {"result": "incorrect", "randomNumber": randomNumber}
       
@fcp.route('/results')
def results():
        user_instance = db.session.get(user, current_user.id)
        resultList = user_instance.responses
        instance = sq(user_instance.questionsAnswered, user_instance.correct, user_instance.wrong, user_instance.weights, user_instance.senator1, user_instance.senator2, user_instance.governor,user_instance.state, user_instance.house,user_instance.president,user_instance.vp)
        return render_template("renderResult.html", resultList= resultList, instance = instance)
@fcp.route('/result/<int:id>')
def renderQuestionResult(id):
        choice = request.args.get('choice') 

        theUser = user.query.get(current_user.id)
        instance = sq(theUser.questionsAnswered, theUser.correct, theUser.wrong, theUser.weights, theUser.senator1, theUser.senator2, theUser.governor,theUser.state, theUser.house, theUser.president, theUser.vp)
        q, c, w1_val, w2_val, w3_val = instance.deployDiscreteQ(id)
        
        return render_template("questionResult.html", q = q, c=c, w1_val=w1_val, w2_val=w2_val, w3_val=w3_val, choice = choice)                           
