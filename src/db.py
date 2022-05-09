from mysql.connector import connect, ProgrammingError
from json import load
from click import secho
from cryptography.fernet import Fernet 
from os import path
from mysql.connector.errorcode import ER_ACCESS_DENIED_ERROR

if path.exists('./db_password.key'):
  with open('./db_password.key', 'r') as k:
    key = k.read().encode()
    f = Fernet(key)
else:
  key = Fernet.generate_key()
  with open('./db_password.key', 'w') as k:
    k.write(key.decode())

class Database:
  loginfile = open('login.json', 'r') 
  details = load(loginfile)

  def __init__(self):
    try:
      self.details['password'] = f.decrypt(self.details['password'].encode()).decode()
      self.db = connect(**self.details)
      secho("Database connected successfully", fg='bright_green')

      self.db.close()
    except ProgrammingError as err:
      f.decrypt(self.details['password'].encode()).decode()
      if err.errno == ER_ACCESS_DENIED_ERROR:
        print("Wrong password or username")
      else:
        print(err)

      # print(errorcod)
  

    # with open('schema.sql') as r:
    #   self.db.executescript(r.read())

d=Database()