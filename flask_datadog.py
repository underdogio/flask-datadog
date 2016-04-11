from datadog.dogstatsd.base import DogStatsd


class TimerWrapper(DogStatsd._TimedContextManagerDecorator):
    def __init__(self, statsd, *args, **kwargs):
        super(TimerWrapper, self).__init__(statsd, *args, **kwargs)

    def start(self):
        self.__enter__()

    def stop(self):
        self.__exit__(None, None, None)


class StatsD(object):
    def __init__(self, app=None, config=None):
        """
        Constructor for `flask.ext.datadog.StatsD`

        >>> from flask.ext.datadog import StatsD
        >>> app = Flask(__name__)
        >>> statsd = StatsD(app=app)

        :param app: Flask app to configure this client for, if `app` is `None`, then do not
            configure yet (call `init_app` manually instead)
        :type app: flask.Flask or None

        :param config: Configuration for this client to use instead of `app.config`
        :type config: dict or None
        """
        self.config = config
        self.statsd = None

        # If an app was provided, then call `init_app` for them
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):
        """
        Initialize Datadog DogStatsd client from Flask app

        >>> from flask.ext.datadog import StatsD
        >>> app = Flask(__name__)
        >>> statsd = StatsD()
        >>> statsd.init_app(app=app)

        Available config settings:

          STATSD_HOST - statsd host to send metrics to (default: 'localhost')
          STATSD_MAX_BUFFER_SIZE - max number of metrics to buffer before sending, only used when batching (default: 50)
          STATSD_NAMESPACE - metric name prefix to use, e.g. 'app_name' (default: None)
          STATSD_PORT - statsd port to send metrics to (default: 8125)
          STATSD_TAGS - list of tags to include by default, e.g. ['env:prod'] (default: None)
          STATSD_USEMS - whether or not to report timing in milliseconds (default: False)

        :param app: Flask app to configure this client for
        :type app: flask.Flask

        :param config: optional, dictionary of config values (defaults to `app.config`)
        :type config: dict
        """
        # Used passed in config if provided, otherwise use the config from `app`
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        # Set default values for expected config properties
        self.config.setdefault('STATSD_HOST', 'localhost')
        self.config.setdefault('STATSD_MAX_BUFFER_SIZE', 50)
        self.config.setdefault('STATSD_NAMESPACE', None)
        self.config.setdefault('STATSD_PORT', 8125)
        self.config.setdefault('STATSD_TAGS', None)
        self.config.setdefault('STATSD_USEMS', False)

        self.app = app

        # Configure DogStatsd client
        # https://github.com/DataDog/datadogpy/blob/v0.11.0/datadog/dogstatsd/base.py
        self.statsd = DogStatsd(host=self.config['STATSD_HOST'],
                                port=self.config['STATSD_PORT'],
                                max_buffer_size=self.config['STATSD_MAX_BUFFER_SIZE'],
                                namespace=self.config['STATSD_NAMESPACE'],
                                constant_tags=self.config['STATSD_TAGS'],
                                use_ms=self.config['STATSD_USEMS'])

    def timer(self, *args, **kwargs):
        """Helper to get a `flask_datadog.TimerWrapper` for this `DogStatsd` client"""
        return TimerWrapper(self.statsd, *args, **kwargs)

    def incr(self, *args, **kwargs):
        """Helper to expose `self.statsd.increment` under a shorter name"""
        return self.statsd.increment(*args, **kwargs)

    def decr(self, *args, **kwargs):
        """Helper to expose `self.statsd.decrement` under a shorter name"""
        return self.statsd.decrement(*args, **kwargs)

    def __getattr__(self, name):
        """
        Magic method for fetching any underlying attributes from `self.statsd`

        We utilize `__getattr__` to ensure that we are always compatible with
        the `DogStatsd` client.
        """
        # If `self.statsd` has the attribute then return that attribute
        if self.statsd and hasattr(self.statsd, name):
            return getattr(self.statsd, name)
        raise AttributeError('\'StatsD\' has has attribute \'%s\'' % (name, ))

    def __enter__(self):
        """
        Helper to expose the underlying `DogStatsd` client for context managing

        >>> statsd = StatsD(app=app)
        >>> # Batch any metrics within the `with` block
        >>> with statsd:
        >>>   statsd.increment('metric')
        """
        return self.statsd.__enter__()

    def __exit__(self, *args, **kwargs):
        """Helper to expose the underlying `DogStatsd` client for context managing"""
        return self.statsd.__exit__(*args, **kwargs)
