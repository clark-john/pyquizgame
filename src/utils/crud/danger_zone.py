from getpass import getpass
from utils.fernetDecoder import getFernetEncoder
from db import Database
from utils.crud.create_pw import create_password
from utils.crud.delete_all import delete_all_questions
from InquirerPy import prompt
from utils.constants import coloramaCritical, coloramaWarn, critical, Prompts
from traceback import print_exception
from click import secho
from colorama import Fore

dat = Database()
f = getFernetEncoder()

def dangerous_zone():
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
		password = getpass("Enter your password to enter danger zone: ")
		if password != pw:
			attempt += 1
			secho('Incorrect password.', fg=critical)
			if attempt == 5:
				secho('You cannot enter danger zone.', fg='bright_red')
				exit()
			continue
		else:
			break

def danger_zone_prompt():
	dangerzone_choice = prompt(Prompts.danger_zone)
	if dangerzone_choice[0] == 'exit':
		secho('Exiting...')
		exit()
	else:
		delete_all_questions()