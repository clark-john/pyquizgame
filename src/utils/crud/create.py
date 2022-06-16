from click import secho
from utils.constants import success, b_red, question_pattern, warn, SQL
from utils.crud.pw_start import password_start
from db import Database

def	create(password_needed):
	# db should be Database()
	dat = Database()
	if password_needed == False:
		pass
	else:
		password_start(password_needed)
	
	cur = dat.db.cursor()
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
		cur.execute(SQL.create, (q, a))
		dat.db.commit()
		dat.db.close()