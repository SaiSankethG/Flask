from flask import Flask, render_template

app = Flask(__name__)

@app.route("/<name>")
def home(name):
    return render_template("index.html", content="This is passed to template as a parameter")

if(__name__) == "___main__":
    app.run(debug=True)