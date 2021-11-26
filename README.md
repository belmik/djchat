# djchat - test task 

Django based chat room

## How to run on public accessible machine

- Before running you need to set couple of environment variables:
  - `ALLOWED_HOSTS` domain name which pointed at your server
  - `SECRET_KEY` django secret key string
  - `POSTGRES_PASSWORD` password for postgres database
- Copy repository to your host machine
- Run `docker-compose up --build -d`
- To setup django models for first time run `docker-compose exec web python manage.py migrate`
- At this point chat should be running with ssl

## How to run on local machine without ssl
- Setup same environment variables 
- Copy repository
- Run `docker-compose -f docker-compose-local.yml up --build -d`
- To setup django models for first time run `docker-compose exec web python manage.py migrate`
- Chat should be available at `http://0.0.0.0:8000/`
