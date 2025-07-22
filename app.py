import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "myspace.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class yourspace(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=True)
    desc = db.Column(db.String(600), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.SrNo} {self.title}"

@app.route("/", methods= ["GET", "POST"])
def hello_world():
    if request.method == "POST":
        title = request.form['title']
        desc = request.form['desc']
        space = yourspace(title = title, desc = desc)
        db.session.add(space)
        db.session.commit()
    space = yourspace.query.all()    
    return render_template('index.html', space=space)

@app.route("/update/<int:SrNo>", methods= ["GET", "POST"])
def update(SrNo):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        space = yourspace.query.filter_by(SrNo=SrNo).first()
        space.title=title
        space.desc=desc
        db.session.add(space)
        db.session.commit()
        return redirect("/")
    space = yourspace.query.filter_by(SrNo=SrNo).first()
    return render_template('update.html', yourspace=space)
    


@app.route("/delete/<int:SrNo>")
def delete(SrNo):
    space = yourspace.query.filter_by(SrNo=SrNo).first()
    if yourspace:
        db.session.delete(space)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tables created!")
    app.run(debug=True)