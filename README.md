# Yet another django blog application

## Install

For newcomers in python world it's kind of a mess. Even if we skip python 2.x vs python 3.x
drama, we still have to make gazilion of choices. Since installing all modules system wide
is not in fashion, there are some options to have a local env. What would you choose - `virtualenv`?
`venv`? And what are all those `virtualenvwrapper`, `pew`, `penv` and friends?

This project went with on of possible setups. Initial install is neatly outlined [there][mozilla].

Don't create your own project though, because you already have blogg!

To manage dependencies we will use `pipenv`, because it's closes to sanity. Most guides recommend
local install, but only system one worked for me

~~~bash
# ubuntu
$ sudo pip3 install pipenv
~~~

Nice. Once that's done, it's time to install postgresql and setup database and user there.

~~~bash
$ sudo apt-get install postgresql-9.5
~~~

Database setup (borrowed from [here][do]):

~~~bash
$ sudo -u postgres psql
psql (9.5.11)
Type "help" for help.

postgres=# create database blogg;
CREATE DATABASE
postgres=# create user blogg with password '<your password there>';
CREATE ROLE
postgres=# alter role blogg  SET client_encoding TO 'utf8';
ALTER ROLE
postgres=# alter role blogg  SET default_transaction_isolation TO 'read committed';
ALTER ROLE
postgres=# alter role blogg   SET timezone TO 'UTC';
ALTER ROLE
postgres=# GRANT ALL PRIVILEGES ON DATABASE blogg to blogg;
GRANT
postgres=# \q
~~~

Next, create `.env` file in the root of this repo with following content:

~~~
SECRET_KEY=<large random string>
DEBUG=True
DB_NAME=blogg
DB_USER=blogg
DB_PASSWORD=<your password from previous step there>
DB_HOST=127.0.0.1
~~~

Once that's done, running `blogg` is just a matter of

~~~bash
$ cd /path/to/blogg
$ pipenv install
$ pipenv run python3 manage.py migrate
$ pipenv run python3 manage.py runserver
~~~

## Notes

Just in case you forgot, you can get to `pgsql` shell using:

~~~bash
sudo -u postgres psql
~~~

And small cheatsheet:

* `\l` - list all databases
* `\c <db>` - switch to database `<db>`
* `\dt` - show all tables in the active database
* `\d <table>` describe table

[mozilla]: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment
[do]: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
