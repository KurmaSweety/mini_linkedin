#  MiniLinkedIn 

MiniLinkedIn is a community platform built with Flask, SQLAlchemy, and Bootstrap that mimics 
core features of LinkedIn — including user registration, login, profile creation/editing, posting updates,
and a responsive UI with dark/light mode.

##  Features

-  User Registration & Login (with password hashing)
-  Profile Management (headline, company, skills, education, etc.)
-  Upload Profile Picture
-  Create, Edit & Delete Posts (only by author)
-  Home Feed with all posts
-  Responsive UI with Bootstrap 5


##  Tech Stack

Frontend  --- HTML, CSS, Bootstrap5(responsive UI)

Backend   --- Flask, Jinja2

Database  --- SQLite(SQLAlchemy)

Authentication ---  Flask-Login

Deployment --- Render.com

Extra features I add this project ----  flash messages, Edit profile, Edit post, Delete post

##  Project Structure
mini_linkedin/
│
├── app.py                   # Main Flask app
├── models.py                # SQLAlchemy models
├── forms.py                 # WTForms for forms
├── templates/               # Jinja2 HTML files
│ ├── base.html
│ ├── home.html
│ ├── register.html
│ ├── login.html
│ ├── profile.html
│ ├── edit_profile.html
│ ├── create_post.html
│ ├── edit_post.html
│ ├── landing.html
│
├── static/
│ ├── css/
│ └── profile_pics/
│
├── instance/linkedin_clone.db        # SQLite database
├── requirements.txt
└── README.md

## Set Up Virtual Environment
python -m venv venv
source venv/bin/activate

## Install Requirements
pip install -r requirements.txt

If you face an error with email validation:

pip install email-validator

## Run the App
python app.py

## Future Improvements
- User-to-user messaging

- Likes & comments on posts

- Search users and posts

- Connection system (Follow/Unfollow)

- Admin dashboard

- Profile recommendation algorithm