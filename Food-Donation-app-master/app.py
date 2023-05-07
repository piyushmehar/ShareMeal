from flask import Flask, jsonify, request, render_template, session, redirect, url_for
import sqlite3
"""import flask_mail
from flask_mail import Mail, Message"""

app = Flask(__name__)
app.secret_key = ('FLASK_SECRET_KEY')


@app.route("/db")
def test_db():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS Users')
    conn.commit()
    conn.execute(
        'CREATE TABLE Users (uid INTEGER PRIMARY KEY, name TEXT, email TEXT,  password TEXT, gender TEXT, address TEXT,  mobilenumber TEXT)')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"


@app.route("/showchart")
def testihn_db():
    xarray = [
        "Africa",
        "Asia",
        "Europe",
        "Latin America",
        "North America",
    ]
    yarray = [2478, 5267, 734, 784, 433]
    return render_template('chart.html', xdata=xarray, ydata=yarray)


@app.route("/dbuser")
def tester_db():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS Users')
    conn.commit()
    conn.execute(
        'CREATE TABLE Users (uid INTEGER PRIMARY KEY ,name TEXT,email TEXT, password TEXT,gender TEXT,address TEXT,mobilenumber TEXT)')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"


@app.route("/dbrequests")
def tester1_db():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS Requests')
    conn.commit()
    conn.execute(
        'CREATE TABLE Requests (requestid INTEGER PRIMARY KEY ,name TEXT,quantity TEXT, location TEXT,contact TEXT,uid TEXT,donorid TEXT,status TEXT, FOREIGN KEY(uid) REFERENCES Users(uid))')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"


@app.route("/dbdonations")
def tester2_db():
    conn = sqlite3.connect('database.db')
    print('Opened database successfully', flush=True)
    conn.execute('DROP TABLE IF EXISTS Donations')
    conn.commit()
    conn.execute(
        'CREATE TABLE Donations (donationid INTEGER PRIMARY KEY ,name TEXT,quantity TEXT, location TEXT,contact TEXT,uid TEXT,requestorid TEXT,status TEXT, FOREIGN KEY(uid) REFERENCES Users(uid))')
    print('Table created successfully', flush=True)
    conn.close()
    return "Table created successfully"


@app.route("/")
def homeiu():
    session['uid'] = 1
    msgger = 0
    msg = ''
    return render_template('Index.html', msg=msg, msgger=msgger)


@app.route("/Mission")
def mission():
    return render_template("Mission.html")


@app.route("/Home")
def homey():
    msgger = 0
    msg = ''
    return render_template("Index.html", msg=msg, msgger=msgger)


@app.route("/Contact")
def contact():
    return render_template("Contact.html")


@app.route("/AboutUs")
def aboutus():
    return render_template("AboutUs.html")


@app.route('/acceptRequest', methods=['POST'])
def ajaxrequest():
    data = request.get_json()
    reqid = int(data['id'])
    result = {'result': 'fail'}
    if request.method == 'POST':
        con = sqlite3.connect('database.db')
        try:
            with sqlite3.connect("database.db") as con:
                uid = int(session['uid'])
                cur = con.cursor()
                cur.execute(
                    "UPDATE Requests SET donorid =(?), status = (?) WHERE requestid = (?)", (uid, 'closed', reqid))
                con.commit()
                msg = "Record successfully added"
                result = {'result': 'pass'}
                return jsonify(result)
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
        return jsonify(result)


@app.route('/Logintest', methods=['POST'])
def ajaxloginrequest():
    
    data = request.get_json()
    uname = data['uname']
    pwd = data['pwd']

    result = {'result': 'fail'}
    if request.method == 'POST':
        con = sqlite3.connect('database.db')
        try:
            with sqlite3.connect("database.db") as con:
                uid = int(session['uid'])
                cur = con.cursor()
                cur.execute(
                    "select * from Users WHERE name = (?) and password = (?)", (uname, pwd))
                user = cur.fetchall()
                con.commit()
                if len(user) > 0:
                    result = {'result': 'pass'}
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
        return jsonify(result)


@app.route('/acceptDonation', methods=['POST'])
def ajaxdonate():
    data = request.get_json()
    reqid = int(data['id'])
    result = {'result': 'fail'}
    if request.method == 'POST':
        con = sqlite3.connect('database.db')
        try:
            with sqlite3.connect("database.db") as con:
                uid = int(session['uid'])
                cur = con.cursor()
                cur.execute(
                    "UPDATE Donations SET requestorid =(?), status = (?) WHERE donationid = (?)", (uid, 'closed', reqid))
                con.commit()
                msg = "Record successfully added"
                result = {'result': 'pass'}
                return jsonify(result)
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
        return jsonify(result)


@app.route("/Requestlist")
def Requestlist():
    if request.method == 'GET':
        con = sqlite3.connect('database.db')
        try:
            with sqlite3.connect("database.db") as con:
                uid = int(session['uid'])
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM Requests where donorid IS NULL and uid!=(?)", (str(uid)))
                con.commit()
                requestlist = cur.fetchall()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
        return render_template('Request.html', requestlist=requestlist)


