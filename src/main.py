from random import choice
from click import secho
from db import Database
from time import sleep
from pytomlpp import load

settings = load('settings.toml', 'r')

def main_quiz():
  # Click's secho Variables
  success = 'bright_green'
  critical = 'red'
  warn = 'yellow'

  secho('Starting quiz...')
  secho('Fetching questions...')

  dat = Database()
  cur = dat.db.cursor()
  fetch_id = 'select id from questions'
  questions = cur.execute('select question from questions;').fetchall()
  questions_length = len(questions)
  ids = cur.execute(fetch_id).fetchall()

  if questions_length == 0:
    secho('You don\'t have any questions yet.\nCreate some with \"python quiz.py admin --create-question\"', fg=warn)
    exit()
  elif questions_length <= 2:
    secho('You can\'t have two or less questions.', fg=warn)
    exit()

  ids_list = []
  for x in ids:
    ids_list.append(x[0])
    pass

  query = 'select question, answer from questions where id = ?'

  secho('Let\'s start.')

  get_hard_mode_setting = settings['Quiz']['hard_mode']
  get_no_colors_setting = settings['Quiz']['no_colors']
  get_no_scoreboard_setting = settings['Quiz']['no_scoreboard']

  if get_no_colors_setting:
    success = critical = None
  else:
    pass

  score = 0
  while True:
    if questions_length > 2:
      random_choice = choice(ids_list)
      qna = cur.execute(query, (random_choice,)).fetchone()
      q = qna[0]
      a = qna[1]
      sleep(0.5)
      print(q)
      def empty_list_condition():
        if ids_list == []:
          secho('Thanks for playing', fg=success)
          if get_no_scoreboard_setting:
            pass
          else:
            secho(f'You scored {score} over {questions_length}', fg='cyan')
          exit()
        else:
          pass
      answer = input()
      if answer == a:
        secho('correct',fg=success)
        ids_list.pop(ids_list.index(random_choice))
        score += 1
        empty_list_condition()
        continue
      else:
        if not get_hard_mode_setting:
          secho('wrong',fg=critical)
          ids_list.pop(ids_list.index(random_choice))
          empty_list_condition()
          continue
        else:
          secho('You got the wrong answer. Exiting...', fg=critical)
          exit()
    else:
      pass
    
    
