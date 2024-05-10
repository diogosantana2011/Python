from flask import Flask, jsonify, request
import os, signal, threading, random, decimal

class MockServer:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()
        self.server_thread = None

    def setup_routes(self):
        """
        Configure routes for mock server
        """
        
        ## AQUAPAY USER BALANCE
        @self.app.route('/users/v1/userbalance', methods=['GET'])
        def getUserBalance():
            """
                MOCK of aquapay get user balance
                Path: /users/v1/userbalance
                @returns object with balance details.
            """
            random_decimal = float(decimal.Decimal(random.randrange(10, 460))/1000)

            return jsonify(
                {
                    "pendingTransfer": 0,
                    "totalBalance": random_decimal,
                    "availableBalance": random_decimal,
                    "symbol": "BTC",
                    "updatedAt": 1569964868574,
                    "depositAddress": "-"
                }
            )

        @self.app.route('/alive', methods=['GET'])
        def test_route():
            """
                TODO: Implement logic from gist confirming server is running.
                Use this endpoint.
            """
            return jsonify({'message': 'Server is running'}), 200

        @self.app.route('/negative')
        def negative_route():
            """
                Dummy GET example with 400 response.
                TODO: fix if clause as incorrectly always throwing 400
            """
            return jsonify({"message":'This is a negative response'}), 400
        
        @self.app.route('/post', methods=['POST'])
        def post_route():
            """
                Dummy POST example.
            """
            expected_payload = {"success": True, "message": "This was sent via POST call"}
            received_payload = request.json

            if expected_payload == received_payload:
                return jsonify({"message": "success"}), 200
            else:
                return jsonify({"success": False, "error": "Invalid payload"}), 400
        
        # SHUTDOWN
        @self.app.route('/shutdown', methods=['POST'])   
        def stop_server():
            """
                Call method: 'POST',
                Body: {"message": "signal shutdown", "shutdown": "true"} - 200 OK
                Otherwise will throw 500.
                With threading JSON response is returned before shutting down the server.
            """
            expected_payload = {"message": "signal shutdown", "shutdown": "true"}
            received_payload = request.json
            if expected_payload == received_payload:
                response_thread = threading.Thread(target=self.send_shutdown_response)
                response_thread.start()
                shutdown_thread = threading.Thread(target=self.shutdown_server)
                shutdown_thread.start()
                return jsonify({"success": "true", "message": "Shutting down server..."}), 200
            else:
                return jsonify({"success": "false", "error": "FAILED SHUTDOWN REQUEST"}), 500

    # SHUTDOWN
    def send_shutdown_response(self):
        """
           Method is called in the response_thread to send the JSON response
        """
        print("Sending shutdown response...")

    def shutdown_server(self):
        """
            Method which contains the logic to shut down the server
            and is called in the shutdown_thread.
            Based on 'os' getpid() and killing running process.
        """
        os.kill(os.getpid(), signal.SIGINT)

    # START  
    def start(self):
        self.server_thread = threading.Thread(target=self.app.run(), kwargs={'debug': True})
        self.server_thread.start()
