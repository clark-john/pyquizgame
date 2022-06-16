from click import confirm, secho
from pytomlpp import load, dump
from InquirerPy import prompt
from constants import settings_file

config = load(settings_file, 'r')

sections = {
  'type': 'rawlist',
  'message': 'Choose section:',
  'choices': ['Quiz','Others']
}

Others = {
  'type': 'rawlist',
  'message': 'Choose section:',
  'choices': ['reset settings']
}

Quiz_options = {
  'type': 'rawlist',
  'message': 'Choose option:',
  'choices': ['hard_mode','no_colors','no_scoreboard']
}

boolean_choices = {
  'type': 'rawlist',
  'message': 'Choose value:',
  'choices': ['true', 'false']
}

def settings_area():
  section = prompt(sections)
  if section[0] == 'Quiz':
    option = prompt(Quiz_options)
    if option[0] == 'hard_mode':
      hard_mode_bool = prompt(boolean_choices)
      if hard_mode_bool[0] == 'true':
        config['Quiz']['hard_mode'] = True
        dump(config, settings_file, 'w')
      else:
        config['Quiz']['hard_mode'] = False
        dump(config, settings_file, 'w')
    elif option[0] == 'no_colors':
      no_colors_bool = prompt(boolean_choices)
      if no_colors_bool[0] == 'true':
        config['Quiz']['no_colors'] = True
        dump(config, settings_file, 'w')
      else:
        config['Quiz']['no_colors'] = False
        dump(config, settings_file, 'w')
    elif option[0] == 'no_colors':
      no_scoreboard_bool = prompt(boolean_choices)
      if no_scoreboard_bool[0] == 'true':
        config['Quiz']['no_scoreboard'] = True
        dump(config, settings_file, 'w')
      else:
        config['Quiz']['no_scoreboard'] = False
        dump(config, settings_file, 'w')
  else:
    pr = prompt(Others)
    if pr[0] == 'reset settings':
      conf = confirm('Are you sure you want to reset settings?')
      if conf:
        options = ['hard_mode','no_colors','no_scoreboard']
        for x in options:
          config['Quiz'][x] = False
        dump(config, settings_file, 'w')
        secho('Settings reset successfully', fg='green')
      else:
        pass
    else:
      secho('Exiting...')
      exit()