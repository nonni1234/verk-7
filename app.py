import os
import pymysql.cursors
from flask import Flask, render_template as template, session, url_for, request, redirect
app = Flask(__name__)
app.secret_key = os.urandom(16)
print(app.secret_key)
# Sql stuff

connection = pymysql.connect(
    host='tsuts.tskoli.is',
    user='1809022520',
    password='mypassword',
    db='1809022520_verk7',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor)

sql = "SELECT * FROM USERS;"
with connection.cursor() as cursor:
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
@app.route("/")
def home():
    if "logged_in" in session:
        if session["logged_in"]:
            return template("admin.html", log = session["logged_in"])
    else:
        return template("index.html")

@app.route("/submit", methods=["GET","POST"])
def submit():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        session["name"] = name
        session["email"] = email
        session["logged_in"] = True
        with connection.cursor() as cursor:
            sql = f"INSERT INTO users values('{name}','{email}','{password}');"
            cursor.execute(sql)
            connection.commit()
            connection.close()
        return template("result.html", name=name, email=email,password=password)
    return "error"

@app.route("/login")
def loginsite():
    return "login"

@app.route("/signup")
def signupsite():
    return template("signup.html")

@app.errorhandler(404)
def pagenotfound(error):
    return template("404.html"), 404

if __name__ == '__main__':
    #app.run()
    app.run(debug=True, use_reloader=True)