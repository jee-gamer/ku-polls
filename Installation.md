# Steps
1. Clone this repo into your python IDE `$ git clone https://github.com/jee-gamer/ku-polls.git KU-polls`.
2. Cd into the directory `$ cd ku-polls` or your directory name if you changed it.
3. Create a virtualenv `$ python -m venv .venv` if you haven't already.
4. Upgrade pip to be able to get the new django version `$ python -m pip install --upgrade pip`. <br>
(At the time of development pip was version 24.2)
6. Activate the virtualenv and run `$ pip install -r requirements.txt`.
7. Create your own `.env` file, view examples in `sample.env`.
8. Make migrations `$ python manage.py makemigrations`.
9. Migrate `$ python manage.py migrate`.
10. Run tests `$ python manage.py test`.

## How to run is in README.md
