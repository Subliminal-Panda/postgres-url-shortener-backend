## INTRODUCTION: BACKEND/API

- This program's backend is built in Python using Flask, Sqlite, Marshmallow and sqlalchemy.

- To generate random short URL's, a variable called saved_link is defined as ="".join([random.SystemRandom().choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for * in range(7)]) an algorithm allowing 3,521,614,606,208 unique randomly generated URL slugs.

* This algorithm takes advantage of Python's native random and string libraries.

- To prevent duplicate links, the backend performs a database search for duplicates. If a duplicate exists, it enters a while loop, re-rolling random links, until a unique link is generated. Though the odds of this happening are 62^7 per link in the database, it's always better to verify.

- To clone this repository and have a look at the code:

1.  Navigate in your preferred terminal (Windows: Command Prompt, PowerShell Linux: Bash Mac: Terminal) to the directory you would like to clone my repository to. You'll be downloading a set of files.

2.  When you're at the proper directory, run the following command:

    \$ gh repo clone Subliminal-Panda/postgres-url-shortener-backend

- If you want to run this app entirely on your own computer, you'll have to follow the steps toward the bottom, under CLONING AND RUNNING THE FRONTEND REPOSITORY as well as CLONING AND RUNNING THE BACKEND REPOSITORY.

## INTRODUCTION: USING THE APP

- This program is reasonably user-friendly, so it shouldn't be too tough to dive right in!

- I recommend running it inside codesandbox for the sake of simplicity. To get to it (if you're not in codesandbox already) navigate to the following URL:

https://codesandbox.io/s/beautiful-noyce-j499o?

\*If you'd like to try this application outside codesandbox, skip down to CLONING AND RUNNING THE FRONTEND REPOSITORY.

- To enter a URL, click the input field titled "Enter a new URL:" and enter your desired destination URL.

- It doesn't matter if it starts with a prefix of http://, https://, www., or even no prefix whatsoever! just make sure the URL is spelled correctly.

- If you would like to create your own custom short link, enter your desired link name in the "Custom short link (optional): input field. You can use most special characters, but no spaces. Just keep in mind, if you write a short link that isn't short, it will overflow the display area. (It will still work, it just won't look very pretty.)

- Click the green "Submit Url" button. The backend will automatically recognize whether you've created a custom short link. If not, it will generate a random 10 character link instead.

- It might take just a moment to update the list with your new URL and Short Link (free databases are prioritized last... sad.)

- Once your link appears, you can click either the URL itself (to the left) or the short link (on the right) to visit the URL you entered! It's magical!

- To delete a URL and its corresponding Short Link, just click the pink/red "Delete Link" button to the right, on the same row.

## REQUIREMENTS: CODE SANDBOX

- This module (in codesandbox) requires the following dependencies, which should be pre-loaded:

* react
* react-dom
* react-scripts

## CLONING AND RUNNING THE FRONTEND REPOSITORY

- If you'd like to try this application outside codesandbox:

1.  Navigate in your preferred terminal (Windows: Command Prompt, PowerShell Linux: Bash Mac: Terminal) to the directory you would like to clone my repository to. You'll be downloading a set of files.

2.  When you're at the proper directory, run the following command:

    \$ gh repo clone Subliminal-Panda/postgres-url-shortener-frontend

3.  If you don't have npm already, install it at the following link:

https://github.com/npm/npm/archive/refs/tags/v5.2.0.zip

4.  Then boot up the app on your computer:

    $ npm i
    $ npm start

- That should do it! The backend is always running, so you don't need to do anything special for that. However, if you would like to run this entirely on your own machine (in a test environment) you'll have to do the following:

## CLONING AND RUNNING THE BACKEND REPOSITORY

1.  Install python, if you don't already have it:

    https://www.python.org/downloads/

2.  Clone the backend repository, if you haven't already- go to a directory where you're comfortable cloning an app, then run this in your terminal:

        $ gh repo clone Subliminal-Panda/postgres-url-shortener-backend

3.  Install PIP via the terminal, if you don't already have it:

        $ python -m ensurepip --upgrade

4.  Install Pipenv:

        $ pip install pipenv

5.  Enter a pipenv shell environment:

        $ pipenv shell

6.  Install the following dependencies within your pipenv shell environment:

        $ pipenv install flask flask_sqlalchemy flask_marshmallow flask_cors psycopg2 gunicorn

7.  To change the db to your local environment, delete line 21 in app.py, then remove the "#" symbol before the next line to change it to active code.

8.  Start python:

        $ pipenv run python

9.  Run the following commands using Python:

        > from app import db
        > db.create_all()

10. If that doesn't return any errors, your test environment database is created! Now let's get it running:

        $ pipenv run python app.py

11. Alright, the backend is running on your local machine. Next, if you haven't already, follow the instructions in CLONING THE FRONTEND REPOSITORY.

12. finally, in your cloned front-end repository, in the Home.js file, add "//" before line 8 to change it to a comment, and delete the "//" on line 7 to turn it into active code. If your python cloned application isn't running on "http://127.0.0.1:5000" you will need to replace this with wherever it is running.

13. Alright, you've got a working backend and frontend running on your computer! Baddabing!