@app.route("/Donationlist")
def Donationlist():
    if request.method == 'GET':
        con = sqlite3.connect('database.db')
        try:
            with sqlite3.connect("database.db") as con:
                uid = int(session['uid'])
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM Donations where requestorid IS NULL and uid!=(?)", str(uid))
                con.commit()
                donationlist = cur.fetchall()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
        return render_template('Donation.html', donationlist=donationlist)


@app.route("/login", methods=['POST', 'GET'])
def login():
   
    msgger = 0
    msg = ''
    if request.method == 'POST':
        
        con = sqlite3.connect('database.db')
        user = ''
        try:
            email = request.form['email']
            password = request.form['password']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "SELECT * from Users WHERE email=(?) and password =(?)", (email, password))
                user = cur.fetchall()

            con.commit()
            if len(user) > 0:
                session['uid'] = user[0][0]
                return redirect(url_for('Dashboard'))
            else:
                msg = 'Invalid Credentials'
                return render_template("Index.html", msg=msg, msgger=msgger)
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
    return render_template("Index.html", msg=msg, msgger=msgger)


@app.route("/Signup")
def Signup():
    return render_template('Signup.html')


@app.route("/Register")
def Register():
    return render_template('Registration.html')


@app.route("/Dashboard", methods=['POST', 'GET'])
def Dashboard():

    if request.method == 'GET':
        
        con = sqlite3.connect('database.db')
        try:
            with sqlite3.connect("database.db") as con:
                uid = int(session['uid'])
                cur = con.cursor()
                cur.execute(
                    "SELECT * FROM Requests where uid =(?)", str(uid))
                con.commit()
                requestlist = cur.fetchall()
                cur.execute(
                    "SELECT * FROM Requests where donorid =(?)", str(uid))
                con.commit()
                acceptedrequestlist = cur.fetchall()

                cur.execute(
                    "SELECT * FROM Donations where uid =(?)", str(uid))
                con.commit()
                donationlist = cur.fetchall()
                cur.execute(
                    "SELECT * FROM Donations where requestorid =(?)", str(uid))
                con.commit()
                accepteddonationlist = cur.fetchall()

                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
    return render_template('Landing.html', requestlist=requestlist, donationlist=donationlist, accepteddonationlist=accepteddonationlist, acceptedrequestlist=acceptedrequestlist)


@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    con = sqlite3.connect('database.db')
    if request.method == 'POST':
        try:
            nm = request.form['username']
            addr = request.form['addr']
            city = request.form['email']
            zip = request.form['password']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Users (username,addr,          email,password)VALUES(?,?,?,?)", (nm, addr, city, zip))

            con.commit()
            msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
    return render_template("result.html", msg=msg)


@app.route('/createUser', methods=['POST', 'GET'])
def createUser():
    
    con = sqlite3.connect('database.db')
    msg = 'start'
    msgger = 0
    if request.method == "POST":
        try:
            
            name = request.form['name']
            # addr = request.form['addr']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            address = request.form['address']
            mobilenumber = request.form['mobilenumber']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Users (name, email, password, gender,address,mobilenumber)VALUES(?,?,?,?,?,?)", (name, email, password, gender, address, mobilenumber))
            con.commit()
            msgger = 1
            msg = "Account created successfully!"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
    return render_template("Index.html", msg=msg, msgger=msgger)


@app.route('/createRequest', methods=['POST', 'GET'])
def createRequest():

    if request.method == "GET":
        return render_template('RequestForm.html')

    if request.method == "POST":
        con = sqlite3.connect('database.db')
        msg = 'start'
        try:
            name = request.form['name']
            quantity = request.form['quantity']
            location = request.form['location']
            contact = request.form['contact']
            uid = session['uid']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Requests (name,quantity,location,contact,uid,status)VALUES(?,?,?,?,?,?)", (name, quantity, location, contact, uid, 'open'))
            con.commit()
            msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
    return redirect(url_for('Dashboard'))


@app.route('/createDonation', methods=['POST', 'GET'])
def createDonation():
    if request.method == "GET":
        return render_template('DonationForm.html')

    if request.method == "POST":
        con = sqlite3.connect('database.db')
        msg = 'start'
        try:
            name = request.form['name']
            quantity = request.form['quantity']
            location = request.form['location']
            contact = request.form['contact']
            uid = session['uid']
            with sqlite3.connect("database.db") as con:
                cur = con.cursor()
                cur.execute(
                    "INSERT INTO Donations (name,quantity,location,contact,uid,status)VALUES(?,?,?,?,?,?)", (name, quantity, location, contact, uid, 'open'))
            con.commit()
            msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = str(e)
        finally:
            con.close()
    return redirect(url_for('Dashboard'))


@app.route('/list')
def list():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Users")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


@app.route('/request')
def requesti():
    con = sqlite3.connect("database.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Users")
    rows = cur.fetchall()
    return render_template("list.html", rows=rows)

if __name__ == "__main__":
    app.run(debug=True)
