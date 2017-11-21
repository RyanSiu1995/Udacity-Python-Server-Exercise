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

# Initialize the web server and specify the parameters
app = Flask("__main__")
app.debug = True
app.secret_key = "RyanIsSoHandsome"


@app.route("/")
@app.route("/index")
def indexDisplay():
    # Query the catagories and latest items
    catagory = database_session.query(Catagory).all()
    itemTitle = "Latest Items"
    itemShow = database_session.query(Items).join(
        Items.catagory).order_by(desc(Items.date)).limit(10).all()
    # Try to access the session variable logined
    # If it is not set yet, it will be set for checking the login
    # index.html will share with viewing the items in catagory
    # Have to pass the home parameter to identify the index
    try:
        return render_template(
            "index.html", catagory=catagory, itemShow=itemShow,
            itemTitle=itemTitle, home=True, login=session['logined'])
    except:
        session['logined'] = False
        return render_template(
            "index.html", catagory=catagory, itemShow=itemShow,
            itemTitle=itemTitle, home=True, login=session['logined'])


@app.route("/catalog/items/<catagoryTarget>")
def indexDisplayTemp(catagoryTarget):
    # Query the items with selected catagory
    catagory = database_session.query(Catagory).all()
    itemTitle = catagoryTarget
    itemShow = database_session.query(Items).join(
        Items.catagory).filter_by(name=catagoryTarget).all()
    return render_template(
        "index.html", catagory=catagory, itemShow=itemShow,
        itemTitle=itemTitle, login=session['logined'])


@app.route("/newCatagory", methods=["GET", "POST"])
def newCatagory():
    # Set up the guard to the restricted page
    try:
        if not session['logined']:
            flash('Please login first in order to add the new catagory')
            return redirect('/')
    except:
        flash('Please login first in order to add the new catagory')
        return redirect('/')
    # If the method is POST, do the following
    if request.method == "POST":
        newCataName = request.form["catagory"]
        try:
            # Prevent catagory from repeating
            item = database_session.query(
                Catagory).filter_by(name=newCataName).one()
            flash("Catagory \"%s\" has already existed!" % (newCataName,))
            return redirect("/newCatagory")
        except NoResultFound:
            # Try to add the new catagory
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
    # Query the details of the items and render
    item = database_session.query(Items).filter_by(id=item_id).join(
        Items.catagory).one()
    try:
        return render_template(
            "viewItem.html", item=item, id=item_id, login=session['logined'])
    except:
        # Prevent the session variable from unsetting
        session['logined'] = False
        return render_template(
            "viewItem.html", item=item, id=item_id, login=session['logined'])


@app.route("/item/<int:item_id>/edit", methods=["GET", "POST"])
def editItem(item_id):
    # Set up the guard to the restricted page
    try:
        if not session['logined']:
            flash('Please login first in order to edit the items')
            return redirect('/')
    except:
        flash('Please login first in order to edit the items')
        return redirect('/')
    # If the method is POST, connect to the database and update it
    if request.method == "POST":
        item_update = database_session.query(Items).filter_by(id=item_id).one()
        item_update.name = request.form["name"]
        item_update.catagory_id = request.form["catagory_id"]
        item_update.description = request.form["description"]
        # Commit the changes and except the errors
        try:
            database_session.add(item_update)
            database_session.commit()
            flash("Item \"%s\" has been updated!" % (item_update.name,))
            return redirect("/")
        except SQLAlchemyError:
            flash("Cannot edit the item! Please contact developer!")
            return redirect("/")
    else:
        # Render the item edited to user
        try:
            item = database_session.query(Items).filter_by(id=item_id).join(
                Items.catagory).one()
            catagory = database_session.query(Catagory).all()
            return render_template(
                "itemForm.html", item=item, catagory=catagory, editFlag=True)
        except NoResultFound:
            flash("Cannot find the item!")
            return redirect('/')


