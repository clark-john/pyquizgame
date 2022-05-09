from mysql.connector import connect, ProgrammingError
from json import load
# from mysql.connector.errorcode import (
#   ER_SERVER_ISNT_AVAILABLE
# )
from click import secho

class Database:
  loginfile = open('login.json', 'r') 
  details = load(loginfile)

  def __init__(self):
    try:
      global db
      self.db = connect(**self.details)
    # except Error as err:
      # if err.errno == ER_SERVER_ISNT_AVAILABLE:
        # print("server offline")
    except ProgrammingError as err:
      raise err
    secho("Database connected successfully", fg='bright_green')
    self.db.close()
  




    # with open('schema.sql') as r:
    #   self.db.executescript(r.read())

d=Database()