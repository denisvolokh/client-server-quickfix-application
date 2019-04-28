import quickfix
from initiator_app import InitiatorApplication

file_name = "initiator.cfg"

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