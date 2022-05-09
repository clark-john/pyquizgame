from click import confirm, secho
from cryptography.fernet import Fernet
from getpass import getpass
from re import compile
from colorama import Fore, init
from sys import platform
from os import path
from db import Database
from traceback import print_exception
from InquirerPy import prompt

# Secho color variables
success = 'bright_green'
critical = 'red'
warn = 'yellow'
yellow = warn
b_red = 'bright_red'

# Colorama variables
coloramaSuccess = Fore.GREEN
coloramaCritical = Fore.RED 
coloramaWarn = Fore.YELLOW

# crud sql statements
create = 'insert into questions (question, answer) values (?, ?);'
read = 'select question, answer from questions;'
update = 'update questions set question = ?, answer = ? where id = ?'
delete = 'delete from questions where id = ?'

# colors initialization (it depends on any platform)
if platform == 'win32':
	init()
else:
	pass

# .key file 
if path.exists('password.key'):
  with open('password.key', 'r') as key:
    k = key.read().encode()
    f = Fernet(k)
else:
  with open('password.key', 'w') as key:
    k = Fernet.generate_key()
    f = Fernet(k)
    key.write(k.decode())

# Password related functions

# create password if pw is null
def create_password():
	dat = Database()
	cur = dat.db.cursor(buffered=True)
	pw_pattern = compile('^[\w]{8,}')
	while True:
		secho('Password should contain equal or more than 8 characters.', fg='yellow', bold=True)
		new = getpass('Enter your new password: ')
		if pw_pattern.match(new) == None:
			secho("Try again", fg='bright_red')
		else:
			conf = getpass('Repeat for confirmation: ')
			if conf != new:
				secho('Passwords do not match.', fg=warn)
			else:
				new = f.encrypt(new.encode())
				new_password = new.decode()
				cur.execute('insert into quizadmin (pw, role) values (?, \'admin\')', (new_password,))
				cur.close()
				dat.db.close()
				secho('Password created successfully.', fg=success)
				exit()

# reset
def reset_password():
	dat = Database()
	cur = dat.db.cursor(buffered=True)
	pw_pattern = compile('^[\w]{8,}')
	while True:
		secho('Password should contain equal or more than 8 characters.', fg='yellow', bold=True)
		new = getpass('Enter your new password: ')
		if pw_pattern.match(new) == None:
			secho("Try again", fg='bright_red')
		else:
			conf = getpass('Repeat for confirmation: ')
			if conf != new:
				secho('Passwords do not match.', fg=warn)
			else:
				new = f.encrypt(new.encode())
				new_password = new.decode()
				cur.execute('update quizadmin set pw = ? where role = \'admin\'',(new_password,))
				cur.close()
				dat.db.close()
				secho('Password reset successfully.', fg=success)
				break

# if dangerous zone is entered
def dangerous_zone():
	dat = Database()
	cur = dat.db.cursor(buffered=True)
	cur.execute('select pw from quizadmin')
	password_check = cur.fetchone()
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
	
# confirmation for deleting questions

def confirmation_of_deleting_all_questions():
	pass
 
# startup
def password_start():
	dat = Database()
	cur = dat.db.cursor(buffered=True)
	cur.execute('select pw from quizadmin')
	password_check = cur.fetchone()
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

# crud related functions

# create/add
def	add_question(password_needed):
	dat = Database()
	if password_needed == False:
		pass
	else:
		password_start()
	question_pattern = compile('^[\w\s]*\?$')
	cur = dat.db.cursor(buffered=True)
	secho('Creating question', fg=success, bold=True)

	q = input("Write your question: ")
	if q.lower() == 'exit':
		secho('Aborted!', fg=b_red)
		exit()
	else:
		q = q

	a = input("Write your answer: ")
	if a.lower() == 'exit':
		secho('Aborted!', fg=b_red)
		exit()
	else:
		a = a

	if question_pattern.match(q) == None:
		secho('Questions must end with a question mark.', fg=warn)
	else:
		secho('Question created successfully.', fg=success)
		cur.execute(create, (q, a))
		cur.close()
		dat.db.close()

# read/view
def view_questions(password_needed):
	dat = Database()
	print(dat.key)
	if password_needed == False:
		pass
	else:
		password_start()
	cur = dat.db.cursor(buffered=True)
	questions = cur.execute(read).fetchall()
	for x in questions:
		y, z = x
		print(y+"\n\tAnswer:".expandtabs(2),z)
	cur.close()
	dat.db.close()

