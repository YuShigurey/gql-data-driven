"""https://docs.python.org/3/library/sqlite3.html"""

from email.policy import default
import sqlite3

con = sqlite3.connect("foo.db")
cur = con.cursor()
cur.execute("PRAGMA foreign_keys = ON")
cur.execute("CREATE TABLE IF NOT EXISTS has_attribute(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT)")
cur.execute("CREATE TABLE IF NOT EXISTS attribute(id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, type TEXT, defaultValue TEXT, isCore TEXT, description TEXT, example TEXT)")
cur.execute(
"""
CREATE TABLE IF NOT EXISTS has_attribute_attribute_link(
has_attribute_attribute_link_id INTEGER PRIMARY KEY AUTOINCREMENT,
has_attribute_id INTEGER,
attribute_id INTEGER,
FOREIGN KEY (has_attribute_id) REFERENCES has_attribute(id) ON DELETE CASCADE ON UPDATE CASCADE, 
FOREIGN KEY (attribute_id) REFERENCES attribute(id) ON DELETE CASCADE ON UPDATE CASCADE
)
"""
)
# "CREATE TABLE IF NOT EXISTS child (id text PRIMARY KEY NOT NULL ,parentID TEXT,FOREIGN KEY (parentID) REFERENCES parent(id) ON DELETE CASCADE ON UPDATE CASCADE);"

default_attribute = dict(
    "name": "",
    "type": "",
    "defaultValue": "",
    "isCore": "yes",
    "description": "",
    "example": ""
)