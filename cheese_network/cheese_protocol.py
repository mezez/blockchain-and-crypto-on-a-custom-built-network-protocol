class CheeseProtocol:
    TRACKER_PORT = 9999
    join_chain = "JOIN_CHAIN"
    get_chain = "GET_CHAIN"
    get_peers = "GET_PEERS"


    @staticmethod
    def process_client_request(request_body):
        if request_body == CheeseProtocol.join_chain:
            return CheeseProtocol.join_chain
        if request_body == CheeseProtocol.get_chain:
            return CheeseProtocol.get_chain
        if request_body == CheeseProtocol.get_peers:
            return CheeseProtocol.get_peers


