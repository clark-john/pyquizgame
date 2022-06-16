from click import secho, confirm
from db import Database
from traceback import print_exception
from utils.fernetDecoder import getFernetEncoder
from .pw_start import password_start
from utils.constants import coloramaCritical, critical, success, SQL

dat = Database()
f = getFernetEncoder()

def delete(password_needed):
	if password_needed == False:
		pass
	else:
		password_start(password_needed)
	cur = dat.db.cursor()
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
		cur.execute(SQL.delete, (choose_question_to_delete,))
		secho('Question deleted successfully', fg=success)
		dat.db.commit()
		dat.db.close()
	else:
		secho('Exiting...')