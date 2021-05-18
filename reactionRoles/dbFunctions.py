import sqlite3 as sql
from const import DBNAME

initialized = False

# Database has table reactionRole(messageID, reactionEmote, roleID)

#Adds a reaction role to the database
def addReactionRole(messageID, emoteName, roleID):
    if(not initialized):
        print("Tried to change DB when uninitialized!")
        return 0
    cur = sql.connect("{}.db".format(DBNAME)).cursor()
    cur.execute("INSERT INTO {} VALUES ({}, '{}', {}})".format(DBNAME, messageID, emoteName, roleID))
    cur.connection.commit()
    cur.connection.close()
    return 1

#Removes a reaction role from the database
def removeReactionRole(messageID, emoteName):
    if(not initialized):
        print("Tried to change DB when uninitialized!")
        return 0
    cur = sql.connect("{}.db".format(DBNAME)).cursor()
    cur.execute("DELETE FROM {} WHERE messageID = {} and reactionEmote = '{}'".format(DBNAME, messageID, emoteName))
    cur.connection.commit()
    cur.connection.close()
    return 1

#Checks if DB is initalized and if not initializes it
def initDB():
    print("Checking for DB...")
    con = sql.connect("{}.db".format(DBNAME))
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='reactionRole';")
    #Create table if it does not exist
    if(not cur.fetchone()):
        print("Could not find reactionRole table!")
        print("Creating reactionRole table...")
        cur.execute(
            """CREATE TABLE reactionRole(
            messageID INTEGER NOT NULL,
            reactionEmote TEXT NOT NULL,
            roleID INTEGER NOT NULL,
            PRIMARY KEY (messageID, reactionEmote)
            )"""
        )
        print("reactionRole table created!")
        con.commit()
    print("Connected to DB!")
    con.close()
    global initialized
    initialized = True