@app.route("/item/<int:item_id>/delete", methods=["GET", "POST"])
def deleteItem(item_id):
    # Set up the guard to the restricted page
    try:
        if not session['logined']:
            flash('Please login first in order to delete the items')
            return redirect('/')
    except:
        flash('Please login first in order to delete the items')
        return redirect('/')
    # If the request is POST, try to delete the item
    if request.method == "POST":
        item = database_session.query(Items).filter_by(id=item_id).join(
            Items.catagory).one()
        database_session.delete(item)
        database_session.commit()
        flash("Item \"%s\" has already deleted!" %
              (item.name, ))
        return redirect("/")
    else:
        # Try to find the item and render to the confirmation page
        try:
            item = database_session.query(Items).filter_by(id=item_id).join(
                Items.catagory).one()
            return render_template("delete.html", item=item, id=item_id)
        except NoResultFound:
            flash("Cannot find the item!")
            return redirect('/')


@app.route("/item/new", methods=["GET", "POST"])
def newItem():
    # Set up the guard to the restricted page
    try:
        if not session['logined']:
            flash('Please login first in order to add the new items')
            return redirect('/')
    except:
        flash('Please login first in order to add the new items')
        return redirect('/')
    # If the method is POST, try to add the new record
    if request.method == "POST":
        record = Items(name=request.form["name"], catagory_id=request.form[
                       "catagory_id"], description=request.form["description"])
        # Try to add the new items
        try:
            database_session.add(record)
            database_session.commit()
        except SQLAlchemyError:
            flash("Cannot edit the item! Please contact developer!")
            return redirect("/")
        # Flash the system message
        flash("Item \"%s\" has already created!" %
              (record.name,))
        return redirect("/")
    else:
        # Render the existing catagories for selection
        catagory = database_session.query(Catagory).all()
        item = None
        return render_template(
            "itemForm.html", catagory=catagory, item=item, editFlag=False)


@app.route("/catalog.json")
def databaseToJSON():
    items = database_session.query(Items).join(Items.catagory).all()
    # If the query string raw is equal to 1
    # The catagory id will be shown
    # Otherwise
    # The name of catagory will be shown
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
    # Try to create a state variable to confirm the login reques
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(16))
    session['state'] = state
    # Try to get the session variable logined
    try:
        return render_template(
            "login.html", state=state, login=session['logined'])
    except:
        session['login'] = False
        return render_template(
            "login.html", state=state, login=session['logined'])


@app.route("/fbconnect", methods=['POST'])
def fbconnect():
    # If the state variable from request is not the same as the one 
    # in session,
    # Reject the request
    if request.args.get('state') != session['state']:
        response = make_response(json.dunps("Invalid Request!!!"), 401)
        response.header['Content-type'] = 'application/json'
        return response
    session['logined'] = True

    # Get the server token from facebook
    clientToken = request.data
    file = open('secret.json', 'r')
    fbsecret = json.loads(file.read())
    url = 'https://graph.facebook.com/oauth/access_token?' \
        'grant_type=fb_exchange_token&client_id=%s&client_secret=%s' \
        '&fb_exchange_token=%s' % (
            fbsecret['app_id'], fbsecret['secret'], clientToken)
    http = httplib2.Http()
    result = http.request(url, 'GET')[1]
    serverToken = result.split(',')[0].split(':')[1].replace('"', '')
    session['token'] = serverToken

    # Get the user information
    userinfo_url = 'https://graph.facebook.com/v2.8/me'\
        '?access_token=%s&fields=name,id,email' % serverToken
    http = httplib2.Http()
    userinfo = json.loads(http.request(userinfo_url, 'GET')[1])
    # Attach the result to session
    session['provider'] = 'facebook'
    session['user'] = userinfo["name"]
    session['email'] = userinfo["email"]
    session['facebook_id'] = userinfo["id"]

    # Flash the system message
    flash('Login Successfully via %s as %s.' % (
        session['provider'], session['user']))

    return 'success'


@app.route("/fbdisconnect")
def fbdisconnect():
    # Set the session variable to be false
    session['logined'] = False
    # Try to clear the connection from facebook
    # If session variable cannot be found,
    # just return to the index for lazy detaching
    try:
        url = 'https://graph.facebook.com/%s/' \
            'permissions?access_token=%s' % (
                session['facebook_id'], session['token'])
        http = httplib2.Http()
        http.request(url, 'DELETE')
    except:
        flash("Session has already ended in server")
        return redirect('/')
    # Try to delete the session variable for security
    try:
        del session['token']
        del session['provider']
        del session['user']
        del session['email']
        del session['facebook_id']
        flash("Sucessfully logout!")
        return redirect('/')
    except:
        flash("Session has already ended in server")
        return redirect('/')
