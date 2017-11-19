#!/usr/bin/env python
from flask import Flask, render_template, request, redirect, jsonify, session
from flask import url_for, flash, get_flashed_messages, make_response
from database_setup import session as database_session, Catagory, Items
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import desc
import json
import httplib2
import random
import string

app = Flask("__main__")
app.debug = True
app.secret_key = "RyanIsSoHandsome"


@app.route("/")
@app.route("/index")
def indexDisplay():
    catagory = database_session.query(Catagory).all()
    itemTitle = "Latest Items"
    itemShow = database_session.query(Items).join(
        Items.catagory).order_by(desc(Items.date)).limit(10).all()
    return render_template(
        "index.html", catagory=catagory, itemShow=itemShow,
        itemTitle=itemTitle, home=True, login=session['logined'])


@app.route("/catalog/items/<catagoryTarget>")
def indexDisplayTemp(catagoryTarget):
    catagory = database_session.query(Catagory).all()
    itemTitle = catagoryTarget
    itemShow = database_session.query(Items).join(
        Items.catagory).filter_by(name=catagoryTarget).all()
    return render_template(
        "index.html", catagory=catagory, itemShow=itemShow,
        itemTitle=itemTitle, login=session['logined'])


@app.route("/newCatagory", methods=["GET", "POST"])
def newCatagory():
    if not session['logined']:
        flash('Please login first in order to add the new catagory')
        return redirect('/')
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


@app.route("/item/<int:item_id>")
def viewItem(item_id):
    item = database_session.query(Items).filter_by(id=item_id).join(
        Items.catagory).one()
    return render_template(
        "viewItem.html", item=item, id=item_id, login=session['logined'])


@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def editItem(item_id):
    if not session['logined']:
        flash('Please login first in order to edit the items')
        return redirect('/')
    if request.method == "POST":
        item_update = database_session.query(Items).filter_by(id=item_id).one()
        item_update.name = request.form["name"]
        item_update.catagory_id = request.form["catagory_id"]
        item_update.description = request.form["description"]
        database_session.add(item_update)
        database_session.commit()
        flash("Item \"%s\" has been updated!" % (item_update.name,))
        return redirect("/")
    else:
        try:
            item = database_session.query(Items).filter_by(id=item_id).join(
                Items.catagory).one()
            catagory = database_session.query(Catagory).all()
            return render_template(
                "itemForm.html", item=item, catagory=catagory, editFlag=True)
        except NoResultFound:
            return render_template("itemForm.html")


@app.route("/item/<int:item_id>/delete", methods=["GET", "POST"])
def deleteItem(item_id):
    if not session['logined']:
        flash('Please login first in order to delete the items')
        return redirect('/')
    if request.method == "POST":
        item = database_session.query(Items).filter_by(id=item_id).join(
            Items.catagory).one()
        database_session.delete(item)
        database_session.commit()
        flash("Item \"%s\" in \"%s\" has already deleted!" %
              (item.name, item.catagory.name))
        return redirect("/")
    else:
        try:
            item = database_session.query(Items).filter_by(id=item_id).join(
                Items.catagory).one()
            return render_template("delete.html", item=item, id=item_id)
        except NoResultFound:
            return render_template("itemForm.html")


@app.route("/item/new", methods=["GET", "POST"])
def newItem():
    if not session['logined']:
        flash('Please login first in order to add the new items')
        return redirect('/')
    if request.method == "POST":
        record = Items(name=request.form["name"], catagory_id=request.form[
                       "catagory_id"], description=request.form["description"])
        database_session.add(record)
        database_session.commit()
        flash("Item \"%s\" has already created!" %
              (record.name,))
        return redirect("/")
    else:
        catagory = database_session.query(Catagory).all()
        item = None
        return render_template(
            "itemForm.html", catagory=catagory, item=item, editFlag=False)


@app.route("/catalog.json")
def databaseToJSON():
    items = database_session.query(Items).join(Items.catagory).all()
    if request.args.get('raw') == "1":
        return jsonify(Item=[i.serialize for i in items])
    else:
        output = []
        for i in items:
            output.append({
                "name": i.name,
                'description': i.description,
                'date_created': i.date,
                'catagory': i.catagory.name
            })
        return jsonify(Items=output)


@app.route("/login")
def login():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(16))
    session['state'] = state
    return render_template("login.html", state=state, login=session['logined'])


@app.route("/fbconnect")
def fbconnect():
    if request.args.get('state') != session['state']:
        response = make_response(json.dunps("Invalid Request!!!"), 401)
        response.header['Content-type'] = 'application/json'
        return response
    session['logined'] = True
    return 'success'


@app.route("/fbdisconnect")
def fbdisconnect():
    session['logined'] = False
    flash("Sucessfully logout!")
    return redirect('/')