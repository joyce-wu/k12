
import sqlite3
import csv

#accounts
account_db = sqlite3.connect("accounts_database.db");
account_c = account_db.cursor();

account_c.execute("CREATE TABLE accounts (user TEXT PRIMARY KEY, password TEXT, contributed_stories INTEGER)")

def add_account(user, password):
    #check to see if user doesn't exist
    accounts = account_c.execute("SELECT user FROM accounts WHERE user = '%s'" %(user))
    data = account_c.fetchall()
    if(len(data) == 0):
        #contributed_stories is empty at first
        account_c.execute("INSERT INTO accounts VALUES ('%s', '%s', '%s')" %(user, password, ''))
        print("Success: Added " + user + "!")
    else:
        print("Failed: Username already exists!")

def add_story(user, story):
    stories = account_c.execute("SELECT contributed_stories FROM accounts WHERE user = '%s'" %(user))
    story_data = account_c.fetchall()
    print(story_data)
    if(len(story_data) == 0):
        new_stories = story
    #else:
        #assumes that the
        #new_stories = story_data + ',' + story
        account_c.execute("UPDATE accounts SET contributed_stories = '%s'" %(new_stories))
        print("Success: %s has contributed to %s" %(user, story))

def print_all_accounts():
    accounts = account_c.execute("SELECT * FROM accounts")
    for account in accounts:
        print(account)

add_account('donut', '1234')
add_account('asdjlkf', '123429')
add_account('donqwut', '1qw234')
add_account('donqwut', '1qw234')

add_story('donut', 'doNutFactory')
add_story('donut', 'doNetFactory')
add_story('donut', 'doNotFactory')
print_all_accounts()

account_db.commit()
account_db.close()





#stories
'''stories_db = sqlite3.connect("stories_database");
stories_c = stories_db.cursor();

stories_c.execute("CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT, link TEXT)")


stories_db.commit();
stories_db.close();
'''
