# Questionnaires
This is a project that I worked on after learning Django framework. The project is a basic implementation of quizes.
A quiz is composed of:
- categories
- questions

Each category contain multiple questions. Each question is linked to a category and contains multiple answers. **_Only 1 answer is correct._**

\
\
_Steps for installation_:
1. open the terminal and create a new folder:\
`mkdir <new_folder>`
2. change location into this newly created folder:\
`cd <new_folder>`
3. clone the git repo into this newly created folder:\
`git clone git@github.com:bplaiasu/questionnaires.git`
4. create a virtual environment:\
`virtualenv .venv`
5. activate the virtual environment:\
`source .venv/bin/activate`
6. to be sure that the virtual environment is activated run the following command:\
`pip freeze`\
If nothing is shown than everything is ok
7. install the dependencies:\
`pip install -r requirements.txt`
8. check django version:\
`django-admin --version`
9. execute collectstatic command:\
`python manage.py collectstatic`
10. **database** For this step I choose to use a PostgreSQL database.
* connect to **psql** command prompt:\
`psql postgres`
* add password for **postgres** user - _recommend this step to be done only for development_:\
`\password postgres`
* create a database for the project. the default name is **surveys_db** but feel free to change the name:\
`CREATE DATABASE <dbname> OWNER postgres`
* check databases:\
`\l`
* quit psql command prompt:\
`\q`
11. create required tables in the database:\
`python manage.py makemigrations`\
`python manage.py migrate`
12. create a superuser for the django administration page:\
`python manage.py createsuperuser`
13. run server:\
`python manage.py runserver`