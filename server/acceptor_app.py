from quickfix import Application
import quickfix as fix
import requests
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

SUBSCRIPTION_TYPES = {
    "0": "Snapshot",
    "1": "Snapshot + Updates",
    "2": "Disable Previous"
}


class AcceptorApplication(Application):

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

            response = requests.get(url="http://127.0.0.1:5555/bonds")
            logger.info("   [+] API response: {0}".format(response.json()))

        if message_type_value == fix.MsgType(fix.MsgType_TradeCaptureReportRequest).getValue():
            logger.info("   [+] Received Trade Capture Report Request!")

            subscription_type_field = fix.SubscriptionRequestType()
            message.getField(subscription_type_field)
            subscription_type_value = subscription_type_field.getValue()
            logger.info("   [+] Subscription Type: {}".format(SUBSCRIPTION_TYPES.get(subscription_type_value)))

            ack_message = fix.Message()
            ack_message.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
            ack_message.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReportAck))
            ack_message.setField(fix.TrdRptStatus(fix.TrdRptStatus_ACCEPTED))
            logger.info("   [+] Sending Ack message!")

            try:
                fix.Session.sendToTarget(ack_message, self.session_id)

            except Exception:
                logger.info("[!!!] Session Not found!")

        return

    def toAdmin(self, message, session_id):
        logger.info("[+] On toAdmin: %s" % message)
        return

    def fromAdmin(self, message, session_id):
        logger.info("[+] On fromAdmin: %s" % message)

    def run(self):

        while True:
            continue
