# KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](TODO-write-URL-of-the-django-tutorial-here), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

[![Python unittest](https://github.com/jee-gamer/ku-polls/actions/workflows/python-app.yml/badge.svg)](https://github.com/jee-gamer/ku-polls/actions/workflows/python-app.yml)

## Purpose
This application is a web application for conducting polls and surveys that can specifiy start and end dates. It is an easy to use app that is able to submit a choice on poll items, and view or modify one's choice any time during a polling period.

## UI
![image](https://github.com/user-attachments/assets/4e294644-5540-467b-b511-47530908e6d6)


## Installation

- [Installation file](../../blob/main/Installation.md)

## Running the Application

1. Go into directory ku-polls `$ cd ku-polls`
2. Make sure you already did `makemigrations` and `migrate` steps in `Installation.md`
3. Run the server on your localhost `$ python manage.py runserver`

## Demo users

| user | password |
|-------|--------|
| admin | ok |
| demo1 | hackme11 |
| demo2 | hackme22 |
| demo3 | hackme33 |

### How to load Demo users
run `$ python manage.py loaddata data/users.json`

### How to load sample question, choices and votes
run `$ python manage.py loaddata data/polls-v4.json data/votes-v4.json`

## How to go into Admin website
Go to `your_url/admin/` instead of the normal `your_url/polls/` <br>
If you run on localhost `your_url` will be `http://127.0.0.1:8000/`
or `localhost:8000`

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [How to use](../../wiki/How%20to%20use)

- [Vision Statement](../../wiki/Vision)
- [Requirements](../../wiki/Requirements)
- [Project Plan](../../wiki/Project%20Plan)
- [Domain Model](../../wiki/Domain%20Model)
