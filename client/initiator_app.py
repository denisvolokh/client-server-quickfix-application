from quickfix import Application
import quickfix as fix
import quickfix50sp2 as fixn
import logging

formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

logger = logging.getLogger("client_app")
file_handler = logging.FileHandler('app.logs')

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

        if message_type_value == fix.MsgType(fix.MsgType_MarketDataRequestReject).getValue():
            logger.info("   [!!!] Received Market Data Request Rejected message!")

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

        msg.setField(fix.SecurityReqID("123"))  # IRESS will set the request ID in this field.
        msg.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT)) # Value of this field will be set to 0 (Snapshot)
        msg.setField(fix.SecurityRequestType(8))  # value of this field will be set to 8 (All Securities)
        msg.setField(fix.SecurityType(fix.SecurityType_CORPORATE_BOND))

        try:
            fix.Session.sendToTarget(msg, self.session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    def send_TradeCaptureReportRequest_message(self):
        msg = fix.Message()
        msg.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        msg.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReportRequest))
        msg.getHeader().setField(fix.TradeRequestID("Trade-Request-Id"))
        # msg.setField(fix.StringField(263, fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))
        msg.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))

        try:
            fix.Session.sendToTarget(msg, self.session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    def send_MarketDataRequest_message(self):
        logger.info("[+] Sending MarketDataRequest message ...")

        msg = fix.Message()
        msg.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        msg.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
        msg.setField(fix.MDReqID("Market-Data-Request-Id"))
        msg.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))

        msg.setField(fix.NoMDEntryTypes(2))

        group = fixn.MarketDataRequest.NoMDEntryTypes()

        group.setField(fix.MDEntryType(fix.MDEntryType_BID))
        msg.addGroup(group)

        # group.setField(fix.MDEntryType(fix.MDEntryType_OFFER))
        # msg.addGroup(group)

        msg.setField(fix.NoRelatedSym(1))
        msg.setField(fix.SecurityID("AF2016"))

        try:
            fix.Session.sendToTarget(msg, self.session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    def send_MarketDataRequest_rejected_message(self):
        logger.info("[+] Sending MarketDataRequest(Rejected) message ...")

        msg = fix.Message()
        msg.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        msg.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequest))
        msg.setField(fix.MDReqID("Market-Data-Request-Id-Rejected"))
        msg.setField(fix.SubscriptionRequestType(fix.SubscriptionRequestType_SNAPSHOT_PLUS_UPDATES))

        msg.setField(fix.NoMDEntryTypes(2))

        group = fixn.MarketDataRequest.NoMDEntryTypes()

        group.setField(fix.MDEntryType(fix.MDEntryType_BID))
        msg.addGroup(group)

        # group.setField(fix.MDEntryType(fix.MDEntryType_OFFER))
        # msg.addGroup(group)

        msg.setField(fix.NoRelatedSym(1))
        msg.setField(fix.SecurityID("AF2016"))

        try:
            fix.Session.sendToTarget(msg, self.session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    # def run(self):
    #
    #     while True:
    #         continue

    def run(self):

        print(">>>     Press 1 to send SecurityDefinitionRequest message")
        print(">>>     Press 2 to send TradeCaptureReport request message")
        print(">>>     Press 3 to send MarketDataRequest message")
        print(">>>     Press 4 to send MarketDataRequest (Rejected) message")
        print(">>>     Press q to quit")

        while True:
            _input_value = input()

            if _input_value == "1":
                self.send_SecurityDefinitionRequest_message()

            elif _input_value == "2":
                self.send_TradeCaptureReportRequest_message()

            elif _input_value == "3":
                self.send_MarketDataRequest_message()

            elif _input_value == "4":
                self.send_MarketDataRequest_rejected_message()

            elif _input_value == "q":
                break

            elif _input_value == 'd':
                import pdb
                pdb.set_trace()

            else:
                continue
