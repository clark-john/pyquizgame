from getpass import getpass
from click import secho
from utils.constants import warn, pw_pattern, success
from db import Database
from utils.fernetDecoder import getFernetEncoder

dat = Database()
f = getFernetEncoder()

def create_password():
	cur = dat.db.cursor()
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
				dat.db.commit()
				dat.db.close()
				secho('Password created successfully.', fg=success)
				exit()