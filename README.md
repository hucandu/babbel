## BabbelLearn

### How to run

* Direct run locally
  - install virtualenv using `pip install -m virtualenv`
  - create virtualenv using `virtualenv env -p python3`
  - install requirements using `pip install -r requirements/base.txt` and `pip install -r requirements/local.txt`
  - run server `python manage.py runserver`
  - *Note* - *you need to setup postgres seperatly with this type of installation and create postgres DB manually, recomended to use docker appraoch*


* Docker run locally
  - run `docker-compose -f local.yml build`
  - run `docker-compose -f local.yml up`


### Postman Collection link
  - https://www.getpostman.com/collections/5d0b556b7d2a1852fa3a

### Documentation Link
  - https://documenter.getpostman.com/view/17731664/UUy4c5Ha
