
### Pipenv notes
- `pipenv shell`: Create and Login to virtual environment
- `pipenv shell --python 3.10` (or whatever version you're using): Create and login to a virtual environment with a specific python version.
- `pipenv --rm`: Remove virtual environment (while logged out)
- `exit`: Exit virtual environment (while logged in)
- Typically, pipenv environments are stored in your home directory.
    - Pipfile: /Users/enzolarosa/Sites/cashflow/Pipfile
    - Using /Users/enzolarosa/.pyenv/versions/3.10.0/bin/python3 (3.10.0) 
- While inside of a pipenv environment, you don't need to say `python3 or pip3 blahblahblah`. You can just write `pip <command>` or `python <command> ...`
- pip freeze —local > requirements.txt create the requirement.txt with the isntalled packages

### Markdown Notes:
- **bold**
- *italic*
- ***bold italic***
# Super Big
## Sub Big
### Sub Sub Big

### Django Notes
1. pip install django
2. `django-admin startproject config .`: Create a new Django project with a config folder inside of the current project foldler. This removes duplication in naming.
