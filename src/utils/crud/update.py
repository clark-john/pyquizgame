from .pw_start import password_start
from db import Database
from utils.fernetDecoder import getFernetEncoder
from click import secho
from utils.constants import coloramaCritical, critical, success, b_red, question_pattern, SQL
from traceback import print_exception

dat = Database()
f = getFernetEncoder()

def update(password_needed):
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

	if question_pattern.match(q) == None:
		secho('Questions must end with a question mark.', fg='yellow')
	else:
		secho('Question updated successfully.', fg=success)
		cur.execute(SQL.update, (q, a, choose_question_to_update))
		dat.db.commit()
		dat.db.close()