from db import Database
from utils.fernetDecoder import getFernetEncoder
from utils.crud.create_pw import create_password
from utils.constants import coloramaCritical, coloramaWarn, success, critical
from click import secho, confirm
from traceback import print_exception
from getpass import getpass
from colorama import Fore

dat = Database()
f = getFernetEncoder()

def delete_all_questions():
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
		print_exception(Exception(coloramaCritical+'It looks like your token has been f\'ed up. Did you delete the .key file?'+coloramaWarn+"\n"+"To fix this: Reset your password by typing \"py quiz.py --admin reset\""+Fore.RESET))
		raise SystemExit
	while True:
		conf = confirm('Are you sure you want to delete all questions?')
		if conf:
			password = getpass("Enter your password: ")
			if password != pw:
				attempt += 1
				secho('Incorrect password.', fg=critical)
				if attempt == 5:
					secho('Try again to remember your password.', fg='bright_red')
					exit()
				continue
			else:
				cur.execute('drop table questions')
				dat.db.commit()
				dat.db.close()
				secho('Questions deleted successfully.', fg=success)
		else:
			secho('Exiting...')