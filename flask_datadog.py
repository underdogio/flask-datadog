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
        self.config = config
        self.statsd = None
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):
        """
        Initialize Datadog DogStatsd client from Flask app

        Available config settings:

          STATSD_HOST - statsd host to send metrics to (default: 'localhost')
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
        self.config.setdefault('STATSD_NAMESPACE', None)
        self.config.setdefault('STATSD_PORT', 8125)
        self.config.setdefault('STATSD_TAGS', None)
        self.config.setdefault('STATSD_USEMS', False)

        self.app = app

        # Configure DogStatsd client
        # https://github.com/DataDog/datadogpy/blob/v0.11.0/datadog/dogstatsd/base.py
        self.statsd = DogStatsd(host=self.config['STATSD_HOST'],
                                port=self.config['STATSD_PORT'],
                                namespace=self.config['STATSD_NAMESPACE'],
                                constant_tags=self.config['STATSD_TAGS'],
                                use_ms=self.config['STATSD_USEMS'])

    @property
    def use_ms(self):
        return self.config.get('use_ms', False)

    def timer(self, *args, **kwargs):
        return TimerWrapper(self.statsd, *args, **kwargs)

    def timed(self, *args, **kwargs):
        return self.statsd.timed(*args, **kwargs)

    def timing(self, *args, **kwargs):
        return self.statsd.timing(*args, **kwargs)

    def incr(self, *args, **kwargs):
        return self.statsd.increment(*args, **kwargs)

    def decr(self, *args, **kwargs):
        return self.statsd.decrement(*args, **kwargs)

    def gauge(self, *args, **kwargs):
        return self.statsd.gauge(*args, **kwargs)

    def histogram(self, *args, **kwargs):
        return self.statsd.histogram(*args, **kwargs)

    def set(self, *args, **kwargs):
        return self.statsd.set(*args, **kwargs)

    def event(self, *args, **kwargs):
        return self.statsd.event(*args, **kwargs)
