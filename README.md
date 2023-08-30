# 💻 Cafe Menu
Welcome to the online cafe menu project

## Titles 📋

you can see the documantations of each part clicking on the links below:
* [About Project](about-project)
  
* [Setup](#setup)
  
  - [Installation](#installation)
    
* [Running The Project](#running-the-project)
  

## About Project

This is a repository of a python/django project of an online cafe menu.

this is a web appliacation that both, manager of the cafe and cusomer can use it which is so optimized because it is one application but it can be used for all users ☺️. 

This means that customers are able to see the menu of the cafe and order directly through their phones 📲.

👨👩 Manager and Staff can have access 🔑 to see their sales, change the manu and availablity of a produt, the customer's order 🛒 and do all the things a manager and staff needs to do.

## Setup

Before installation make sure you have the prerequisites mentioned below ✅:
 - GITHUB
 - PYTHON
 - PIP

   
### Installation

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Mohammad-R-N/Shop-Project.git
$ cd Shop-Project
```

change the directory(cd)

```sh
$ cd Shop-Project
```

Create a virtual environment to install dependencies in:

```sh
$ python3 -m venv env
```
 Activate the  virtual environment
 
For Mac/Linux:

```sh
$ source env/bin/activate
```

For Windows:

```sh
env\Scripts\activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```

Note the `(env)` in front of the prompt. This indicates that this terminal.

Make migrations: 

```sh
(env)$ python manage.py makemigrations
(env)$ python manage.py migrate
```
Create an account for admin:

```sh
python manage.py createsuperuser
```
### Running The Project
Once `pip` has finished downloading the dependencies:

change the directory(cd)

```sh
(env)$ cd cafe
```

Run the project

```sh
(env)$ python manage.py runserver
```

And navigate to `http://127.0.0.1:8000`.

To access the admin panel, go to http://localhost:8000/admin and log in using admin account you created earlier.
