from flask import Flask
from flask import render_template
import csv


app = Flask(__name__)


class DataCovid :
    def __init__(self):
        self.data = {}
        self.rowlabel = []
        with open("time_series_covid19_deaths_global.csv.txt") as csvfile:
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

datacovid = DataCovid()

@app.route('/favicon.ico')
def favicon():
    return ""

@app.route('/')
def home():
    return render_template('map.html',data = datacovid, iddate = 4)    

@app.route('/<iddate>')
def withdate(iddate):
    return render_template('map.html',data = datacovid,iddate=iddate)    

if __name__ == '__main__':
    app.run(debug=True)