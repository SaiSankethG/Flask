from flask import Blueprint, render_template  

second = Blueprint("second", __name__, template_folder="templates")

@second.route("/home")
@second.route("/")
def home():
    return render_template("admin.html")