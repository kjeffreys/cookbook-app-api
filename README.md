# cookbook-app-api
[![Build Status](https://www.travis-ci.com/kjeffreys/cookbook-app-api.svg?branch=main)](https://www.travis-ci.com/kjeffreys/cookbook-app-api)
 
_(included and explained commands run that were useful/frequent)_

## 1) Build from Dockerfile:
```
    docker build .
```

## 2) Build from docker-compose.yml:
```
   docker-compose build
```

## 3) Run commands using docker-compose:
```
docker-compose run {name of the service to run the command on} {command}
```

### Example
```
docker-compose run app sh -c "django-admin startproject app ."
```
    
    (Service here refers to an entry under "services" in docker-compose.yml)
    
    ... run a linux container created from the docker files, and then run...
    ... the command following, in this case from bash shell (sh -c), run ...
    ... the django admin management command "startproject" that comes    ...
    ... built-in with the Django pip install acquired from our req.txt,  ...
    ... and startproject creates the new project call "app", and         ...
    ... it does this startproject of app in the current directory        ...
    
    ... This process is run on the docker container, the path will be    ...
    ... based from the last "WORKDIR" set in "Dockerfile". So it's as    ...
    ... though we have used "cd into /app based on the Dockerfile, and   ...
    ... then we create a project (template code from django)             ...

## 4) TravisCI: setup AND troubleshooting for github integration with TDD
    ... Tracing through the .travis.yml file                             ...
    ... Every time the is a push to github, the .travis.yml tells travis ...
    ... 1) Spin up a Python 3.6 server                                   ...
    ... 2) Make the docker service available                             ...
    ... 3) Use pip to install docker-compose                             ...
    ... 4) Run test build & flake8 linting,failures will fail build/email...

    !!! UPDATE: Travis-CI Docker Pull Issue !!!

    -Docker have applied a rate limit on pulling images.

    -The limit is 100 pulls within 6 hours for unauthenticated users, 
    and 200 for authenticated users.

    -Because Travis-CI uses a shared IP (for all TravisCI users), 
    the 100 pulls is consumed quickly.

    -The solution is to authenticate with Docker in the Travis-CI job, 
    so you can take advantage of the 200 pulls every 6 hours.

    You can do it by following the below steps.
    1. Register on Docker Hub
    If you don't already have one, head over to hub.docker.com 
    and register for a new free account.

    2. Add credentials to Travis-CI project
    Login to travis-ci.com and select the cooking-app-api project.

    Choose More options > Settings:
    On the page, locate the Environment Variables section.
    
    Add the following variables:

    DOCKER_USERNAME - The username for your Docker Hub account.
    DOCKER_PASSWORD - The password for your Docker Hub account.

    !!!Be sure to escape and special characters in your password by 
    adding "\" before them!!!

    Also, ensure you leave DISPLAY VALUE IN BUILD LOG unchecked for 
    both values, because you don't want to expose your credentials 
    in the job output.

    3. Update Travis-CI Config
    In your project, open the .travis-ci.yml file, 
    and add the following block:

    before_install:
        - echo $DOCKER_PASSWORD | docker login --username $DOCKER_USERNAME 
        --password-stdin

    This does the following:
    echo $DOCKER_PASSWORD prints the password to the screen, 
    and the | (pipe) will send that output to the proceeding command.

    docker login --username $DOCKER_USERNAME will call the docker 
    login command with the username we set in the environment variables.

    --password-stdin is used to accept the password in a way that 
    prevents it being printed to the screen 
    (it???s required with the | syntax).

    Once done, full .travis-ci.yml file should look like .travis.yml 
    file as seen in first .travis.yml commit to this project.


    !!! UPDATE: Travis-CI Docker Pull Issue #2!!!
    TravisCI may not authorize for private repos with a free account. 
    Making repo public and making new commit to test if pull triggers 
    successfully.

    !!! Last update: Now working. May have just been migration of 
    TravisCI.org to TravisCI.com causing issues. Will test private again
    in future.

## 5) Getting started with Django TDD
**Prior** to running:
```
docker-compose run app sh -c "python manage.py test && flake8"
```
which will run all django tests 
(methods starting with test in files starting with test) 
and flake8 linter... need to install the flake8 on the docker image.

**Install** flake8 after adding to reqs by running 
```
docker-compose build
```
**Then**
```
docker-compose run app sh -c "python manage.py test && flake8"
```
```
Example output of above cmd:
Creating cookbook-app-api_app_run ... done
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
Destroying test database for alias 'default'...
./app/calc.py:5:1: E302 expected 2 blank lines, found 1
./app/calc.py:7:1: W391 blank line at end of file
./app/test_calc.py:4:1: E302 expected 2 blank lines, found 1
./app/test_calc.py:8:31: E231 missing whitespace after ','
./app/test_calc.py:12:1: W391 blank line at end of file
./app/test_calc.py:12:36: E231 missing whitespace after ','
ERROR: 1
```

## 6) Configure Django customer user model
```
docker-compose run app sh -c "python manage.py startapp core"
```
For new apps, add the new app (in this case 'core') to:
**INSTALLED_APPS** within the original settings file at path:
app/app/settings.py

