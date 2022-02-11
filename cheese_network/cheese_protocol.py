class CheeseProtocol:
    TRACKER_HOST = '0.0.0.0'
    TRACKER_PORT = 9999
    INVALID_PEER_ID_RESPONSE = "INVALID_PEER_ID"
    join_chain = "JOIN_CHAIN"
    get_chain = "GET_CHAIN"
    get_peers = "GET_PEERS"
    new_cheese = "NEW_CHEESE"


    @staticmethod
    def process_peer_request(request_body):
        # for tracker
        if request_body.startsWith(CheeseProtocol.join_chain):
            return CheeseProtocol.join_chain
        if request_body.startsWith(CheeseProtocol.get_peers):
            return CheeseProtocol.get_peers
        # for peers
        if request_body.startsWith(CheeseProtocol.get_chain):
            return CheeseProtocol.get_chain
        if request_body.startsWith(CheeseProtocol.new_cheese):
            return CheeseProtocol.new_cheese

    @staticmethod
    def validate_request(request_body, connected_peers):
        request_body = request_body.split(':')
        request_type = request_body[0]
        peer_id = request_body[1]

        for peer_data in connected_peers:
            if peer_id in peer_data.keys():
                return peer_data

        return False


