## BabbelLearn

### How to run

* Direct run locally
  - install virtualenv using `pip install -m virtualenv`
  - create virtualenv using `virtualenv env -p python3`
  - enter into virtual env using `source env/bin/activate`
  - install requirements using `pip install -r requirements/base.txt` and `pip install -r requirements/local.txt`
  - set environment variable `export DATABASE_URL=postgres://<USERNAME>:<PASSWORD>@localhost:5432/<DB_NAME>"`
  - migrate database using `python manage.py migrate`
  - run server `python manage.py runserver`
  - *Note* - *you need to setup postgres seperatly with this type of installation and create postgres DB manually, recomended to use docker appraoch instead to directly run application with postgres*


* Docker run locally
  - make sure you have docker and docker-compose installed, if not please refer https://docs.docker.com/engine/install/
  - run `docker-compose -f local.yml build`
  - run `docker-compose -f local.yml up`


### Postman Collection link
  - https://www.getpostman.com/collections/5d0b556b7d2a1852fa3a

### Documentation Link
  - https://documenter.getpostman.com/view/17731664/UUy4c5Ha