# update/edit
def edit_question(password_needed):
	dat = Database()
	if password_needed == False:
		pass
	else:
		password_start()
	cur = dat.db.cursor(buffered=True)
	questions = cur.execute('select question, answer from questions;').fetchall()
	id = cur.execute('select id from questions').fetchall()
	questions_length = len(questions)
	for x, u in zip(questions, range(questions_length)):
		for w in id[u]:
			y, z = x
			print(str(w)+". "+y+"\n\tAnswer:".expandtabs(2),z)

	choose_question_to_update = input('Which question to update? (choose by number): ').lower()
	if choose_question_to_update == 'exit':
		secho('Aborted!')
		exit()
	elif not(choose_question_to_update == 'exit'):
		try:
			type(int(choose_question_to_update)) == int
		except:
			print_exception(Exception(coloramaCritical+'Invalid value'))
			exit()
		finally:
			pass
	else:
		secho('Invalid value.',fg=critical)
		exit()
	
	question_selection = cur.execute('select question from questions where id=?', (choose_question_to_update,)).fetchone()[0]
	secho('Updating this question: '+question_selection)

	q = input('Type your new question: ')
	if q.lower() == 'exit':
		secho('Aborted!', fg=b_red)
	else:
		q = q

	a = input('Type your new answer: ')
	if a.lower() == 'exit':
		secho('Aborted!', fg=b_red)
	else:
		a = a

	question_pattern = compile('^[\w\s]*\?$')
	
	if question_pattern.match(q) == None:
		secho('Questions must end with a question mark.', fg='yellow')
	else:
		secho('Question updated successfully.', fg=success)
		cur.execute(update, (q, a, choose_question_to_update))
		cur.close()
		dat.db.close()

# remove/delete
def remove_question(password_needed):
	dat = Database()
	if password_needed == False:
		pass
	else:
		password_start()
	cur = dat.db.cursor(buffered=True)
	questions = cur.execute('select question, answer from questions;').fetchall()
	id = cur.execute('select id from questions').fetchall()
	questions_length = len(questions)
	for x, u in zip(questions, range(questions_length)):
		for w in id[u]:
			y, z = x
			e = str(w)+". "+y+"\n\tAnswer: ".expandtabs(2)+z
			print(e)

	choose_question_to_delete = input('Which question to remove? (choose by number): ').lower()
	if choose_question_to_delete == 'exit':
		secho('Aborted!')
		exit()
	elif not(choose_question_to_delete == 'exit'):
		try:
			type(int(choose_question_to_delete)) == int
		except:
			print_exception(Exception(coloramaCritical+'Invalid value'))
			exit()
		finally:
			pass
	else:
		secho('Invalid value.',fg=critical)
		exit()
		
	question_selection = cur.execute('select question from questions where id=?', (choose_question_to_delete,)).fetchone()[0]
	secho('Deleting this question: '+question_selection)
	
	conf = confirm('Are you sure?')
	if conf:
		cur.execute(delete, (choose_question_to_delete,))
		secho('Question deleted successfully', fg=success)
		cur.close()
		dat.db.close()
	else:
		secho('Exiting...')

# inquirerpy 

two_options = {
	'type': 'rawlist',
	'message': 'Admin Area',
	'choices': [
		'CRUD Operations (Manage questions)',
		'Danger Zone'
	]
}

crud_operations = {
	'type':'rawlist',
	'message':'Choose any of these crud operations:',
	'choices': [
		'create question', 
		'read questions', 
		'update question', 
		'delete question'
	]
}

danger_zone = {
	'type':'rawlist',
	'message':'Danger zone',
	'choices': [
		'delete all questions',
		'exit' 
	]
}

# Danger Zone

def delete_all_questions():
	dat = Database()
	cur = dat.db.cursor(buffered=True)
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
				cur.close()
				dat.db.close()
				secho('Questions delete successfully.', fg=success)
		else:
			secho('Exiting...')

# Danger zone (rawlist prompt)
def danger_zone_prompt():
	dangerzone_choice = prompt(danger_zone)
	if dangerzone_choice[0] == 'exit':
		secho('Exiting...')
		exit()
	else:
		delete_all_questions()

# Admin area

def admin_area():
	password_start()
	two_options_choice = prompt(two_options)[0]
	if two_options_choice == 'CRUD Operations (Manage questions)':
		crud_choice = prompt(crud_operations)
		crud_choice = crud_choice[0]
		if crud_choice == 'create question':
			add_question(0)
		elif crud_choice == 'read questions':
			view_questions(0)
		elif crud_choice == 'update question':
			edit_question(0)
		else:
			remove_question(0)
	else:
		danger_zone_prompt()
	