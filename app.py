from flask import Flask, render_template, session, url_for, redirect, request
import os
import db_functions #import the functions file
#---------TO FLASH: flash("message here")-------------------

#create flask app and establish secret_key
app = Flask(__name__)
#encrypts cooke values
app.secret_key = os.urandom(32)

#------REPLACE WITH DICT OF ACCOUNT FROM DB--------
#the user is a key, it's value is a list
#the list contains the password and a list of all the book's they've edited
accounts = {'topher':['stuycs', ['how to cs at stuy']]}
#--------------------------------------------------

#landing page
@app.route("/")
def root():
    #is the user is already logged in, then take them directly to the home/view all stories page
    if 'uname' in session.keys():
        return render_template('viewall.html')
    else: #if they're not logged in, bring them to the general welcome page and ask them to login/signup
        return render_template('welcome.html') #OR WHATEVER THE WELCOME PAGE HTML IS

@app.route("/login")
def login():
    form_dict = request.args
    uname = form_dict['uname'] #get user from url string
    password = form_dict['password'] #get pass from url string

    #check for existing user
    if uname in accounts.keys():
        #check matching password
        if accounts[uname] == password:
            #add username to the current session
            session['uname'] = uname
            return render_template("viewall.html", title = '<INSERT HTML THAT WILL CREATE A BUTTON THAT WILL LINK TO THE ONESTORY PAGE AND INPUT THE STORY FROM THE DB WITH JINJA>') #must send username var for jinja
        else:
            return render_template("login.html", msg = "Incorrect password.")
    else:
        return render_template('login.html', msg = "Incorrect username.")


@app.route("/register")
def register():
    form_dict = request.args
    uname = form_dict['username']
    pass1 = form_dict['password1']
    pass2 = form_dict['password2']

    if uname in accounts.keys(): #is username taken
        return render_template("register.html", msg = "That username is taken.")
    else:
        if pass1 == pass2: #if the passwords match, create account
            db_functions.add_account(username, password1)
            session['uname'] = uname #add the username to the session
            return render_template("viewall.html", title = '<INSERT HTML THAT WILL CREATE A BUTTON THAT WILL LINK TO THE ONESTORY PAGE AND INPUT THE STORY FROM THE DB WITH JINJA>')
        else:
            return render_template("register.html", msg = "Passwords do not match.")
