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
#--------------------------------------------------

#landing page
@app.route("/",methods=['POST','GET'])
def root():
    #is the user is already logged in, then take them directly to the home/view all stories page
    print(db_functions.stories_dict())
    if 'username' in session.keys():
        title_id_list = []
        stories = db_functions.stories_dict()
        for id in stories:
            title_id_list.append([str(id), str(stories[id][0])])
        return render_template("viewall.html", title_id_list = title_id_list)
    else: #if they're not logged in, bring them to the general welcome page and ask them to login/signup
        return render_template('welcome.html')

@app.route("/login",methods=['POST','GET'])
def login():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    if 'username' in session:
        #create list of story ids, titles
        title_id_list = []
        for id in stories:
            title_id_list.append([str(id), str(stories[id][0])])
        return render_template("viewall.html", title_id_list = title_id_list)
    else:
        return render_template("login.html")


@app.route("/check_login",methods=['POST','GET'])
def check_login():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

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
                title_id_list.append([str(id), str(stories[id][0])])
            return render_template("viewall.html", title_id_list = title_id_list) #must send username var for jinja
        else:
            return render_template("login.html", msg = "Incorrect password.")
    else:
        return render_template('login.html', msg = "Incorrect username.")


@app.route("/register",methods=['POST','GET'])
def register():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    if 'username' not in session:
        return render_template('register.html')
    else:
        #create list of story ids, titles
        title_id_list = []
        for id in stories:
            title_id_list.append([str(id), str(stories[id][1])])
            return render_template("viewall.html", title_id_list = title_id_list)

@app.route('/check_register',methods=['POST','GET'])
def check_register():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    form_dict = request.args
    uname = form_dict['username']
    pass1 = form_dict['password1']
    pass2 = form_dict['password2']

    if uname in accounts.keys(): #is username taken
        return render_template("register.html", msg = "That username is taken.")
    else:
        if pass1 == pass2: #if the passwords match, create account
            print(uname + " " + pass1)
            db_functions.add_account(uname, pass1)
            db_functions.print_all_accounts()

            session['username'] = uname #add the username to the session

            #create list of story ids, titles
            title_id_list = []
            for ID in stories:
                title_id_list.append([str(ID), str(stories[ID][0])])
            return render_template("viewall.html", title_id_list= title_id_list, msg = 'Welcome.')
        else:
            return render_template("register.html", msg = "Passwords do not match.")



@app.route("/viewall",methods=['POST','GET'])
def viewall():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    form_dict = request.args
    chosen_ID = int(form_dict['chosen_ID']) #THIS IS AN ID

    #FOR COMPOSING
    if chosen_ID == -1:
        return render_template("compose.html")


    #FOR EDITING
    #if their chosen story is one that they've ALREADY edited, then they can read it
    #print('*****CHOSEN ID******')
    #print(chosen_ID)

    #print('****SESSION USER****')
    #print(session.get('username'))

    if chosen_ID not in accounts[ session.get('username') ][1]: #CHECK FOR ACCURACY
        print(session.get('username'))
        print(stories[chosen_ID][2])
        return render_template("edit.html", chosen_ID = chosen_ID, title = stories[chosen_ID][0], last_update = stories[chosen_ID][2], msg = "Since you have not yet edited this story, you must do so before viewing the entire story.") #they can edit
    else: #if they have already edited the story
        return render_template("onestory.html", title = stories[chosen_ID][0], story = stories[chosen_ID][1], msg = "You\'ve contributed to this story before. While you can't contribute to it again, you can read the whole story so far.")



@app.route("/compose",methods=['POST','GET'])
def compose():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    form_dict = request.args
    title =  form_dict['title']
    story = form_dict['story']
    user = session.get('username')

    #create a new ID number for this story
    if bool(stories) == False: #if the stories dict is empty
        new_ID = 0
    else: #if stories dict has stories in it already
        new_ID = len(stories)

    #function for adding user info into accounts db and story to story db
    db_functions.add_story_user(user, new_ID)
    db_functions.add_story(title, story)
    return render_template("onestory.html", title = title, story = story, msg = "Successfully composed new story. Here\'s your story so far. Users wil be able to add to you story in the future. Although you can\'t edit it again, you can check up on it later to see if anyone else has continued it!")


@app.route("/edit",methods=['GET'])
def edit():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    form_dict = request.args
    chosen_ID = int(form_dict['chosen_ID'])
    update = form_dict['update']
    user = session.get('username')

    #function to update account db to include newly edited story
    db_functions.add_story_user(user, chosen_ID)
    #function to add story update to story
    db_functions.update_story(chosen_ID, update)
    stories = db_functions.stories_dict()
    return render_template("onestory.html", title = stories[chosen_ID][0], story = stories[chosen_ID][1], msg = "Successfully edited story. Here\'s the story so far. While you can't contibute to it again in the future, you can always check back here to see if anyone else has continued the story!")


@app.route("/logout",methods=['POST','GET'])
def logout():
    accounts = db_functions.accounts_dict()
    stories = db_functions.stories_dict()

    #remove user info from session
    if 'username' in session:
        session.pop('username')
    return render_template('welcome.html', msg = 'Logout was successful.')


#db_functions.finish()

#-------------------------------
if __name__ == "__main__":
    app.debug = True
    app.run()
