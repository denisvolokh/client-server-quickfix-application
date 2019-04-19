import quickfix
from acceptor_app import AcceptorApplication

file_name = "acceptor.cfg"

try:
    settings = quickfix.SessionSettings(file_name)
    application = AcceptorApplication()
    store_factory = quickfix.FileStoreFactory(settings)
    log_factory = quickfix.FileLogFactory(settings)
    acceptor = quickfix.SocketAcceptor(application, store_factory, settings, log_factory)

    acceptor.start()

    acceptor.stop()

except quickfix.ConfigError as e:
    print(e)