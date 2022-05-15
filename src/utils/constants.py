from colorama import Fore
from re import compile

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
reset = Fore.RESET

# regex patterns
pw_pattern = compile('^[\\w]{8,}')
question_pattern = compile('^[\\w\\s]*\\?$')

# crud sql statements
class SQL:
	create = 'insert into questions (question, answer) values (?, ?);'
	read = 'select question, answer from questions;'
	update = 'update questions set question = ?, answer = ? where id = ?'
	delete = 'delete from questions where id = ?'

# prompts
class Prompts:
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