#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from database_setup import session as database_session, Catagory, Items
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

app = Flask("__main__")
app.debug = True
app.secret_key = "RyanIsSoHandsome"


@app.route("/")
@app.route("/index")
def indexDisplay():
    catagory = database_session.query(Catagory).all()
    return render_template("index.html", catagory=catagory, itemShow=itemShow)


@app.route("catalog/items/<string: catagory>")
def indexDisplay(catagory):
    catagory = database_session.query(Catagory).all()
    itemShow = "hello"
    return render_template("index.html", catagory=catagory, itemShow=itemShow)


@app.route("/newCatagory", methods=["GET", "POST"])
def newCatagory():
    if request.method == "POST":
        newCataName = request.form["catagory"]
        try:
            item = database_session.query(
                Catagory).filter_by(name=newCataName).one()
            flash("Catagory \"%s\" has already existed!" % (newCataName,))
            return redirect("/newCatagory")
        except NoResultFound:
            newCata = Catagory(name=newCataName)
            try:
                database_session.add(newCata)
                database_session.commit()
                return redirect("/")
            except SQLAlchemyError:
                flash("Cannot commit the new item! Please contact developer!")
                return redirect("/newCatagory")
    else:
        return render_template("newCatagory.html")


@app.route("/item/<int: item_id>")
def viewItem(item_id):
    return render_template("viewItem.html")


@app.route("/item/<int: item_id>/edit", methods=["GET", "POST"])
def viewItem(item_id):
    if request.method == "POST":
        return render_template("itemForm.html")
    else:
        return render_template("itemForm.html")


@app.route("/item/<int: item_id>/delete", methods=["GET", "POST"])
def viewItem(item_id):
    if request.method == "POST":
        return render_template("delete.html")
    else:
        return render_template("delete.html")


@app.route("/item/new", methods=["GET", "POST"])
def newItem():
    if request.method == "POST":
        return render_template("itemForm.html")
    else:
        return render_template("itemForm.html")
