# Instagram Clone Backend(Django)

An Instagram clone project built with React and Django.
Take a look at the [frontend]() for this project as well.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)

## Overview

This project is an Instagram clone that replicates some of the basic features of the popular photo-sharing platform. It consists of a frontend built with React and a backend implemented with Django.

## Features

- User authentication (signup, login, logout)
- Image uploading and sharing
- Like and comment on posts
- View other user's posts on main page
- View other user's profile
- Edit your own profile
- Delete your own Posts

## Installation

To run the project locally, follow these steps:

### Backend (Django)
1. Create Virtual envronment 
    `python -m venv venv`
2. Activate Virtual Env by runing following command.
    `venv\Scripts\activate`
3. Run `pip install -r requirements.txt` to install all dependencies.
4. Set up database by running ` python manage.py migrate`.
5. Start server using `python manage.py runserver`.


## Usage 
- Open your browser and go to `http://localhost:3000` to access the React frontend.
- The Django backend will be running at `http://localhost:8000`.

## Technologies Used

- Python 
- Django and Django Rest Framework
- PostgreSQL (or your preferred database)

## Screenshots
![screen1](./screenshots/ss-welcome.png)
![screen2](./screenshots/ss-welcome2.png)
![screen3](./screenshots/ss-profile-page.png)


