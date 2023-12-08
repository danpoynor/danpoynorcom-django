# WIP: Dan Poynor Portfolio

## Initial steps used to create this project

<details>
  <summary>Click to expand</summary>

## Create A New Environment

Assuming you have Python 3 installed, create a new virtual environment for this project.

This will keep dependencies separate and avoid conflicts with other projects.

If Anaconda is installed, decactivate it's base environment and create a new one for this project.

```sh
# Deactivate the (base) environment if Anaconda is installed
conda deactivate
# Make sure virtualenv is installed
pip3 install virtualenv
# Create a new virtual environment
virtualenv venv
# Activate the new environment
source venv/bin/activate
```

## Install Dependencies

After you’ve created and activated a virtual environment, enter the command:

```sh
python -m pip install Django
python -m pip install python-dotenv
```

Verify that Django can be seen by Python:

```sh
python -m django --version
```

## Create A New Django Project and Run The Development Server

```sh
django-admin startproject danpoynor
cd danpoynor
python manage.py runserver
```

Visit <https://localhost:8000> in a web browser to see the Django welcome page.

## Automatic reloading of runserver

NOTE: The development server automatically reloads Python code for each request as needed. You don’t need to restart the server for code changes to take effect. However, some actions like adding files don’t trigger a restart, so you’ll have to restart the server in these cases.

---

## Create A New App

```sh
python manage.py startapp portfolio
```

## Create A New Model

Edit the models.py file to add a new models.

## Run Migrations

```sh
python manage.py migrate
```

## Create A Superuser

```sh
python manage.py createsuperuser
```

## Register The Models With The Admin

## Create Views

## Create Templates

Create a new directory called templates in the the app directory.

Create a new file called index.html in the templates directory.

Edit the index.html file to add some HTML.

## Create A URL

Edit the app urls.py file to add a new URL.

Edit the project urls.py file to include the app urls.

## Run The Development Server

```sh
python manage.py runserver
```

</details>
