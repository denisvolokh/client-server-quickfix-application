from quickfix import Application
import quickfix as fix
import quickfix50sp2 as fixn
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

TRADE_TRANSACTION_TYPE = {
    "NEW": 0,
    "CANCEL": 1,
    "RELEASE": 3
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

            self._ack_trade_capture_request(message=message, session_id=session_id)

        if message_type_value == fix.MsgType(fix.MsgType_MarketDataRequest).getValue():
            logger.info("   [+] Received Market Data Request!")

            self._process_market_data_request(message=message, session_id=session_id)

        return

    def toAdmin(self, message, session_id):
        logger.info("[+] On toAdmin: %s" % message)
        return

    def fromAdmin(self, message, session_id):
        logger.info("[+] On fromAdmin: %s" % message)

    def run(self):

        while True:
            continue

    def _process_market_data_request(self, message, session_id):
        logger.info("  [+] Processing market data request ...")

        md_req_id_field = fix.MDReqID()
        message.getField(md_req_id_field)
        md_req_id_value = md_req_id_field.getValue()
        logger.info("   [+] Market Data Request Id: {}".format(md_req_id_value))

        security_id_field = fix.SecurityID()
        message.getField(security_id_field)
        security_id_value = security_id_field.getValue()
        logger.info("   [+] Security Id: {}".format(security_id_value))

        if "REJECT" in md_req_id_value.upper():
            reject_message = fix.Message()
            reject_message.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
            reject_message.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataRequestReject))

            reject_message.setField(fix.MDReqID(md_req_id_value))

            logger.info("   [+] Sending Reject message!")

            try:
                fix.Session.sendToTarget(reject_message, session_id)

            except Exception:
                logger.info("[!!!] Session Not found!")

        else:
            market_data_snapshot = fix.Message()

            market_data_snapshot.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
            market_data_snapshot.getHeader().setField(fix.MsgType(fix.MsgType_MarketDataSnapshotFullRefresh))

            market_data_snapshot.setField(fix.ApplID("SERVER"))
            market_data_snapshot.setField(fix.ApplSeqNum(1))
            market_data_snapshot.setField(fix.SecurityID(security_id_value))

            group = fixn.MarketDataSnapshotFullRefresh.NoMDEntries()
            group.setField(fix.MDEntryType(fix.MDEntryType_BID))
            group.setField(fix.MDEntryID("111"))
            group.setField(fix.MDEntryPx(99.9))
            group.setField(fix.Yield(0.9))
            group.setField(fix.MDEntrySize(1234))
            market_data_snapshot.addGroup(group)

            try:
                fix.Session.sendToTarget(market_data_snapshot, session_id)

            except Exception:
                logger.info("[!!!] Session Not found!")



    def _ack_trade_capture_request(self, message, session_id):
        logger.info("  [+] Ack trade capture request ...")

        subscription_type_field = fix.SubscriptionRequestType()
        message.getField(subscription_type_field)
        subscription_type_value = subscription_type_field.getValue()
        logger.info("   [+] Subscription Type: {}".format(SUBSCRIPTION_TYPES.get(subscription_type_value)))

        ack_message = fix.Message()
        ack_message.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
        ack_message.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReportRequestAck))
        ack_message.setField(fix.TrdRptStatus(fix.TrdRptStatus_ACCEPTED))
        logger.info("   [+] Sending Ack message!")

        try:
            fix.Session.sendToTarget(ack_message, self.session_id)

            self._send_trade_capture_report(session_id=session_id)

        except Exception:
            logger.info("[!!!] Session Not found!")

    def _send_trade_capture_report(self, session_id):
        logger.info("  [+] Send trade capture report ...")

        response = requests.get(url="http://restapi:5555/trades")
        logger.info("   [+] Trades API response: {0}".format(response.json()))

        trades = response.json()
        for index, trade_item in enumerate(trades):
            report_mesage = fix.Message()
            report_mesage.getHeader().setField(fix.BeginString(fix.BeginString_FIX50))
            report_mesage.getHeader().setField(fix.MsgType(fix.MsgType_TradeCaptureReport))
            report_mesage.setField(fix.ApplID(index))
            report_mesage.setField(fix.ApplSeqNum(index))
            report_mesage.setField(fix.TradeReportID("TRADE-REPORT-ID"))
            report_mesage.setField(fix.TradeID(trade_item["trade_id"]))
            report_mesage.setField(fix.TradeReportTransType(TRADE_TRANSACTION_TYPE[trade_item["trade_report_transaction_type"]]))
            report_mesage.setField(fix.TrdType(0))  # Regular trade
            report_mesage.setField(fix.TransactTime(trade_item["transact_type"]))
            report_mesage.setField(fix.LastPx(trade_item["traded_price"]))
            report_mesage.setField(fix.LastQty(trade_item["traded_quantity"]))
            report_mesage.setField(fix.Yield(trade_item["trade_yield_percentage"]))
            report_mesage.setField(fix.SecurityID(trade_item["security_id"]))

            try:
                fix.Session.sendToTarget(report_mesage, self.session_id)

            except Exception:
                logger.info("[!!!] Session Not found!")

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
            logger.info("   [+] Bonds API response: {0}".format(response.json()))

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


