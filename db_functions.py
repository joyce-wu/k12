
import sqlite3
import csv

#accounts
account_db = sqlite3.connect("accounts_database.db");
account_c = account_db.cursor();

account_c.execute("CREATE TABLE accounts (user TEXT, password TEXT, contributed_stories INTEGER)")

def add_account(user, password):
    account_c.execute("INSERT INTO accounts VALUES (" + user + ", " + password + ")")
    #account_c.execute("INSERT INTO accounts VALUES ({0}, {1})" format(user, password))
    #account_c.execute("INSERT INTO accounts VALUES (%s, %s)" %(user, password))

def print_all_accounts():
    accounts = account_c.execute("SELECT * FROM accounts")
    for account in accounts:
        print(account)

add_account('donut', '1234')
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
