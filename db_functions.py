
import sqlite3
import csv
'''
#accounts database
account_db = sqlite3.connect("accounts_database.db");
account_c = account_db.cursor();


account_c.execute("CREATE TABLE accounts (user TEXT PRIMARY KEY, password TEXT, contributed_stories TEXT)")

#add_account() adds an account given its username and password
def add_account(user, password):
    #looks through the table to see if the user already exists
    accounts = account_c.execute("SELECT user FROM accounts WHERE user = '%s'" %(user))
    data = account_c.fetchall()
    if(len(data) == 0):
        #contributed_stories is empty at first
        account_c.execute("INSERT INTO accounts VALUES ('%s', '%s', '%s')" %(user, password, '[]'))
        print("Success: Added " + user + "!")
    else:
        print("Failed: Username already exists!")

#add_story() adds the given story to the user's list of contributed stories
def add_story_user(user, story):
    #checks to see if
    #eval(): string into list
    stories = account_c.execute("SELECT contributed_stories FROM accounts WHERE user = '%s'" %(user))
    stories_data = account_c.fetchall()
    if(len(stories_data) == 0):
        print("The user does not exist!")
    else:
        list_stories = eval(stories_data[0][0])
        #insert stories in order
        i = 0;
        for ele_story in list_stories:
            if ele_story > story:
               list_stories.insert(i, story) 
               break
            i+=1
        if i == len(list_stories):
            list_stories.append(story)
        account_c.execute("UPDATE accounts SET contributed_stories = \"%s\" WHERE user = '%s'" %(repr(list_stories), user))
        print("Success: %s has contributed to %s" %(user, story))

def print_all_accounts():
    accounts = account_c.execute("SELECT * FROM accounts")
    for account in accounts:
        print(account)

add_account('donut', '1234')
add_account('asdjlkf', '123429')
add_account('donqwut', '1qw234')
add_account('donqwut', '1qw234')

add_story_user('dont', '1')
add_story_user('donut', '0')
add_story_user('donut', '5')
add_story_user('donut', '8912')
add_story_user('donut', '92')
print_all_accounts()

account_db.commit()
account_db.close()



'''
#stories
stories_db = sqlite3.connect("stories_database");
stories_c = stories_db.cursor();

stories_c.execute("CREATE TABLE stories (id INTEGER PRIMARY KEY, title TEXT, whole_story TEXT, last_update TEXT)") #consider list of contributors?
def add_story(title, text):
    stories_c.execute("INSERT INTO stories VALUES ('%d', '%s', '%s', '%s')" %(next_id(), 'da donut story', "\t" + text, "\t" + text))
    print("Success: Added " + title + "!")

#convert accounts/stories database to csv?
def next_id():
    stories_c.execute("SELECT id FROM stories WHERE ID = (SELECT MAX(ID) FROM stories)")
    prev_id = stories_c.fetchall()
    if len(prev_id) == 0:
        return 0
    
    return prev_id[0][0] + 1

def update_story(story_id, new_text):
    stories_c.execute("SELECT * FROM stories WHERE id = " + str(story_id))
    story = stories_c.fetchall()
    if len(story) == 0:
        print("Failed: Story does not exist!")
    else:
        '''print("blarge===========")
        print(story)'''
        old_whole_story = story[0][2]

        stories_c.execute("UPDATE stories SET last_update = '%s' WHERE id = %d" %("\t" + new_text, story_id))
        stories_c.execute("UPDATE stories SET whole_story = '%s' WHERE id = %d" %(old_whole_story + "\n\t"+ new_text, story_id))
        
    
def print_all_stories():
    stories = stories_c.execute("SELECT * FROM stories")
    for story in stories:
        print(story)

        #print story(int id) --> check permissions --> if edited --> view entire story
        #                                              else --> view last update w/ edit button
def print_last_update_story_content(story_id):
    stories_c.execute("SELECT last_update FROM stories WHERE id = " + str(story_id))
    story = stories_c.fetchall()
    print(story[0][0])
    
def print_whole_story_content(story_id):
    stories_c.execute("SELECT whole_story FROM stories WHERE id = " + str(story_id))
    story = stories_c.fetchall()
    print(story[0][0])
    
    
add_story('da donut story', 'there was once a donut')
add_story('da', 'asdf')
add_story('the cow family', 'the cow said moo')
add_story('cats... meow', 'cats are cute')

update_story(2, "and then he ate a donut")
print_all_stories()
print_whole_story_content(2)
print_last_update_story_content(2)


stories_db.commit();
stories_db.close();
