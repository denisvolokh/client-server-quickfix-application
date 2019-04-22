from quickfix import Application
import quickfix as fix
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger("acceptor_app")
file_handler = logging.FileHandler('logs/app.logs')

file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


class AcceptorApplication(Application):

    # def __init__(self, *args, **kwargs):
    #     super(Application, self).__init__(*args, **kwargs)

    def onCreate(self, session_id):
        self.session_id = session_id
        logger.info("[+] On Create: {}".format(session_id))
        return

    def onLogon(self, session_id):
        return

    def onLogout(self, session_id):
        logger.info("[+] On Logout: %s" % session_id)
        return

    def toApp(self, message, session_id):
        logger.info("[+] On toApp: %s" % message)
        return

    def fromApp(self, message, session_id):
        logger.info("[+] On fromApp: %s" % message)

        message_type_field = fix.MsgType()
        message.getHeader().getField(message_type_field)
        message_type_value = message_type_field.getValue()

        if message_type_value == fix.MsgType(fix.MsgType_SecurityDefinitionRequest).getValue():
            logger.info("   [+] Received Security Definition Request!")

        return

    def toAdmin(self, message, session_id):
        logger.info("[+] On toAdmin: %s" % message)
        return

    def fromAdmin(self, message, session_id):
        logger.info("[+] On fromAdmin: %s" % message)

    def run(self):

        while True:
            continue