**NOTE**:
The original state should create an error b/c in TDD, we want to make sure 
any tests fail first, which initially did in 
app/core/tests/test_models.py for the unit test
**test_create_user_with_email_successful(self):**

Leaving this error example for TDD understanding. However, in future commits
understand that TDD is used to make tests fail at first, but the new files added
for commit are updated to not fail _prior_ to add/commit, thus protecting the
repo's integrity. i.e. just b/c we don't keep adding tests that fail, doesn't
mean it wasn't done first and then the tests/code were altered to make the test
pass. This is important to understand b/c without failing first there is no 
assurance the test is actually working for the intended functionality tests.
```
======================================================================
ERROR: test_create_user_with_email_successful (core.tests.test_models.ModelTests)
Test creating a new user with a email entry is successful
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/core/tests/test_models.py", line 12, in test_create_user_with_email_successful
    password=password
TypeError: create_user() missing 1 required positional argument: 'username'

----------------------------------------------------------------------
Ran 1 test in 0.007s

FAILED (errors=1)
Destroying test database for alias 'default'...
ERROR: 1
```

And this is b/c django's default for get_user_model().objects.create_user()
is to expect an argument of "username". So when creating the model, it will
_extend_ the base django create_user() method and create the new version
with an argument of a user's "email" field instead of "username", 
and then the test will no longer fail.

Updating models to extend Django base methods for creating a user to be tested.

```
is_active=True
```
means a new user being created will be considered active unless
other specified

```
is_staff=False
```
means a new user being created will **NOT** be considered an employee access.

**FINALLY** notice that in app/app/settings.py , the added variable:
```
AUTH_USER_MODEL = 'core.User'
```
And that is the final step in creating a _custom_ user model extended from
the Django built-in User() and UserManager() models.

### Whenever models are changed, need to make migrations by running:
```
docker-compose run app sh -c "python manage.py makemigrations {app}"
```
In this case:
```
docker-compose run app sh -c "python manage.py makemigrations core"
```

**Output :**
```
Migrations for 'core':
  core/migrations/0001_initial.py
    - Create model User
```
Which produced file core/migrations/0001_initial.py is the instructions for 
Django to create the model in the real db that will be used later, and
setup the database automatically from the new models\

### Normalize emails
Django has a helper method to normalize domain section of emails to all 
lowercase, preventing random capitalization changes from not recognizing 
users as the same. This is added to in models, in the UserManager class's 
create_user() method now.
```
user = self.model(email=self.normalize_email(email), **extra_fields)
```
And checked against a test in test_models.py
```
self.assertEqual(user.email, email.lower())
```

### Add validation for email field
**Step 1)** TDD failure
```
    def test_new_user_invalid_email(self):
    """Test that creating user with no email raises error"""
        with self.assertRaises(ValueError):
        user = get_user_model().objects.create_user(None, 'test123')
```
**Output :**
```
======================================================================
FAIL: test_new_user_invalid_email (core.tests.test_models.ModelTests)
Test that creating user with no email raises error
----------------------------------------------------------------------
Traceback (most recent call last):
  File "/app/core/tests/test_models.py", line 29, in test_new_user_invalid_email
    user = get_user_model().objects.create_user(None, 'test123')
AssertionError: ValueError not raised

----------------------------------------------------------------------
Ran 3 tests in 0.222s

FAILED (failures=1)
Destroying test database for alias 'default'...
ERROR: 1
```
**Step 2:** Implement the feature in models.py so that 
{None, '', ..., other non-entries} to email field _will_ raise **ValueError**
```
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
```

## 7) Setup Django admin
   Update Django admin to allow management of custom user model. Consequently,
   this provides an interface to login and be able to:
        1) C reate new users manually
        2) R ead which users have been created by the Django
        3) U pdate and make changes to existing users
        4) D?

### Add tests for listing users in Django admin
    1) Add core/tests/test_admin.py
        a) Add all admin page Unit Tests
        b) Extend TestCase class to AdminSiteTests class
        c) Create setup() function: (Precedes all Unit Tests)
            i) Runs before all the other tests are run
            ii) Completes setup tasks that need to be done before other
              tests in the TestCase class will function correctly.

            Setup Task 1) create test Client
            Setup Task 2) setup new user (admin) to be used in tests
            Setup Task 3) Make sure user is logged into the Client
            Setup Task 4) create another user (regular/not admin) 
                            that is not authenticated to test (e.g. list users)
        d) Unit Test 1: Test that users are listed in Django Admin
            NOTE 1: same as normal users, admin.py expects username by default. 
            So again it will be tested for and modified to accept 'email' for a
            custom admin_user creation in lieu of expecting 'username'.
            Note 2: reverse() helper method from Django used. well documented
            on Django but want to note the syntax:
            ... reverse('{appBeingUsed}:{urlBeingUsed}') ...

            Steps:
            i) reverse('admin:core_user_changelist')
            will generate the URL for listing the user page.  
            ii) res = self.client.get(url)
            Use the test client object obtained from setup() to perform an
            HTTP get() on the url obtained from (i)
            iii) self.assertContains(res, self.user.name),(res, self.user.email)
            Django helper to check that the response from (ii) has fields.

