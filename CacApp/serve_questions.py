import pandas
import random
import json
stateCapitals={
    "Alabama": "Montgomery",
    "Alaska": "Juneau",
    "Arizona": "Phoenix",
    "Arkansas": "Little Rock",
    "California": "Sacramento",
    "Colorado": "Denver",
    "Connecticut": "Hartford",
    "Delaware": "Dover",
    "Florida": "Tallahassee",
    "Georgia": "Atlanta",
    "Hawaii": "Honolulu",
    "Idaho": "Boise",
    "Illinois": "Springfield",
    "Indiana": "Indianapolis",
    "Iowa": "Des Moines",
    "Kansas": "Topeka",
    "Kentucky": "Frankfort",
    "Louisiana": "Baton Rouge",
    "Maine": "Augusta",
    "Maryland": "Annapolis",
    "Massachusetts": "Boston",
    "Michigan": "Lansing",
    "Minnesota": "Saint Paul",
    "Mississippi": "Jackson",
    "Missouri": "Jefferson City",
    "Montana": "Helena",
    "Nebraska": "Lincoln",
    "Nevada": "Carson City",
    "New Hampshire": "Concord",
    "New Jersey": "Trenton",
    "New Mexico": "Santa Fe",
    "New York": "Albany",
    "North Carolina": "Raleigh",
    "North Dakota": "Bismarck",
    "Ohio": "Columbus",
    "Oklahoma": "Oklahoma City",
    "Oregon": "Salem",
    "Pennsylvania": "Harrisburg",
    "Rhode Island": "Providence",
    "South Carolina": "Columbia",
    "South Dakota": "Pierre",
    "Tennessee": "Nashville",
    "Texas": "Austin",
    "Utah": "Salt Lake City",
    "Vermont": "Montpelier",
    "Virginia": "Richmond",
    "Washington": "Olympia",
    "West Virginia": "Charleston",
    "Wisconsin": "Madison",
    "Wyoming": "Cheyenne"
}








df = pandas.read_csv("CacApp/Question,Correct Answer,Wrong Answe.csv")
question = df['Question']
correct = df['Correct Answer']
w1 = df['Wrong Answer 1']
w2 = df['Wrong Answer 2']
w3 = df['Wrong Answer 3']
df.to_csv("output.csv", index=True)


class serveQuestions:
    speaker = "Mike Johnson"
    justice_number = 9
    chief_justice = "John Roberts"
    president_party = "Democrat"  
    def __init__(self,questionsAnswered, right, wrong, weights, sen1, sen2, governor,state, house, president, vp):
        self.questions = questionsAnswered
        self.right = right
        self.wrong = wrong
        self.weights = weights
        self.sen1 = sen1
        self.sen2 = sen2
        self.governor = governor
        self.state = state
        self.house = house
        self.president = president
        self.vp = vp
        
    def setWeights(self,weights):
        self.weights = weights 
    def getWeights(self):
        return self.weights
    def deployQ(self):    
        
        if not self.weights or len(self.weights) != len(question):
            self.weights = [10 for _ in range(len(question))]
        questionIndex = random.choices(range(len(question)), self.weights, k=1)

            
        q = question.at[questionIndex[0]] 
        c = correct.at[questionIndex[0]]
        w1_val = w1.at[questionIndex[0]]
        w2_val = w2.at[questionIndex[0]]
        w3_val = w3.at[questionIndex[0]]
        if questionIndex[0] == 62:
            c = self.governor
        if questionIndex[0] == 61:
            c = stateCapitals[self.state]
        if questionIndex[0] == 93:
            c = self.house
        if questionIndex[0] == 94:
            c = self.president
        if questionIndex[0] == 95:
            c= self.vp
        if questionIndex[0] == 97:
            c = self.president_party
        if questionIndex[0] == 63:
            c = self.speaker
    
            
        return questionIndex[0], q.strip(), c.strip(), w1_val.strip(), w2_val.strip(), w3_val.strip()

    def incWeight(self,questionIndex):
        self.weights[questionIndex] += 5
    def decWeight(self, questionIndex):
        self.weights[questionIndex] -= 2
        if self.weights[questionIndex] < 1:
            self.weights[questionIndex] = 2




            

          
  



    def deployDiscreteQ(self, questionIndex):
        q = question.at[questionIndex] 
        c = correct.at[questionIndex]
        w1_val = w1.at[questionIndex]
        w2_val = w2.at[questionIndex]
        w3_val = w3.at[questionIndex]
        if questionIndex == 62:
            c = self.governor
        if questionIndex == 61:
            c = stateCapitals[self.state]
        if questionIndex == 93:
            c = self.house
        if questionIndex == 94:
            c = self.president
        if questionIndex == 95:
            c= self.vp
        if questionIndex == 97:
            c = self.president_party
        if questionIndex == 63:
            c = self.speaker
        return q, c, w1_val, w2_val, w3_val
        
    def getCorrect(self, questionIndex):
        c = correct.at[questionIndex]
        if questionIndex == 60:
            c = self.governor
        if questionIndex == 61:
            c = stateCapitals[self.state]
        if questionIndex == 93:
            c = self.house
        if questionIndex == 94:
            c = self.president
        if questionIndex == 95:
            c= self.vp
        if questionIndex == 97:
            c = self.president_party
        if questionIndex == 63:
            c = self.speaker
        return c


    
    def endTask(self):
        return self.right, self.wrong
    def __str__(self):
        return print(self.weights)
        



        
        