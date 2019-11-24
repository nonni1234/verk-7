import os
import pymysql.cursors
from flask import Flask, render_template as template, session, url_for, request, redirect
app = Flask(__name__)
app.secret_key = os.urandom(16)
print(app.secret_key)
# Sql stuff
try:
    connection = pymysql.connect(
        host='tsuts.tskoli.is',
        user='1809022520',
        password='mypassword',
        db='1809022520_verk7',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor)
except pymysql.OperationalError:
    print("Connection Failed")
    quit()

sql = "SELECT * FROM USERS;"
with connection.cursor() as cursor:
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)
@app.route("/")
def home():
    if "logged_in" in session and session["logged_in"] == True: 
        return redirect(url_for("admin"))
    else:
        return template("index.html")

@app.route("/admin")
def admin():
    if "logged_in" in session and session["logged_in"] != True:
        return template("index.html")
    else:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            results = cursor.fetchall()
            nafn = session.get("nafn")
            print(results)
            print(nafn)
            return template("admin.html", results = results, nafn=nafn)

@app.route("/login", methods=["GET","POST"])
def loginsite():
    if "logged_in" in session and session["logged_in"] == True:
        redirect("/")
    if request.method == "POST":
        if "logged_in" in session and session["logged_in"]:
            return "þú ert logged in núþegar!"
        else:
            if request.method == "POST":
                name = request.form["name"]
                password = request.form["password"]
                sql = f"SELECT * FROM users WHERE user_name = '{name}' AND user_password = '{password}'"
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(sql)
                        results = cursor.fetchone()
                        if results == None:
                            return "rangt lykilorð eða notendanafn"
                        else:
                            session["logged_in"] = True
                            session["nafn"] = results["user_name"]
                            return redirect(url_for("home"))
                except pymysql.OperationalError:
                    return "Database tenging ekki náð" # Þetta lætur þig vita ef eitthvað er að tengingunni
        
    else:
        return template("login.html")

@app.route("/signup", methods=["POST","GET"])
def signupsite():
    if "logged_in" in session and session["logged_in"] == True:
        return redirect("/")
    elif request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]
        session["logged_in"] = True
        with connection.cursor() as cursor:
            sql = f"INSERT INTO users values('{name}','{email}','{password}');"
            try:
                cursor.execute(sql)
                connection.commit()
            except pymysql.IntegrityError:
                return "Þetta notendanafn og/eða email er núþegar skráð"
        return template("result.html", name=name, email=email,password=password)
    else:
        return template("signup.html")

@app.route("/signout")
def signout():
    if "logged_in" in session:
        session["logged_in"] = False
        return redirect("/")
    else:
        return "Eitthvað fór úrskeiðis"
@app.errorhandler(404)
def pagenotfound(error):
    return template("404.html"), 404

if __name__ == '__main__':
    #app.run()
    app.run(debug=True, use_reloader=True)