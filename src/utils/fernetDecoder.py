from os import path
from cryptography.fernet import Fernet

def getFernetEncoder() -> Fernet:
  if path.exists('password.key'):
    with open('password.key', 'r') as key:
      k = key.read().encode()
      f = Fernet(k)
      return f
  else:
    with open('password.key', 'w') as key:
      k = Fernet.generate_key()
      f = Fernet(k)
      key.write(k.decode())
      return f