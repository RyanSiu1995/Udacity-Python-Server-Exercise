#!/usr/bin/env python
from flask import Flask, render_template
from database_setup import session, Catagory, Items

app = Flask("__main__")
app.debug = True

@app.route("/")
@app.route("/index")
def indexDisplay():
    catagory = session.query(Catagory).all()
    return render_template("index.html", catagory=catagory)
