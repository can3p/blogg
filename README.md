# Yet another django blog application

Blog application written in Django + python with livejournal.com compatible xmlrpc

__Warning__: xmlrpc api support almost nothing compared to the real one - create or
update post with subject and body

## Install

For newcomers in python world it's kind of a mess. Even if we skip python 2.x vs python 3.x
drama, we still have to make gazilion of choices. Since installing all modules system wide
is not in fashion, there are some options to have a local env. What would you choose - `virtualenv`?
`venv`? And what are all those `virtualenvwrapper`, `pew`, `penv` and friends?

This project went with on of possible setups. Initial install is neatly outlined [there][mozilla].

Don't create your own project though, because you already have blogg!

To manage dependencies we will use `pipenv`, because it's closer to sanity. Most guides recommend
local install, but only a system one worked for me

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
BASE_URL=http://localhost:8000
~~~

Once that's done, running `blogg` is just a matter of

~~~bash
$ cd /path/to/blogg
$ pipenv install
$ pipenv run python3 manage.py migrate
$ pipenv run python3 manage.py runserver
~~~

## Adding user

Blogg is set up using pipenv, so we'll use it to get into proper virtual
environment and then we'll jump recursively into another shell, python this time,
to create new user.

~~~bash
$ pipenv shell
$ python manage.py shell
Python 3.5.2 (default, Nov 23 2017, 16:37:01) 
[GCC 5.4.0 20160609] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> from web.models import User
>>> user = User.objects.create_user('john', 'john.doe@a.com', 'test1234')
~~~

## Cl-journal intrgration

[cl-journal][cl-journal] is a livejournal client, which can work
with blogg. Follow instructions from it's home page to get it up
and running. After that you can start using it with blogg with
a following command:

~~~bash
$ mkdir my-blog
$ cd my-blog
$ cl-journal init http://localhost:8000/xmlrpc
~~~

Where `http://localhost:8000` should be replaced with
a base url your instance of blogg works on

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
* every statement *should* end with semicolon. If your statement do not work, this is why.

[mozilla]: https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/development_environment
[do]: https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04
[cl-journal]: https://github.com/can3p/cl-journal
