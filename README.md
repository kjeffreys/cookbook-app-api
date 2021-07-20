# cookbook-app-api

Notes: 
(mostly commands run to remember that are useful/frequent)

# 1) Build from Dockerfile:
```
    docker build .
```

# 2) Build from docker-compose.yml:
```
   docker-compose build
```

# 3) Run commands using docker-compose:
    "docker-compose run {name of the service to run the command on} {command}"

    ex1)```docker-compose run app sh -c "django-admin startproject app ."```
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

# 4) TravisCI: setup AND troubleshooting for github integration with TDD
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
    (it’s required with the | syntax).

    Once done, full .travis-ci.yml file should look like .travis.yml 
    file as seen in first .travis.yml commit to this project.


    !!! UPDATE: Travis-CI Docker Pull Issue #2!!!
    TravisCI may not authorize for private repos with a free account. 
    Making repo public and making new commit to test if pull triggers 
    successfully.

    !!! Last update: Now working. May have just been migration of 
    TravisCI.org to TravisCI.com causing issues. Will test private again
    in future.

# 5) Getting started with Django TDD

    Prior to running
    ```docker-compose run app sh -c "python manage.py test && flake8"```
    which will run all django tests 
    (methods starting with test in files starting with test) 
    and flake8 linter... need to install the flake8 on the docker image.

    Install flake8 after adding to reqs by running 
    ```docker-compose build```

Example output of above cmd:
user@host /d/cookbook-app-api (main)
$ docker-compose run app sh -c "python manage.py test && flake8" 
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

    
