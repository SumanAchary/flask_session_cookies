from flask import Flask, redirect, url_for, render_template, request, session, make_response

from datetime import timedelta
import random
import copy

app = Flask(__name__)
app.secret_key = "^#@(#^@&"
app.permanent_session_lifetime = timedelta(minutes=1)


@app.route("/")
def home():
    number = random.randint(11111, 99999)
    return render_template("index.html", num=number)


@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        return redirect(url_for("user"))
    else:
        if "user" in session:
            return redirect(url_for("user"))

        return render_template("login.html")


@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("user_profile.html", name=user)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))


@app.route('/setCookie', methods=['POST', 'GET'])
def setcookie():
    user = 'Cookie not yet set'
    if request.method == "POST":
        user = request.form["name"]
    resp = make_response(render_template('cookie.html'))
    resp.set_cookie('userID', user)
    return resp


@app.route('/getcookie')
def getcookie():
    name = request.cookies.get('userID')
    my_name = copy.deepcopy(name)
    return render_template("getcookie.html", name = my_name)


if __name__ == "__main__":
    app.run(debug=True)
