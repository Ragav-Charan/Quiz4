import os

import pyodbc as pyodbc
from flask import Flask, render_template, request

app = Flask(__name__)
port = int(os.getenv('VCAP_APP_PORT','5000'))
myHostname = "flyingjaguar.redis.cache.windows.net"
myPassword = "3azkQQEBo5hhkEhjS7GrD+RF8AmdpJtsjWst5KxqEYY="
server = 'charan.database.windows.net'
database = 'MyDB'
username = 'charan123'
password = 'Smokescreen@5'
driver= '{ODBC Driver 17 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)

@app.route('/')
def home():
    cur = cnxn.cursor()
    cur.execute("select StateName from voting WHERE TotalPop between 2000 and 8000")
    get1 = cur.fetchall()
    l1=[]
    l2=[]
    for row1 in get1:
        l1.append(row1[0])
    cur.execute("select StateName from voting WHERE TotalPop between 8000 and 40000")
    get2 = cur.fetchall()
    for  row2 in get2:
        l2.append(row2[0])
    return render_template("home.html", q1 = l1,q2 = l2)

@app.route('/records')
def records():
    return render_template('records.html')

@app.route('/options', methods=['POST', 'GET'])
def options():
    p1 = int(request.form['p1']) * 1000
    p2 = int(request.form['p2']) * 1000
    rows = []
    get = []
    c = []
    points = []
    style = {'role':'style'}
    annotation = {'role':'annotation'}
    points.append(['TotalPop','Registered'])
    cur = cnxn.cursor()
    cur.execute("select TotalPop,Registered from voting WHERE TotalPop between ? and ?",(p1,p2))
    get = cur.fetchall();
    rows.append(get)
    for row in get:
        points.append([row[0],row[1]])
    return render_template("list.html", p=points)

@app.route('/records1')
def records1():
    return render_template('records1.html')

@app.route('/options1', methods=['POST', 'GET'])
def options1():
    p = int(request.form['p']) * 1000
    rows = []
    get = []
    c = []
    points = []
    points.append(['Total Population','State Count'])
    cur = cnxn.cursor()
    cur.execute("select max(TotalPop) from voting")
    maxPop = cur.fetchone();
    print (maxPop)
    i = 0
    while(i < maxPop[0] ):
        cur.execute("select count(StateName) from voting WHERE TotalPop between ? and ?",(i,i+(p)))
        get = cur.fetchone();
        key = str(i)+"-"+str(i+(p))
        points.append([key, get[0]])
        i = i+(p)
        print(points)
    return render_template("list1.html", p=points)


if __name__ == '__main__':
    app.run()
