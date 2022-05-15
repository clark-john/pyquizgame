from click import secho
from colorama import init
from sys import platform
from InquirerPy import prompt
from .crud.pw_start import password_start

from utils.crud.create import create
from utils.crud.read import read
from utils.crud.update import update
from utils.crud.delete import delete
from utils.crud.delete_all import delete_all_questions
from utils.constants import *
from utils.crud.danger_zone import danger_zone_prompt

# colors initialization (it depends on any platform)
if platform == 'win32':
	init()
else:
	pass

# Admin area

def admin_area():
	password_start()
	two_options_choice = prompt(Prompts.two_options)[0]
	if two_options_choice == 'CRUD Operations (Manage questions)':
		crud_choice = prompt(Prompts.crud_operations)
		crud_choice = crud_choice[0]
		if crud_choice == 'create question':
			create(0)
		elif crud_choice == 'read questions':
			read(0)
		elif crud_choice == 'update question':
			update(0)
		else:
			delete(0)
	else:
		danger_zone_prompt()
	