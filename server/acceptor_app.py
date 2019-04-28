from quickfix import Application
import quickfix as fix
import requests
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger("acceptor_app")
file_handler = logging.FileHandler('app.logs')

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

            self._process_security_definition_request(message=message, session_id=session_id)

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

    def _process_security_definition_request(self, message, session_id):
        logger.info("  [+] Processing security definition request ...")

        security_type_field = fix.SecurityType()
        message.getField(security_type_field)
        securty_type_value = security_type_field.getValue()
        logger.info("  [+] Security Type: {}".format(securty_type_value))

        security_request_id_field = fix.SecurityReqID()
        message.getField(security_request_id_field)
        securty_request_id_value = security_request_id_field.getValue()
        logger.info("  [+] Security Request Id: {}".format(securty_request_id_value))

        if securty_type_value == fix.SecurityType_CORPORATE_BOND:
            # response = requests.get(url="http://127.0.0.1:5555/bonds")
            response = requests.get(url="http://restapi:5555/bonds")
            logger.info("   [+] API response: {0}".format(response.json()))

            bonds = response.json()
            for bond_item in bonds:
                self._send_security_definition(security_req_id=securty_request_id_value,
                                               data=bond_item,
                                               session_id=session_id)

    def _send_security_definition(self, security_req_id, data, session_id):
        logger.info("   [+] Sending definition: {}".format(data["internalcode"]))
        msg = fix.Message()
        msg.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        msg.getHeader().setField(fix.MsgType(fix.MsgType_SecurityDefinition))
        msg.setField(fix.ApplID("SERVER"))
        # msg.setField(fix.ApplSeqNum())
        msg.setField(fix.SecurityReqID(security_req_id))
        msg.setField(fix.SecurityResponseType(8))  # Exchange Symbol

        msg.setField(fix.SecurityAltID(str(data["internalcode"])))
        msg.setField(fix.MaturityDate(str(data["maturity_date"])))
        msg.setField(fix.CouponRate(data["nominal_yield"]))
        msg.setField(fix.InstrAttribValue(str(data["type"])))
        msg.setField(fix.SecurityType(fix.SecurityType_CORPORATE_BOND))
        msg.setField(fix.Currency("AUD"))

        msg.setField(fix.SecurityAltIDSource("8"))  # Instrument Identifier = 8

        fix.Session.sendToTarget(msg, session_id)


