class CheeseProtocol:
    # TRACKER_HOST = '0.0.0.0'
    TRACKER_HOST = '127.0.0.1'
    TRACKER_PORT = 9999
    INVALIDPEERID = "INVALIDPEERID"
    PCONNECT = "PCONNECT"
    PCONNECTACK = "PCONNECTACK"
    TCONNECTACK = "TCONNECTACK"
    GETCHAIN = "GETCHAIN"
    GETCHAINACK = "GETCHAINACK"
    GETOPENTRANSACTIONS = "GETOPENTRANSACTIONS"
    GETOPENTRANSACTIONSACK = "GETOPENTRANSACTIONSACK"
    GETPEERS = "GETPEERS"
    GETPEERSACK = "GETPEERSACK"

    BRCHEESE = "BRCHEESE"
    BRCHEESEACK = "BRCHEESEACK"

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
        # for tracker
        if request_body.startswith(CheeseProtocol.PCONNECT):
            return CheeseProtocol.PCONNECT
        if request_body.startswith(CheeseProtocol.GETPEERS):
            return CheeseProtocol.GETPEERS
        # for peers
        if request_body.startswith(CheeseProtocol.GETCHAIN):
            return CheeseProtocol.GETCHAIN
        if request_body.startswith(CheeseProtocol.BRCHEESE):
            return CheeseProtocol.BRCHEESE

    @staticmethod
    def validate_request(request_body, connected_peers):
        request_body = request_body.split(':')
        request_type = request_body[0]
        peer_id = request_body[1]

        for peer_data in connected_peers:
            if peer_data['peer_id'] == peer_id:
                return peer_data

        return False


