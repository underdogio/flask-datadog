Flask-Datadog
=============

This is a simple Flask extension that allows to access DogStatsd in your Flask application. It has an API
compatible with Flask-StatsD


Installation
------------

To install it, simply: ::

    pip install Flask-Datadog


Usage
-----

You only need to import and initialize your app ::

    from flask import Flask
    from flask.ext.datadog import StatsD

    app = Flask(__name__)
    app.config['STATSD_HOST'] = 'statsd.local'
    statsd = StatsD(app)


