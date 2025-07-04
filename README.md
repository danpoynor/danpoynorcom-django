# DanPoynor.com Portfolio Website Built with Django

Django is used as the CMS locally, SQLite for the database, and SASS for CSS. Then `wget` is used to crawl  a list of links from `http://localhost:8000/sitemap.xml` and generate static `.html` files to deploy to a production site, such as GitHub Pages.

Django is considered a "batteries included" web framework, meaning it comes with a lot of features out of the box. It's a great choice for building web applications, and it's also a good choice for building static websites.  IAnd it is especially well-suited for building complex web applications that require a lot of features.

Included features are:

- Built-in **object-relational mapper** (ORM) that makes it easy to interact with databases.
- Built-in **admin interface** that makes it easy to manage content.
- Powerful **URL routing system** that makes it easy to create clean, SEO-friendly URLs.
- A **template system** that makes it easy to create reusable HTML templates.
- Powerful **form system** that makes it easy to create and validate forms.
- Built-in **testing framework** that makes it easy to write and run tests.
- Built-in **security features** such as cross-site scripting (XSS), cross-site request forgery (CSRF), and SQL injection protection.
- Robust **authentication and authorization system**.
- Powerful **caching system** that makes it easy to cache content and improve performance.
- Built-in **internationalization and localization system** that makes it easy to create multilingual websites.
- A built-in **web server** that makes it easy to develop and test web applications locally.
- Has a **massive ecosystem of third-party packages** that make it easy to add new features to web application.
- **Large community of developers** that make it easy to get help and find resources.

Notes below are primarily for my own reference.

## Quick Start

Note: This repo is about 1.08 GB in size and may take a while to download.

Clone this repo, `cd` into the project root directory, install dependencies using `pip`, `source` the virtual environment, and run the development server:

```sh
git clone https://github.com/danpoynor/danpoynorcom-django.git
cd danpoynorcom-django/danpoynorcom
pip install -r requirements.txt
source ../venv/bin/activate
python manage.py runserver
```

You should then be able to visit <http://localhost:8000> in a web browser to see the home page.

## Notable Django Features, Commands, and Packages Used

<details>
  <summary>Click to expand</summary>

### Some Notable Django Features and Frequently Used Commands

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

### Some Notable `pip` Packages Used

