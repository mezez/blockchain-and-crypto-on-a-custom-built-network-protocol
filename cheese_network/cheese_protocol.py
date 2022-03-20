class CheeseProtocol:
    # TRACKER_URL = '192.168.43.188'
    TRACKER_URL = 'localhost'
    TRACKER_HOST = '0.0.0.0'
    # TRACKER_HOST = '127.0.0.1'
    TRACKER_PORT = 9999
    INVALIDPEERID = "INVALIDPEERID"
    PCONNECT = "PCONNECT"
    PCONNECTACK = "PCONNECTACK"
    TCONNECTRESP = "TCONNECTRESP"
    GETCHAIN = "GETCHAIN"
    GETCHAINRESP = "GETCHAINRESP"
    GETOPENTRANSACTIONS = "GETOPENTRANSACTIONS"
    GETOPENTRANSACTIONSRESP = "GETOPENTRANSACTIONSRESP"
    GETPEERS = "GETPEERS"
    GETPEERSRESP = "GETPEERSRESP"

    BRCHEESE = "BRCHEESE"
    BRCHEESEACK = "BRCHEESEACK"

    BRTRANSACTION = 'BRTRANSACTION'
    BRTRANSACTIONACK = 'BRTRANSACTIONACK'

    BRACCEPT = "BRACCEPT"
    BRREJECT = "BRREJECT"

    HCK = "HCK"
    HCKACK = "HCKACK"

    peer_id_start_string = "PID"
    connected_peers_start_string = "CPSS"
    chain_start_string = "CHAIN"
    transaction_start_string = "TR"


    @staticmethod
    def process_peer_request(request_body):
        if request_body.startswith(CheeseProtocol.PCONNECT):
            return CheeseProtocol.PCONNECT
        if request_body.startswith(CheeseProtocol.PCONNECTACK):
            return CheeseProtocol.PCONNECTACK
        if request_body.startswith(CheeseProtocol.TCONNECTRESP):
            return CheeseProtocol.TCONNECTRESP
        if request_body.startswith(CheeseProtocol.GETPEERS):
            return CheeseProtocol.GETPEERS
        if request_body.startswith(CheeseProtocol.GETPEERSRESP):
            return CheeseProtocol.GETPEERSRESP
        if request_body.startswith(CheeseProtocol.GETCHAIN):
            return CheeseProtocol.GETCHAIN
        if request_body.startswith(CheeseProtocol.GETCHAINRESP):
            return CheeseProtocol.GETCHAINRESP
        if request_body.startswith(CheeseProtocol.GETOPENTRANSACTIONS):
            return CheeseProtocol.GETOPENTRANSACTIONS
        if request_body.startswith(CheeseProtocol.GETOPENTRANSACTIONSRESP):
            return CheeseProtocol.GETOPENTRANSACTIONSRESP
        if request_body.startswith(CheeseProtocol.BRCHEESE):
            return CheeseProtocol.BRCHEESE
        if request_body.startswith(CheeseProtocol.BRCHEESEACK):
            return CheeseProtocol.BRCHEESEACK
        if request_body.startswith(CheeseProtocol.BRTRANSACTION):
            return CheeseProtocol.BRTRANSACTION
        if request_body.startswith(CheeseProtocol.BRTRANSACTIONACK):
            return CheeseProtocol.BRTRANSACTIONACK

    @staticmethod
    def validate_request(request_body, connected_peers):
        request_body = request_body.split(':')
        request_type = request_body[0]
        peer_id = request_body[1]

        for peer_data in connected_peers:
            if peer_data['peer_id'] == peer_id:
                return peer_data

        return False


