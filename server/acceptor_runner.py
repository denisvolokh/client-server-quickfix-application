import quickfix
from acceptor_app import AcceptorApplication
import threading
import json
import redis
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

_logger = logging.getLogger("acceptor_app")
file_handler = logging.FileHandler('app.logs')

file_handler.setFormatter(formatter)
_logger.addHandler(file_handler)
_logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
_logger.addHandler(console_handler)


class Listener(threading.Thread):
    def __init__(self, connection, app, logger):
        threading.Thread.__init__(self)

        self.app = app
        self.redis = connection
        self.logger = logger

        self.pubsub = self.redis.pubsub()

        self.logger.info("[+] Subscribing for channels: internal")
        self.pubsub.subscribe(["internal"])

    def work(self, item):
        if type(item["data"]) != int:
            self.logger.info(item['data'])

            self.app.send_report()

    def run(self):
        for item in self.pubsub.listen():
            self.work(item)


if __name__ == "__main__":

    file_name = "acceptor.cfg"
    application = AcceptorApplication(logger=_logger)

    try:
        settings = quickfix.SessionSettings(file_name)
        store_factory = quickfix.FileStoreFactory(settings)
        log_factory = quickfix.FileLogFactory(settings)
        acceptor = quickfix.SocketAcceptor(application, store_factory, settings, log_factory)

        acceptor.start()

        # application.run()
        # acceptor.stop()

    except quickfix.ConfigError as e:
        print(e)

    redis_connection = redis.Redis("redis")
    client = Listener(redis_connection, application, _logger)
    client.start()