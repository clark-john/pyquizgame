from mysql.connector import connect, ProgrammingError
from json import load
from click import secho
from cryptography.fernet import Fernet 
from os import path
from mysql.connector.errorcode import ER_ACCESS_DENIED_ERROR

class Database:
  with open('login.json', 'r') as loginfile: 
    details = load(loginfile)

  if path.exists('db_password.key'):
    with open('./db_password.key', 'r') as k:
      key = k.read().encode()
    f = Fernet(key)
    print(key)
  else:
    key = Fernet.generate_key()
    with open('./db_password.key', 'w') as k:
      k.write(key.decode())
    f = Fernet(key)

  def __init__(self):
    try:
      self.details['password'] = self.f.decrypt(self.details['password'].encode()).decode()
      self.db = connect(**self.details)
      self.db.autocommit = True
      secho("Database connected successfully", fg='bright_green')
      with open('schema.sql') as schema:
        self.cur = self.db.cursor()
        self.cur.execute(schema.read())
    except ProgrammingError as err:
      if err.errno == ER_ACCESS_DENIED_ERROR:
        print("Wrong password or username")
      else:
        print(err)
