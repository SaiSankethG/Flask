from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from admin import second

app = Flask(__name__)
app.secret_key = "learning flask  "
app.permanent_session_lifetime = timedelta(days=10) 
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
app.register_blueprint(second, url_prefix="")

db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    
    def __init__(self, name, email):
        self.name = name
        self.email = email

is_admin = False

@app.route("/")
def home():
    return render_template("index.html" , content = ['hi', 'hello', 'a'] ) 

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["name"]
        session["user"] = user
        if len(session["user"]) == 0 and len(session["mail"]) == 0:
            return render_template("login.html")
        found_user = users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = users(user, "")
            db.session.add(usr)
            db.session.commit()
        flash("Login Successfull!")
        return redirect(url_for("user", name=user))
    else:
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("login.html")
    
@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

@app.route("/user", methods=["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]
        if request.method == "POST":
            email = request.form.get("email")
            session["email"] = email
            found_user = users.query.filter_by(name = user).first()
            found_user.email = email
            db.session.commit()
        else:
            if "email" in session:
                email = session.get("email")
        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login"))
    
@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("email", None)
    flash("Logout successfully!", "info") 
    return redirect(url_for("login"))

@app.route("/api/admin")
def admin_page():
    if is_admin:
        return "Hello admin!"
    else:
        return redirect(url_for("home"))

# @app.route("/template/<name>")
# def cTemplate(name):
#     return render_template("index.html" , content = ['hi', 'hello', 'a'] )

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)