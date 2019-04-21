import quickfix
from client.client_app import InitiatorApplication

file_name = "client/initiator.cfg"

try:
    settings = quickfix.SessionSettings(file_name)
    application = InitiatorApplication()
    store_factory = quickfix.FileStoreFactory(settings)
    log_factory = quickfix.FileLogFactory(settings)
    acceptor = quickfix.SocketInitiator(application, store_factory, settings, log_factory)

    acceptor.start()

    application.run()

    acceptor.stop()

except quickfix.ConfigError as e:
    print(e)