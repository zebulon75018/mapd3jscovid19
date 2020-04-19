from flask import Flask
from flask import render_template
import csv


app = Flask(__name__)

departement = {}

with open("Departementfrancais.csv") as csvfile:
    reader = csv.reader(csvfile) # change contents to floats
    n = 0
    for row in reader: # each row is a list
        #print(row)
        if n!=0:
            try:
                #print(row[1])
                departement[int(row[1])] = row[5]
            except Exception as e:
                pass
        n= n + 1


covidFR = []

covidUSA = []

with open("usa04-15-2020.csv") as csvfile:
    reader = csv.reader(csvfile)
    n = 0 
    for row in reader: # each row is a list
        print(row[0])
        if n!=0:                        
                try:
                    covidUSA.append({"state": row[0], "visited": row[6]})                
                except Exception as e:
                    pass
        n= n + 1
 
with open("sursaud-covid19-quotidien-2020-04-16-10h47-departement.csv") as csvfile:
    reader = csv.reader(csvfile)
    n = 0 
    for row in reader: # each row is a list
        #print(row)
        if n!=0:            
            if row[2] == "0":
                try:
                    covidFR.append({"name": departement[int(row[0])], "population": row[4]})                
                except Exception as e:
                    pass
        n= n + 1

#print(covidFR)
#print(departement)


class DataCovid :
    def __init__(self, filename):
        self.data = {}
        self.rowlabel = []
        with open(filename) as csvfile:
            reader = csv.reader(csvfile) # change contents to floats
            n = 0
            for row in reader: # each row is a list
                if n!=0:
                    self.data[n] = row
                else:
                    self.rowlabel  = row
                n= n + 1
    
    def getNbRow(self):
        return self.data.keys()

    def getLabel(self):
        return self.rowlabel

    def getDate(self):
        return self.rowlabel[4:]

    def getName(self,n):
        return "%s %s" % ( self.data[n][0] , self.data[n][1] )

    def getLat(self,n):
        return self.data[n][2]

    def getLong(self,n):
        return self.data[n][3]

    def getData(self,row,column):
        print(" getData %s %s " % ( row , column ) )
        return self.data[int(row)][int(column)+3]

datacovid = DataCovid("time_series_covid19_deaths_global.csv.txt")

@app.route('/favicon.ico')
def favicon():
    return ""
@app.route('/usa/')
def usa():
    return render_template('usa.html',covid=covidUSA)    

@app.route('/france/')
def france():
    return render_template('france.html',covidFR=covidFR)    
@app.route('/')
def home():
    return render_template('map.html',data = datacovid, iddate = 4)    

@app.route('/<iddate>')
def withdate(iddate):
    return render_template('map.html',data = datacovid,iddate=iddate)    

if __name__ == '__main__':
    app.run(debug=True)