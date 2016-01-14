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
        self.config = None
        self.statsd = None
        if app is not None:
            self.init_app(app)
        else:
            self.app = None

    def init_app(self, app, config=None):
        if config is not None:
            self.config = config
        elif self.config is None:
            self.config = app.config

        self.config.setdefault('STATSD_HOST', 'localhost')
        self.config.setdefault('STATSD_PORT', 8125)
        self.config.setdefault('STATSD_TAGS', None)

        self.app = app

        self.statsd = DogStatsd(self.config['STATSD_HOST'],
                                self.config['STATSD_PORT'], self.config['STATSD_TAGS'])

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
