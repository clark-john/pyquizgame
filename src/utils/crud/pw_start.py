from utils.constants import coloramaCritical, critical, coloramaWarn, reset
from getpass import getpass
from traceback import print_exception
from click import secho
from .create_pw import create_password
from db import Database
from utils.fernetDecoder import getFernetEncoder

dat = Database()
f = getFernetEncoder()

def password_start(password_needed):
	if password_needed:
		cur = dat.db.cursor()
		password_check = cur.execute('select pw from quizadmin').fetchone()
		if password_check == None:
			create_password()
		else:
			password_check = password_check[0]
		attempt = 0
		try:
			pw = f.decrypt(password_check.encode())
			pw = pw.decode()
		except:
			print_exception(Exception(coloramaCritical+'It looks like your token has been f\'ed up. Did you delete the .key file?'+coloramaWarn+"\n"+"To fix this: Reset your password by typing \"py quiz.py --admin reset\""+reset))
			raise SystemExit
		while True:
			password = getpass("Enter your password: ")
			if password != pw:
				attempt += 1
				secho('Incorrect password.', fg=critical)
				if attempt == 5:
					secho('Try again to remember your password.', fg='bright_red')
					exit()
				continue
			else:
				break
	else:
		pass