from sqlite3 import connect

class Database:
  def __init__(self):
    self.db = connect('database.db')
    with open('schema.sql') as r:
      self.db.executescript(r.read())
