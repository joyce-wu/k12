
import sqlite3
import csv
import threading

#lock = threading.RLock()

#accounts database
#, check_same_thread=False); #
account_db = sqlite3.connect("accounts_database");
account_c = account_db.cursor();

#checks to see if accounts database was already created
try:
    account_c.execute("CREATE TABLE accounts (user TEXT PRIMARY KEY, password TEXT, contributed_stories TEXT)")
except:
    print()

account_db.commit();
account_db.close();

#add_account() adds an account given its username and password
#password should be a string
def add_account(user, password):
    account_db = sqlite3.connect("accounts_database");
    account_c = account_db.cursor();

    #looks through the table to see if the user already exists
    #with lock:
    accounts = account_c.execute("SELECT user FROM accounts WHERE user = '%s'" %(user))
    data = account_c.fetchall()
    if(len(data) == 0):
        #contributed_stories is empty at first
        account_c.execute("INSERT INTO accounts VALUES ('%s', '%s', '%s')" %(user, password, '[]'))
        print("Success: Added " + user + "!")
    else:
        print("Failed: Username already exists!")

    account_db.commit();
    account_db.close();

#add_story() adds the given story to the user's list of contributed stories
#story should be a string
def add_story_user(user, story):
    account_db = sqlite3.connect("accounts_database");
    account_c = account_db.cursor();

    #checks to see if the user exists
    stories = account_c.execute("SELECT contributed_stories FROM accounts WHERE user = '%s'" %(user))
    stories_data = account_c.fetchall()
    if(len(stories_data) == 0):
        print("The user does not exist!")
    else:
        #eval() turns the string into list
        list_stories = eval(stories_data[0][0])
        try:
            list_stories.index(story)
            print("%s has already contributed to this story!" %(user))
        except:
            #insert stories in order
            i = 0;
            for ele_story in list_stories:
                if ele_story > story:
                   list_stories.insert(i, story)
                   break
                i+=1
            if i == len(list_stories):
                list_stories.append(story)
            #updates the database
            account_c.execute("UPDATE accounts SET contributed_stories = \"%s\" WHERE user = '%s'" %(repr(list_stories), user))
            print("Success: %s has contributed to %s" %(user, story))

    account_db.commit();
    account_db.close();

#print_all_accounts() prints out all the accounts in the database
def print_all_accounts():
    account_db = sqlite3.connect("accounts_database");
    account_c = account_db.cursor();

    accounts = account_c.execute("SELECT * FROM accounts")
    for account in accounts:
        print(account)

    account_db.commit();
    account_db.close();
print("*******PRINT ALL ACCTS********")
print_all_accounts


#stories database
stories_db = sqlite3.connect("stories_database");
stories_c = stories_db.cursor();
#checks to see if stories database was already created
try:
    stories_c.execute("CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT, whole_story TEXT, last_update TEXT)")
except:
    print()

stories_db.commit();
stories_db.close();

def get_id(title):
    stories = stories_dict()
    for story_id in stories:
        if(stories[story_id][0] == title):
            return story_id

#add_story() adds the story
#returns the id of the new story
def add_story(title, text):
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();
    new_id = next_id()
    stories_c.execute("INSERT INTO stories VALUES ('%d', '%s', '%s', '%s')" %(new_id, title, "\t" + text, "\t" + text))
    stories_db.commit();
    stories_db.close();
    return new_id

#next_id() finds the next available id
#helper function for add_story()
def next_id():
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    stories_c.execute("SELECT id FROM stories WHERE ID = (SELECT MAX(ID) FROM stories)")
    prev_id = stories_c.fetchall()
    if len(prev_id) == 0:
        return 0

    stories_db.commit();
    stories_db.close();

    return prev_id[0][0] + 1

#update_story() adds new text into the story
#story_id should be an integer
def update_story(story_id, new_text):
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    #checks to see if story exists
    stories_c.execute("SELECT * FROM stories WHERE id = " + str(story_id))
    story = stories_c.fetchall()
    if len(story) == 0:
        print("Failed: Story does not exist!")
    else:
        #updates last_update and whole_story
        old_whole_story = story[0][2]

        stories_c.execute("UPDATE stories SET last_update = '%s' WHERE id = %d" %("\t" + new_text, story_id))
        stories_c.execute("UPDATE stories SET whole_story = '%s' WHERE id = %d" %(old_whole_story + "\n\t"+ new_text, story_id))

    stories_db.commit();
    stories_db.close();