- [Django](https://docs.djangoproject.com/en/5.0/topics/install/): Python web framework
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): Python library used to read key-value pairs from a `.env` environment file.
- [`django-extensions`](https://pypi.org/project/django-extensions/): Collection of custom extensions for the Django Framework. Example commands:
  - `python manage.py validate_templates`: Validates Django template syntax.
  - `python manage.py show_urls`: Displays all of the url matching routes for the project.
  - `python manage.py generate_password [--length=<length>]`: Generates a random password.
  - `python manage.py print_settings`: Prints all of the settings for the project.
  - `python manage.py notes`: Prints all TODO, FIXME, and XXX comments in the project.
  - `python manage.py pipchecker`: Scan pip requirement files for out-of-date packages (or just use `pip list --outdated` instead).
  - Database Model Extensions: Implements commonly used patterns like holding the model’s creation and last modification dates: `class MyModel(TitleSlugDescriptionModel, TimeStampedModel, ActivatorModel, models.Model)`
- [`django-debug-toolbar`](https://django-debug-toolbar.readthedocs.io/en/latest/): Django library used to debug code.
- [`django-requests-debug-toolbar`](https://pypi.org/project/django-requests-debug-toolbar/): Django library used to debug requests (not working?).
- [`django-flatblocks`](https://github.com/cartwheelweb/django-flatblocks): Django library used to create small text-blocks on websites, similar to Django's own flatpages (Unused).
- [`djlint`](https://www.djlint.com/): Django library used to lint and format Django templates
- [`phpserialize`](https://pypi.org/project/phpserialize/): Python library used to serialize PHP data. Used by scripts in this project to convert WordPress data to Python data.
- [`inflect`](https://github.com/jaraco/inflect): Python library used to convert plural nouns to singular.
- [`coverage`](https://coverage.readthedocs.io/en/latest/): Python library used to measure code coverage.
- [`django.contrib.sitemaps`](https://docs.djangoproject.com/en/5.0/ref/contrib/sitemaps/): Django library used to generate sitemaps.
- [`django_minify_html`](https://pypi.org/project/django-minify-html/): Django library to minify HTML. Uses [minify-html](https://github.com/wilsonzlin/minify-html), the extremely fast HTML + JS + CSS minifier, with Django. Note that responses are minified even when DEBUG is True. This is recommended because HTML minification can reveal bugs in your templates, so it’s best to always work with your HTML as it will appear in production. Minified HTML is hard to read with “View Source” - it’s best to rely on the inspector in your browser’s developer tools.
- [django-adminactions](https://django-adminactions.readthedocs.io/en/latest/index.html): Used for bulk actions in the Django admin.

Other packages resources to consider using for additional feature additions:

- <https://github.com/andrewp-as-is/django-most-used-packages>
- <https://djangopackages.org/>

### Other Features Include

- [SQLite](https://www.sqlite.org/): Database used in development
- [SASS CSS](https://sass-lang.com/install/): Command line SASS is used in this project to generate the CSS. Dart Sass installed using `brew` on Mac.
- [Google Fonts](https://fonts.google.com/)
- Google Analytics

</details>

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

To compile the SASS files from `portfolio/assets/scss/index.scss` into the CSS file `portfolio/static/portfolio/styles.css`, `cd` into the project `danpoynorcom` directory and run SASS watch command using:

```sh
sass --watch portfolio/assets/scss/index.scss:portfolio/static/portfolio/styles.css
```

You'll have to refresh the browser to see the changes.

When ready to deploy, run the SASS build command using:

```sh
sass --watch portfolio/assets/scss/index.scss:portfolio/static/portfolio/styles.css --style=compressed --no-source-map
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

There are 144 unit tests written so far in the `tests/` directory. Eight Project model tests are skipped after I added the custom managers to the models and should be update sometime.

NOTE: Perhaps because of this projects file structure, I couldn't get tests to run in VS Code Testing panel, so I just run them from the command line.

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

Run tests with warnings

```sh
python -Wa manage.py test portfolio
```

The `-Wa` flag tells Python to display deprecation warnings. Django, like many other Python libraries, uses these warnings to flag when features are going away. It also might flag areas in your code that aren’t strictly wrong but could benefit from a better implementation.

### Other test options include

- `--debug-mode`: This may help troubleshoot test failures.
- `--failfast`: Stops running tests and reports the failure immediately after a test fails.
- `--keepdb`: This option keeps the test database between test runs. This can be useful if you want to run tests faster.

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

Or to account for some occasional latency do a slower crawl and output errors to a file use:

```sh
linkchecker --timeout=20 --threads=1 -F text/linkchecker_output.log http://localhost:8000
```

Note the `--check-extern` option tells `linkchecker` to check external links as well as internal links.

To output a file with the results of the `linkchecker` run, use the `-F` option followed by the path to the file to output to. For example:

```sh
linkchecker --timeout=30 --ignore-url='.*\.swf$' -F text/linkchecker_output.log http://localhost:8000  
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

After testing Bakery and other Django static site generators, I settled on using `wget` to generate the static files for this project. Using `wget` I'm able to capture the paginated pages as needed.

#### Use `wget` To Generate Static Files

##### Setup

Install `wget` if not already installed.

```sh
brew install wget
```

Prep Django for static file export:

- Set `DJANGO_DEBUG=False` in `.env`. (NOTE: I'm not sure if this is necessary anymore)
- Minify SASS using `sass assets/scss/index.scss:static/portfolio/styles.css --style=compressed --no-source-map`
- - In `settings.py` disable the `django-debug-toolbar` by commenting out the `DEBUG_TOOLBAR_CONFIG` setting.

```python
DEBUG_TOOLBAR_CONFIG = {
    # "SHOW_TOOLBAR_CALLBACK": show_toolbar,
    'SHOW_TOOLBAR_CALLBACK': lambda r: False,  # Disables the debug toolbar
}
```

##### Usage

`-N`(or `--timestamping`): Tells `wget` to only download files that are newer than the local copies
`--recursive`: download the entire website.
`--no-clobber`: don't overwrite any existing files (useful for updating your local copy).
`--page-requisites`: download all the files that are necessary to properly display a given HTML page (including images and stylesheets).
`--html-extension`: save files with the `.html` extension.
`--convert-links`: convert all links so that they work offline.
`--restrict-file-names=windows`: modify filenames so that they will work in Windows as well (converts a colon to a plus sign for example).
`--domains localhost`: don't follow links outside of the specified domain.
`--no-parent`: don't follow links outside of the directory hierarchy that the starting URL specifies.

To download files to your current directory, use:

```sh
wget -N --recursive --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains localhost --no-parent http://localhost:8000/
```

The URL to start downloading from should be the last argument in the command.

Note: The --domains option expects a domain name, not a URL. You should remove http:// from the --domains option.

###### The `--mirror` Option

The --mirror option in wget is a shortcut for enabling several options that are useful for mirroring a website. Specifically, it's equivalent to -r -N -l inf --no-remove-listing.

Here's what each of these options does:

- `-r` or `--recursive`: This option tells `wget` to follow links and download pages recursively.
- `-N` or `--timestamping`: This option tells `wget` to only download files that are newer than the local copies. It's useful for updating your local copy of the website without re-downloading everything.
- `-l inf` or `--level=inf`: This option sets the maximum recursion depth to infinite, meaning `wget` will follow links indefinitely. B**y default, `wget` only follows links up to 5 levels deep**.
- `--no-remove-listing`: This option prevents `wget` from removing the temporary `.listing` files generated when downloading directories using FTP. This is generally not relevant when downloading websites over HTTP or HTTPS.

So, when you use `--mirror`, `wget` will download the **entire website**, including all linked pages, and only download files that have changed since the last download. It's a convenient option for creating a local mirror of a website.

The `--mirror` option also sets `-l inf` which means it will follow links **indefinitely deep**, while **the default for --recursive is to follow links up to 5 levels deep**.

Use the --mirror convenience option:

```sh
wget --mirror --no-clobber --page-requisites --html-extension --convert-links --restrict-file-names=windows --domains localhost --no-parent http://localhost:8000/
```

If you are not working on a Windows machine, you can remove the `--restrict-file-names=windows` option.

##### Use `wget` To Generate Static Files From <http://localhost:8000/wget_sitemap/>

First, validate the URLs in the sitemap using `linkchecker` and output the results to a file:

```sh
wget --spider --recursive --no-verbose --force-html -i http://localhost:8000/sitemap.xml > linkchecker_output.txt
```

Download or copy the URLs in the output from <http://localhost:8000/wget_sitemap/> to a plain text file named `wget_urls.txt`.

**Make sure the URLs in `wget_urls.txt` are pointing to `http://localhost:8000/` and NOT `https://danpoynor.com/`.**

Use `linkchecker` to validate the URLs in `wget_urls.txt` and output the results to a file:

```sh
linkchecker --timeout=30 --threads=2 -F text/linkchecker_output.log http://localhost:8000
```

If no broken links are found, then `cd` to the parent directory outside of the project to avoid `git` tracking the initial downloaded files then run `wget` with the `--config` option followed by the path to the `.wgetrc` file:

```sh
wget --config=danpoynorcom-django/.wgetrc -i danpoynorcom-django/wget_urls.txt
```

`wget` will create a directory name `localhost:8000` in the current directory and download the files there.

If `wget` pauses for a long time towards the end it's probably updating all the links in the project to be relative to the current directory. This is a good thing.

Move the files to a `docs/` directory in the project root and remove the `localhost:8000` directory, unless iterating.

Now you can add the `docs/` directory to Git and push it to GitHub and GitHub Pages will serve the static files from there.

---

##### Testing the build

To run a server in the directory containing the output, `cd` into `localhost+8000` directory and run:

```sh
python3 -m http.server 9876
```

Then visit <http://localhost:9876> in a web browser to make sure the server is running and the site looks good.

You can then run `linkchecker` on the build directory to check for broken links and output the results to a file:

```sh
linkchecker --timeout=30 --threads=2 -F text/linkchecker_output_port9876.log http://localhost:9876
```

Check for unused CSS. If the [PurgeCSS CLI](https://purgecss.com/CLI.html) is installed, you can run it from inside the `localhost+8000` directory to create an output file with only the used CSS and compare it to the original CSS file.

```sh
purgecss --css static/portfolio/styles.css --content **/*.html --output static/portfolio/styles.purged.css
```

</details>

## To Do

<details>
  <summary>Click to expand</summary>

- [ ] Write more tests
- [ ] Make sure urls match up:
  - [WGET Sitemap](http://localhost:8000/wget_sitemap/)
  - [sitemap.xml](http://localhost:8000/sitemap.xml)
  - [SEO audit](http://localhost:8000/seo-overview/)
- [ ] Evaluate automating the steps in the section 'Use `wget` To Generate Static Files' above.
- [ ] Evaluate automating adding the `sitemap.xml`, `robots.txt`, `favicon.ico` files to the `docs/` directory.
- [ ] Add concept matrix project item to the portfolio.
- [ ] Update images to high res in the portfolio.
- [ ] Add some cool `view-transition` animations.
- [ ] Add info on how to view Flash projects in the portfolio.

</details>
