# Dan Poynor Portfolio

Personal portfolio website for danpoynor.com built in Django.

Notes below are primarily for my own reference.

## Some Notable Django Features and Frequently Used Commands

- [Django Models](https://docs.djangoproject.com/en/5.0/#the-model-layer)
- [Django Views](https://docs.djangoproject.com/en/5.0/#the-view-layer)
- [Django Templates](https://docs.djangoproject.com/en/5.0/#the-template-layer)
- [Django Custom Tags and Filters](https://docs.djangoproject.com/en/5.0/howto/custom-template-tags/)
- [Django Admin](https://docs.djangoproject.com/en/5.0/#the-admin)
- [Custom Django Management Commands](https://docs.djangoproject.com/en/5.0/howto/custom-management-commands/)
- [Django urlpatterns](https://docs.djangoproject.com/en/5.0/topics/http/urls/)
- [Django Unit Tests](https://docs.djangoproject.com/en/5.0/topics/testing/)
- [Django Tests Integration with Coverage](https://docs.djangoproject.com/en/5.0/topics/testing/advanced/#integration-with-coverage-py)
- [Django Pagination](https://docs.djangoproject.com/en/5.0/topics/pagination/)
- [Django Performance and Optimization](https://docs.djangoproject.com/en/5.0/topics/performance/)
- [Django Settings](https://docs.djangoproject.com/en/5.0/topics/settings/)
- Django Static Files
- [SQLite database in Django](https://docs.djangoproject.com/en/5.0/ref/databases/#sqlite-notes)
- [makemigrations](https://docs.djangoproject.com/en/5.0/ref/django-admin/#makemigrations) and [migrate](https://docs.djangoproject.com/en/5.0/ref/django-admin/#migrate) management commands
- [dumpdata](https://docs.djangoproject.com/en/5.0/ref/django-admin/#dumpdata) and [loaddata](https://docs.djangoproject.com/en/5.0/ref/django-admin/#loaddata) management commands
- [test](https://docs.djangoproject.com/en/5.0/ref/django-admin/#test) management command

Referenced more in the [Django Features](https://docs.djangoproject.com/en/5.0/#the-template-layer) section of the Django documentation.

[Django How-To's](https://docs.djangoproject.com/en/5.0/howto/)

## Some Notable `pip` Packages Used

- [Django](https://docs.djangoproject.com/en/5.0/topics/install/): Python web framework
- [python-dotenv](https://pypi.org/project/python-dotenv/): Python library used to read key-value pairs from a `.env` environment file
- [`django-debug-toolbar`](https://django-debug-toolbar.readthedocs.io/en/latest/): Django library used to debug code
- [`django-requests-debug-toolbar`](https://pypi.org/project/django-requests-debug-toolbar/): Django library used to debug requests (not working?)
- [`django-flatblocks`](https://github.com/cartwheelweb/django-flatblocks): Django library used to create small text-blocks on websites, similar to Django's own flatpages.
- [`djlint`](https://www.djlint.com/): Django library used to lint and format Django templates
- [`phpserialize`](https://pypi.org/project/phpserialize/): Python library used to serialize PHP data. Used by scripts in this project to convert WordPress data to Python data.
- [`inflect`](https://github.com/jaraco/inflect): Python library used to convert plural nouns to singular
- [`coverage`](https://coverage.readthedocs.io/en/latest/): Python library used to measure code coverage.
- [`django.contrib.sitemaps`](https://docs.djangoproject.com/en/5.0/ref/contrib/sitemaps/): Django library used to generate sitemaps.
- [`whitenoise`](http://whitenoise.evans.io/en/stable/): serve static files when Debug is False and after running `python manage.py collectstatic`.
- [`jango_minify_html`](https://pypi.org/project/django-minify-html/): Django library to minify HTML. Uses [minify-html](https://github.com/wilsonzlin/minify-html), the extremely fast HTML + JS + CSS minifier, with Django.
- [bakery](https://palewi.re/docs/django-bakery/): Django helpers for baking your Django site out as flat files.

## Other Features Include

- [SQLite](https://www.sqlite.org/): Database used in development
- [SASS CSS](https://sass-lang.com/install/): Command line SASS is used in this project to generate the CSS. Dart Sass installed using `brew` on Mac.
- [Google Fonts](https://fonts.google.com/)
- Google Analytics

## Initial Steps Used To Create This Project From Scratch

<details>
  <summary>Click to expand</summary>

### Create A New Environment

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

### Install Dependencies

After you’ve created and activated a virtual environment, enter the command:

```sh
python -m pip install Django
python -m pip install python-dotenv
```

Verify that Django can be seen by Python:

```sh
python -m django --version
```

### Create A New Django Project and Run The Development Server

```sh
django-admin startproject danpoynor
cd danpoynor
python manage.py runserver
```

Visit <https://localhost:8000> in a web browser to see the Django welcome page.

### Automatic reloading of runserver

NOTE: The development server automatically reloads Python code for each request as needed. You don’t need to restart the server for code changes to take effect. However, some actions like adding files don’t trigger a restart, so you’ll have to restart the server in these cases.

---

### Create A New App

```sh
python manage.py startapp portfolio
```

### Create A New Model

Edit the models.py file to add a new models.

### Run Migrations

```sh
python manage.py migrate
```

### Create A Superuser

```sh
python manage.py createsuperuser
```

### Register The Models With The Admin

### Create Views

### Create Templates

Create a new directory called templates in the the app directory.

Create a new file called index.html in the templates directory.

Edit the index.html file to add some HTML.

### Create A URL

Edit the app urls.py file to add a new URL.

Edit the project urls.py file to include the app urls.

### Run The Development Server

```sh
python manage.py runserver
```

</details>

## Use SASS CSS in Django

<details>
  <summary>Click to expand</summary>

Command line SASS is used in this project to generate the CSS.

To compile the SASS files from `assets/scss/index.scss` into the CSS file `static/css/styles.css`, `cd` into the `portfolio` app directory and run SASS watch command using:

```sh
sass --watch assets/scss/index.scss:static/css/styles.css
```

You'll have to refresh the browser to see the changes.

When ready to deploy, run the SASS build command using:

```sh
sass assets/scss/index.scss:static/css/styles.css --style compressed
```

</details>

## PIP Notes

<details>
  <summary>Click to expand</summary>

### Uninstall a package

```sh
pip uninstall <package_name>
```

### List installed packages

```sh
pip list
```

### List outdated packages

```sh
pip list --outdated
```

### Upgrade a package

```sh
pip install --upgrade <package_name>
```

### Install a specific version of a package

```sh
pip install <package_name>==<version_number>
```

### Install a package from a requirements file

```sh
pip install -r requirements.txt
```

### Create a requirements file

```sh
pip freeze > requirements.txt
```

</details>

## Run unit tests

There are 146 passing unit tests so far located in the `tests/` directory.

NOTE: I couldn't figure out how to run tests in VS Code, so I run them from the command line for now.

<details>
  <summary>Click to expand</summary>

### Run all tests

```sh
python manage.py test --verbosity=2
```

### Run a specific test suite

```sh
python manage.py test portfolio.tests.test_models
python manage.py test portfolio.tests.test_views
python manage.py test portfolio.tests.test_urls
```

or run one specific test in a test file

```sh
python manage.py test portfolio.tests.test_models.TestModelName
```

### Run a specific test method

```sh
python manage.py test portfolio.tests.test_models.TestModelName.test_method_name
```

</details>

## Run code coverage

<details>
  <summary>Click to expand</summary>

### Install coverage

```sh
pip install coverage
```

### Run coverage in Django

```sh
coverage run --source='.' manage.py test
```

Or for a specific app

```sh
coverage run --source='.' manage.py test portfolio
```

Then view the report

```sh
coverage report
```

or view the report in HTML

```sh
coverage html
```

or output the report to and XML file

```show
coverage xml
```

### View coverage in VS Code

Install the [Coverage Gutters](https://marketplace.visualstudio.com/items?itemName=ryanluker.vscode-coverage-gutters) extension.

Then click the 'Watch' icon in the bottom status bar of the VS Code window and files with coverage will be highlighted in the editor gutter.

## Use `linkchecker` to crawl the site and check for broken links

<details>
  <summary>Click to expand</summary>

#### Install `linkchecker` if not already installed

```sh
pip install linkchecker
```

#### Run `linkchecker`

```sh
linkchecker http://localhost:8000 --check-extern
```

or to do a slower crawl to account for latency and ouput errors to a file use:

```sh
linkchecker --timeout=20 --threads=1 -F text/linkchecker_output.txt http://localhost:8000
```

Note the `--check-extern` option tells `linkchecker` to check external links as well as internal links.

To output a file with the results of the `linkchecker` run, use the `-F` option followed by the path to the file to output to. For example:

```sh
linkchecker --timeout=5 --ignore-url='.*\.swf$' -F text/linkchecker_output.txt http://localhost:8000  
```

If you want to check only HTML pages and ignore other resources, you can use the `--no-warnings` option. This will make `linkchecker` faster and reduce the number of URLs checked. However, it will also make `linkchecker` less thorough, as it won't check if your CSS, JavaScript, images, and other resources are loading correctly.

`linkchecker` will crawl all pages of your website and check all links on each page. It will print a report to the console, showing any broken links it found.

Also, please be aware that `linkchecker` can generate a lot of traffic and may be blocked by some websites. Always use it responsibly and respect the terms of service of the websites you're checking.

#### Other options

Increase the timeout that `linkchecker` uses when accessing URLs by using the `--timeout` option followed by the number of seconds to wait. For example, to wait up to 10 seconds for a response, you can use:

```sh
linkchecker --timeout=10 http://localhost:8000
```

**Ignore URLs**: If there are certain URLs you want `linkchecker` to ignore, you can use the `-i` or `--ignore-url` option followed by a regular expression that matches the URLs to ignore. For example, to ignore all URLs that contain `example.com`, you can use `-i example.com`.

**Set the User-Agent**: Some websites may block or limit requests from `linkchecker` because it identifies itself as a bot. You can change the User-Agent string that `linkchecker` sends with the `-u` or `--user-agent` option. For example, to identify as a regular Chrome browser, you can use `-u "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3`".

**Limit the Depth**: By default, `linkchecker` follows all links it finds, no matter how deep. You can limit the depth of the crawl with the `-r` or `--recursion-level` option followed by a number. For example, to only check links on the homepage and one level deep, you can use `-r 2`.

**Check Only Certain File Types**: If you're only interested in certain types of files, you can use the `--file-extension` option followed by a comma-separated list of file extensions. For example, to check only HTML and CSS files, you can use `--file-extension=html,css`.

Use `linkchecker --list-plugins` to see a list of all available plugins.

`linkchecker -h` or `linkchecker --help` will show a list of all available options.

</details>

## Notes on Exporting Static Website Files from Django

<details>
  <summary>Click to expand</summary>

### Package Options for Exporting Static Files from Django

#### Static Files

- [The staticfiles app](https://docs.djangoproject.com/en/5.0/ref/contrib/staticfiles/)
- [How to manage static files (e.g. images, JavaScript, CSS)](https://docs.djangoproject.com/en/5.0/howto/static-files/)
- - [Deploying static files](https://docs.djangoproject.com/en/5.0/howto/static-files/deployment/)

---

#### Exporting Pages

- [django-compressor](https://django-compressor.readthedocs.io/en/stable/), [django-compressor on GitHub](https://github.com/django-compressor/django-compressor)
- [django-pipeline](https://django-pipeline.readthedocs.io/en/latest/), [django-pipeline on GitHub](https://github.com/jazzband/django-pipeline)
- [django-bakery](https://django-bakery.readthedocs.io/en/latest/), [django-bakery on GitHub](https://github.com/palewire/django-bakery)
- [django-static-precompiler](https://django-static-precompiler.readthedocs.io/en/stable/), [django-static-precompiler on GitHub](https://github.com/andreyfedoseev/django-static-precompiler)
- [django-staticfiles](https://docs.djangoproject.com/en/3.1/ref/contrib/staticfiles/)

</details>

## To Do

<details>
  <summary>Click to expand</summary>

- [ ] Add a favicon
- [ ] Add a robots.txt file
- [ ] Add a sitemap.xml file
- [ ] Add a humans.txt file
- [ ] Populate MediaType column in Project Items table
- [ ] Filter ProjectItems by MediaType on MediaTypeProjectsListView page, possible other places
- [ ] May need to refactor schema so taxonomies are associated with ProjectItems instead of Projects