#print_all_stories() prints all stories
def print_all_stories():
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    stories = stories_c.execute("SELECT * FROM stories")
    for story in stories:
        print(story)
    stories_db.commit();
    stories_db.close();

#print_last_update_story_content() prints the last_update of the given story
def print_last_update_story_content(story_id):
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    stories_c.execute("SELECT last_update FROM stories WHERE id = " + str(story_id))
    story = stories_c.fetchall()
    print(story[0][0])

    stories_db.commit();
    stories_db.close();

#print_whole_story_content() prints the whole_story of the given story
def print_whole_story_content(story_id):
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    stories_c.execute("SELECT whole_story FROM stories WHERE id = " + str(story_id))
    story = stories_c.fetchall()
    print(story[0][0])

    stories_db.commit();
    stories_db.close();

#print_story() returns the story based on its permissions
#story_id should be an integer
def print_story(user, story_id):
    account_db = sqlite3.connect("accounts_database");
    account_c = account_db.cursor();

    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    #checks to see if user exists
    stories = account_c.execute("SELECT contributed_stories FROM accounts WHERE user = '%s'" %(user))
    stories_data = account_c.fetchall()
    if(len(stories_data) == 0):
        print("The user does not exist!")
    else:
        #if the story's id is not found in the user's contributed_stories, then it hasn't contributed to the story before
        list_stories = eval(stories_data[0][0])
        try:
            list_stories.index(str(story_id))
            print("%s has contributed to the story before" %(user))
            data = "whole_story"
        except ValueError:
            print("%s hasn't contributed to the story before" %(user))
            data = "last_update"
        stories_c.execute("SELECT %s FROM stories WHERE id = '%d'" %(data, story_id))

        one_story = stories_c.fetchall()[0][0]

        account_db.commit();
        account_db.close();

        stories_db.commit();
        stories_db.close();

        return one_story

#accounts_dict() returns a dictionary with info from the accounts database
def accounts_dict():
    account_db = sqlite3.connect("accounts_database");
    account_c = account_db.cursor();

    account_c.execute("SELECT * FROM accounts")
    accounts = account_c.fetchall()
    acc_dict = {}
    for account in accounts:
        user = account[0]
        pwd = account[1]
        stories = eval(account[2])
        acc_dict[account[0]] = (pwd, stories)

    account_db.commit();
    account_db.close();

    return acc_dict

#stories_dict() returns a dictionary with info from the stories database
def stories_dict():
    stories_db = sqlite3.connect("stories_database");
    stories_c = stories_db.cursor();

    stories_c.execute("SELECT * FROM stories")
    stories = stories_c.fetchall()
    stry_dict = {}
    for story in stories:
        stry_dict[story[0]] = story[1:]

    stories_db.commit();
    stories_db.close();

    return stry_dict


#testing

print('*******ADDING ACCOUNTS*******')
add_account('donut', '1234')
add_account('brown', 'stuycs')
add_account('dw', 'arthur')
add_account('harold', 'fred')

print_all_accounts()

print ("\n\n******USERS CONTRIBUTING******")
add_story_user('brown', '1')
add_story_user('donut', '0')
add_story_user('donut', '5')
add_story_user('donut', '8912')
add_story_user('donut', '92')

print ('\n\n******ADD STORY*******')
add_story('da donut story', 'there was once a donut')
add_story('da', 'asdf')
add_story('the cow family', 'the cow said moo')
add_story('cats... meow', 'cats are cute')

update_story(2, "and then he ate a donut")
#print_all_stories()
#print_whole_story_content(2)
#print_last_update_story_content(2)
print('\n\n****PRINT STORY****')
print(print_story('donut', 2))

add_story_user('donut','2')
print(print_story('donut', 2))

print('\n\n****PRINT ACCOUNT DICT****')
print(accounts_dict())

print('\n\n****PRINT STORY DICT****')
print(stories_dict())



#finish() commits changes and closes the databases
def finish():
    account_db.commit();
    account_db.close();

    stories_db.commit();
    stories_db.close();
