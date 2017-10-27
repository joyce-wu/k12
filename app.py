from flask import Flask, render_template, session, url_for, redirect, request
import os
import db_functions #import the functions file
#---------TO FLASH: flash("message here")-------------------

#create flask app and establish secret_key
app = Flask(__name__)
#encrypts cooke values
app.secret_key = os.urandom(32)

#------REPLACE WITH DICT OF ACCOUNT FROM DB--------
#user:[password, [story_ids]]
accounts = {'topher':['stuycs', [0, 1]]}

#story_id:[title, content, update]
stories = {0:['how to cs at stuy', 'YOU GOTTA USE YOUR KTS', 'KTS'], 1:['rubber ducky', 'you\'r so fine']}
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
            title =
            return render_template("viewall.html", title = '<INSERT HTML THAT WILL CREATE A BUTTON THAT WILL LINK TO THE ONESTORY PAGE AND INPUT THE STORY FROM THE DB WITH JINJA>', msg = '')
        else:
            return render_template("register.html", msg = "Passwords do not match.")


@app.route("/viewall")
def viewall():
    form_dict = request.args
    chosen_ID = int(form_dict['chosen_ID']) #THIS IS AN ID

    #FOR EDITING
    #if their chosen story is one that they've ALREADY edited, then they can read it
    if chosen_ID not in accounts.(session['uname'])[1]: #CHECK FOR ACCURACY
        return render_template("edit.html", title = stories.(chosen_ID)[0], last_update = stories.(chosen_ID)[1], chosen_ID = chosen_ID)
    else:
        return render_template("viewall.html", title = '<INSERT HTML THAT WILL CREATE A BUTTON THAT WILL LINK TO THE ONESTORY PAGE AND INPUT THE STORY FROM THE DB WITH JINJA>', msg = "You can't edit this story again. Pick another one.")

    #FOR COMPOSING
    if chosen_ID == -1:
        return render_template("compose.html")

@app.route("/compose")
def compose():
    form_dict = request.args
    #############note: ASK BAYAN FOR COMPOSE PAGE TO ALSO INCLUDE JINJA FOR LAST update
    title =  form_dict['title']
    body = form_dict['body']
    user = session['uname']
    new_ID = stories[-1] + 1 #CHECK FOR ACCURACY
    #function for adding user info into accounts db
    add_account_info(user, new_ID)
    #function for adding story to story db
    add_story(new_ID, title, body)


@app.route("/edit")
def edit():
    form_dict = request.args
    chosen_ID = form_dict['chosen_ID']
    update = form_dict['update']

@app.route("/logout")
def logout():
    #remove user info from session
    if 'uname' in session:
        session.pop('uname')
    return render_template('welcome.html', msg = '')





#-------------------------------
if __name__ == "__main__":
    app.debug = True
    app.run()
