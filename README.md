# Cafe Menu
This is a repository of a python/django project of an online cafe menu💻.

this is a project that both, manager of the cafe and cusomer can use it which is so optimized because it is one application but it can be used for all users. 

This means that customers are able to see the menu of the cafe and order directly through their phones📲.

👨👩 Manager and Staff can have access 🔑 to see their sales, change the manu and availablity of a produt, the customer's order and do all the things a manager and staff needs to do.

## Titles
you can see the documantations of each part clicking on the links below:
* [Setup](#set-up)










## Setup
The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/Mohammad-R-N/Shop-Project.git
$ cd Shop-Project
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ virtualenv2 --no-site-packages env
$ source env/bin/activate
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

Once `pip` has finished downloading the dependencies:

```sh
(env)$ cd cafe
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000`.

