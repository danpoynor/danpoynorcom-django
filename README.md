# Dan Poynor Portfolio

Personal portfolio website for danpoynor.com built in Django.

Django is used as the CMS locally, SQLite for the database, and SASS for CSS. Then `wget` is used to crawl  `http://localhost:8000`` and generate static`.html` files to deploy to the live site.

Note some aspects of the Django website are slow to load because of heavy filtering (customer mangers) I'm using to display the data on the front-end. I'm working on optimizing the code to speed things up but this is a low priority since I'm the only one using this repo.

Special URLs:

- <http://localhost:8000/wget_sitemap/>: Generates a sitemap for `wget` to use when generating static files.
- <http://localhost:8000/website-seo-overview/>: Generates a SEO audit of the site.

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
- [`python-dotenv`](https://pypi.org/project/python-dotenv/): Python library used to read key-value pairs from a `.env` environment file.
- ['django-extensions'](https://pypi.org/project/django-extensions/): Collection of custom extensions for the Django Framework. Example commands:
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

There are 144 passing unit tests so far located in the `tests/` directory.

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

After testing Bakery and studying other Django static site generators, I decided to use `wget` to generate the static files for this project since I can get it to capture the paginated pages as needed and it's already installed on my Mac.

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

#### The `--mirror` Option

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

#### Use `wget` To Generate Static Files From A Sitemap from <http://localhost:8000/wget_sitemap/>

Download or copy the output from <http://localhost:8000/wget_sitemap/> to a file named `urls_for_wget.txt`.

Create directory `docs` and download files to it:

```sh
mkdir docs
wget -i urls_for_wget.txt --mirror --no-clobber --page-requisites --html-extension --convert-links --domains localhost --no-parent -P docs
```

NOTE: Might need to manually move the files from `docs/localhost:8000` to `docs/` and delete the `docs/localhost:8000` directory. Also might need to manually add the `sitemap.xml` and `robots.txt` files to the `docs/` directory.

TODO: Automate the above NOTE steps before testing and pushing the site live.

##### Testing the build

To run a server in the directory containing the output, `cd` into `localhost+8000` directory and run:

```sh
python -m http.server 9876
```

Then visit <http://localhost:9876> in a web browser.

You can then run `linkchecker` on the build directory to check for broken links and output the results to a file:

```sh
linkchecker --timeout=20 --threads=2 -F text/linkchecker_output.txt http://localhost:9876
```

Check for unused CSS. If the [PurgeCSS CLI](https://purgecss.com/CLI.html) is installed, you can run it from inside the `localhost+8000` directory to create an output file with only the used CSS and compare it to the original CSS file.

```sh
purgecss --css static/portfolio/styles.css --content **/*.html --output static/portfolio/styles.purged.css
```

</details>

## To Do

<details>
  <summary>Click to expand</summary>

- [ ] Add a robots.txt file.
- [ ] Need to cross check links to make sure urls match up:
  - [WGET Sitemap](http://localhost:8000/wget_sitemap/)
  - [sitemap.xml](http://localhost:8000/sitemap.xml)
  - [SEO audit](http://localhost:8000/website-seo-overview/)
- [ ] Populate MediaType column in Project Items table.
  - [ ] Filter ProjectItems by MediaType on MediaTypeProjectsListView page, possible other places.
  - [ ] May need to refactor schema so other taxonomies are also associated with ProjectItems instead of Projects.
- [ ] Automate the steps in the 'Use `wget` To Generate Static Files' section above.
- [ ] Automate adding the `sitemap.xml` and `robots.txt` files to the `docs/` directory.

</details>
