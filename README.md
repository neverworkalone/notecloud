# notecloud
[![API](https://github.com/neverworkalone/notecloud/actions/workflows/backend.yml/badge.svg?branch=master)](https://github.com/neverworkalone/notecloud/actions/workflows/backend.yml)
[![CircleCI](https://circleci.com/gh/neverworkalone/notecloud.svg?style=shield)](https://app.circleci.com/pipelines/github/neverworkalone/notecloud)
[![codecov](https://codecov.io/gh/neverworkalone/notecloud/branch/master/graph/badge.svg?token=E3N012HFHN)](https://codecov.io/gh/neverworkalone/notecloud)

Notecloud a.k.a. CheckCheck son of Workcloud


# Create database before setup

    $ psql
    postgres=# create user <DB_USER>;
    postgres=# alter user <DB_USER> with password '<DB_PASSWORD>';
    postgres=# create database <DB_NAME> owner <DB_USER>;


# Getting started with notecloud

    $ git clone https://github.com/neverworkalone/notecloud.git
    $ pip install -r requirements.txt
    $ python manage.py migrate
    $ ./serve.sh
    $ cd frontend/wc
    $ npm install
    $ npm run serve


# unittest

    $ tox  # You can use tox to generate coverage with unittest or just below script
    $ ./runtest.sh  # This has more options for convenience. check more with ./runtest.sh --help
