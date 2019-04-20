from quickfix import Application
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger("client_app")
file_handler = logging.FileHandler('logs/app.logs')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class InitiatorApplication(Application):

    def onCreate(self, arg0):
        logger.info("[+] On Create: {}".format(arg0))

        return

    def onLogout(self, session_id):
        logger.info("[+] On Logout: %s" % session_id)
        return

    def toApp(self, message, session_id):
        logger.info("[+] On toApp: %s" % message)
        return

    def fromApp(self, message, session_id):
        logger.info("[+] On fromApp: %s" % message)
        return

    def toAdmin(self, message, session_id):
        logger.info("[+] On toAdmin: %s" % message)

        return

    def fromAdmin(self, message, session_id):
        logger.info("[+] On fromAdmin: %s" % message)

    def run(self):

        while True:
            continue
