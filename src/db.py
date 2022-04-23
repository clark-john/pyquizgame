from psycopg2 import connect
from json import load
from cryptography.fernet import Fernet

class Database:
  with open('login.json', 'r') as j:
    login = load(j)

  password_str = login['password']

  dbname = login['dbname']
  user = login['user']
  port = login['port']
  password = password_str.encode()

  with open('db_password.key', 'r') as k:
    key = k.read().encode()
  f = Fernet(key)

  def __init__(self): 
    try:
      pw = self.f.decrypt(self.password)
      password = pw.decode()
      self.db = connect(f"dbname={self.dbname} user={self.user} port={self.port} password={password}")
      self.db.autocommit = True
      cur = self.db.cursor()
      with open('schema.sql', 'r') as schema:
        cur.execute(schema.read())
    except:
      raise Exception("An error occured.")
