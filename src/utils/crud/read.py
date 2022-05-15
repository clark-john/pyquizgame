from utils.constants import SQL
from db import Database
from utils.crud.pw_start import password_start

def read(password_needed):
  dat = Database()
  if password_needed == False:
    pass
  else:
    password_start(password_needed)
  cur = dat.db.cursor()
  questions = cur.execute(SQL.read).fetchall()
  for x in questions:
    y, z = x
    print(y+"\n\tAnswer:".expandtabs(2),z)