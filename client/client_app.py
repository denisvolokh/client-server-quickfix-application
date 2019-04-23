from quickfix import Application
import quickfix as fix
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

    def onCreate(self, session_id):
        logger.info("[+] On Create: {}".format(session_id))

        return

    def onLogon(self, session_id):
        self.session_id = session_id
        logger.info("[+] Successful Logon to session '%s'." % session_id.toString())

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

        if message_type_value == fix.MsgType(fix.MsgType_TradeCaptureReportAck).getValue():
            logger.info("   [+] Received Trade Report Ack message!")

        return

    def toAdmin(self, message, session_id):
        logger.info("[+] On toAdmin: %s" % message)

        return

    def fromAdmin(self, message, session_id):
        logger.info("[+] On fromAdmin: %s" % message)

    def send_SecurityDefinitionRequest_message(self):
        msg = fix.Message()
        msg.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        msg.getHeader().setField(fix.MsgType(fix.MsgType_SecurityDefinitionRequest))
        msg.getHeader().setField(fix.SecurityReqID("123"))
        msg.getHeader().setField(fix.SecurityRequestType(0))

        try:
            fix.Session.sendToTarget(msg, self.session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    def send_TradeCaptureReportRequest_message(self):
        msg = fix.Message()
        msg.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        msg.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReportRequest))
        msg.getHeader().setField(fix.TradeRequestID("Trade-Request-Id"))
        msg.setField(fix.StringField(263, fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))

        try:
            fix.Session.sendToTarget(msg, self.session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    def run(self):

        print '''
        Press 1 to send SecurityDefinitionRequest message
        Press 2 to send TradeCaptureReport request message
        Press q to quit
        '''

        while True:
            input = raw_input()

            if input == "1":
                self.send_SecurityDefinitionRequest_message()

            elif input == "2":
                self.send_TradeCaptureReportRequest_message()

            elif input == "q":
                break

            elif input == 'd':
                import pdb
                pdb.set_trace()

            else:
                continue
