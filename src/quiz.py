from click import secho, option, group, Choice, launch
from quiz.admin import *
from quiz.settings import settings_area
from main import *
from pytomlpp import dump, load

@group()
def cli():
	pass
@cli.command(short_help='View something',no_args_is_help=True)
@option('--repolink', is_flag=True, help='Returns the repository link of this game.')
@option('--creator', is_flag=True, help='Returns the creator of this game.')
def view(repolink, creator):
	if repolink:
		secho('https://github.com/clark-john/pyquizgame/', fg=success)
		secho('View on browser? (y/n)', fg=yellow)
		view = input().lower()
		if view == 'y':
			launch('https://github.com/clark-john/pyquizgame/')
		else:
			secho('Exiting...')
			exit()
	elif creator:
		secho('clark-john a.k.a. Clark', fg=success)
		secho('View on browser? (y/n)', fg=yellow)
		view = input().lower()
		if view == 'y':
			launch('https://github.com/clark-john/')
		else:
			secho('Exiting...')
			exit()

@cli.command(short_help='Admin Area', help='Use this command to manage questions', no_args_is_help=True)
@option('--create-question','-c', is_flag=True, help='Create a question')
@option('--read-questions','-v', is_flag=True, help='View all questions')
@option('--update-question','-u', is_flag=True, help='Update a question')
@option('--delete-question','-d', is_flag=True, help='Delete a question')
@option('-r','--reset', is_flag=True, help='Reset password')
@option('-m', '--main', is_flag=True, help='Actual admin area')
def admin(
	read_questions, 
	create_question, 
	update_question, 
	delete_question, 
	reset, 
	main
):
	if create_question:
		add_question(1)
	elif read_questions:
		view_questions(1)
	elif update_question:
		edit_question(1)
	elif delete_question:
		remove_question(1)
	elif reset:
		reset_password()
	elif main:
		admin_area()

# loading the settings.toml file

config = load('settings.toml', 'r')

@cli.command(help='Configure pyquizgame',no_args_is_help=True)
@option('-m','--main', help='Main settings area', is_flag=True)
@option('hard_mode', '--hard-mode', help='Hard mode', metavar='BOOLEAN', type=Choice(['true','false'], case_sensitive=False))
@option('no_colors', '--no-colors', help='With or without colors', metavar='BOOLEAN', type=Choice(['true','false'], case_sensitive=False))
@option('no_scoreboard', '--no-scoreboard', help='With or without scoreboard', metavar='BOOLEAN', type=Choice(['true','false'], case_sensitive=False))
def settings(hard_mode, no_colors, no_scoreboard, main):
	if main:
		settings_area()

	elif hard_mode == 'true':
		config['Quiz']['hard_mode'] = True
		dump(config, 'settings.toml', 'w')
		secho('Hard mode set to True', fg=success)
	elif hard_mode == 'false':
		config['Quiz']['hard_mode'] = False
		dump(config, 'settings.toml', 'w')
		secho('Hard mode set to False', fg=success)

	elif no_colors == 'true':
		config['Quiz']['no_colors'] = True
		dump(config, 'settings.toml', 'w')
		secho('\'No colors\' set to True', fg=success)
	elif no_colors == 'false':
		config['Quiz']['no_colors'] = False
		dump(config, 'settings.toml', 'w')
		secho('\'No colors\' set to False', fg=success)
	
	elif no_scoreboard == 'true':
		config['Quiz']['no_scoreboard'] = True
		dump(config, 'settings.toml', 'w')
		secho('\'No scoreboard\' set to True', fg=success)
	elif no_scoreboard == 'false':
		config['Quiz']['no_scoreboard'] = False
		dump(config, 'settings.toml', 'w')
		secho('\'No scoreboard\' set to False', fg=success)

@cli.command(help='Start a game')
def start():
	main_quiz()

if __name__ == '__main__':
	cli()	
