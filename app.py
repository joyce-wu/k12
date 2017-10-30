from flask import Flask, render_template, session, url_for, redirect, request
import os
import db_functions #import the functions file
#---------TO FLASH: flash("message here")-------------------

#create flask app and establish secret_key
app = Flask(__name__)
#encrypts cooke values
app.secret_key = os.urandom(32)

#------REPLACE WITH DICT OF ACCOUNT FROM DB--------
#str:[str, [str]]
#user:[password, [story_ids]]
#accounts = {'topher':['stuycs', [0, 1]]}
accounts = db_functions.accounts_dict()

#int:[str, str, str]
#story_id:[title, content, update]
#stories = {0:['how to cs at stuy', 'YOU GOTTA USE YOUR KTS', 'KTS'], 1:['rubber ducky', 'you\'r so fine']}
stories = db_functions.stories_dict()
#--------------------------------------------------

#landing page
@app.route("/")
def root():
    #create list of story ids, titles
    title_id_list = []
    for id in stories:
        title_id_list.append([str(id), str(stories[id][1])])

    #is the user is already logged in, then take them directly to the home/view all stories page
    if 'username' in session.keys():
        return render_template('viewall.html', title_id_list = title_id_list, msg = 'Welcome back.')
    else: #if they're not logged in, bring them to the general welcome page and ask them to login/signup
        return render_template('welcome.html', uname = '', password = '', password1 = '', password2 = '') #OR WHATEVER THE WELCOME PAGE HTML IS

@app.route("/login")
def login():
    if 'username' in session:
        #create list of story ids, titles
        title_id_list = []
        for id in stories:
            title_id_list.append([str(id), str(stories[id][1])])

            return render_template("viewall.html", title_id_list = title_id_list)
    else:
        return render_template("login.html")


@app.route("/check_login")
def check_login():
    form_dict = request.args
    uname = form_dict['username'] #get user from url string
    password = form_dict['password'] #get pass from url string

    #check for existing user
    if uname in accounts.keys():
        #check matching password
        if accounts[uname][0] == password:
            #add username to the current session
            session['username'] = uname

            #create list of story ids, titles
            title_id_list = []
            for id in stories:
                title_id_list.append([str(id), str(stories[id][1])])

                return render_template("viewall.html", title_id_list = title_id_list) #must send username var for jinja
        else:
            return render_template("login.html", msg = "Incorrect password.")
    else:
        return render_template('login.html', msg = "Incorrect username.")


@app.route("/register")
def register():
    if 'username' not in session:
        return render_template('register.html')
    else:
        #create list of story ids, titles
        title_id_list = []
        for id in stories:
            title_id_list.append([str(id), str(stories[id][1])])

            return render_template("viewall.html", title_id_list = title_id_list)

@app.route('/check_register')
def check_register():
    form_dict = request.args
    uname = form_dict['username']
    pass1 = form_dict['password1']
    pass2 = form_dict['password2']

    if uname in accounts.keys(): #is username taken
        return render_template("register.html", msg = "That username is taken.")
    else:
        if pass1 == pass2: #if the passwords match, create account
            print uname + " " + pass1
            db_functions.add_account(uname, pass1)
            db_functions.print_all_accounts()
            session['username'] = uname #add the username to the session

            #create list of story ids, titles
            title_id_list = []
            for id in stories:
                print ("********STORIES*********")
                print str(stories[id][1])
                title_id_list.append([str(id), str(stories[id][1])])


            return render_template("viewall.html", title_id_list = title_id_list, msg = 'Welcome.')
        else:
            return render_template("register.html", msg = "Passwords do not match.")



@app.route("/viewall")
def viewall():
    form_dict = request.args
    chosen_ID = int(form_dict['chosen_ID']) #THIS IS AN ID

    #FOR EDITING
    #if their chosen story is one that they've ALREADY edited, then they can read it
    if chosen_ID not in accounts[ session['username'] ][1]: #CHECK FOR ACCURACY
        print(session['username'])
        return render_template("edit.html", title = stories[chosen_ID][0], last_update = stories[chosen_ID][2], msg = "Since you have not yet edited this story, you must do so before viewing the entire story.") #they can edit
    else: #if they have already edited the story
        return render_template("onestory.html", title = stories[chosen_ID][0], story = stories[chosen_ID][1], msg = "You\'ve contributed to this story before. While you can't contribute to it again, you can read the whole story so far.")

    #FOR COMPOSING
    if chosen_ID == -1:
        return render_template("compose.html")

@app.route("/compose")
def compose():
    form_dict = request.args
    title =  form_dict['title']
    story = form_dict['story']
    user = session['username']

    #create a new ID number for this story
    if bool(stories) == False: #if the stories dict is empty
        new_ID = 0
    else: #if stories dict has stories in it already
        new_ID = len(stories)

    #function for adding user info into accounts db and story to story db
    add_story_user(user, new_ID)
    add_story(title, story, new_ID)
    return render_template("onestory.html", title = title, story = story, msg = "Successfully composed new story. Here\'s your story so far. Users wil be able to add to you story in the future. Although you can\'t edit it again, you can check up on it later to see if anyone else has continued it!")


@app.route("/edit")
def edit():
    form_dict = request.args
    chosen_ID = form_dict['chosen_ID']
    update = form_dict['update']
    user = session['username']

    #function to update account db to include newly edited story
    add_account_user(user, chosen_ID)
    #function to add story update to story
    update_story(chosen_ID, update)
    return render_template("onestory.html", title = stories[chosen_ID][0], story = stories[chosen_ID][1], msg = "Successfully edited story. Here\'s the story so far. While you can't contibute to it again in the future, you can always check back here to see if anyone else has continued the story!")


@app.route("/logout")
def logout():
    #remove user info from session
    if 'username' in session:
        session.pop('username')
    return render_template('welcome.html', msg = 'Logout was successful.')


db_functions.finish()

#-------------------------------
if __name__ == "__main__":
    app.debug = True
    app.run()
