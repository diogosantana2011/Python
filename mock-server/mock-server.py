from flask import Flask, jsonify, request
import os, signal, threading, random, decimal, uuid, datetime, random

payment_data={}

class MockServer:
    def __init__(self, port=5000):
        self.app = Flask(__name__)
        self.app.name = 'Cashier Server'
        self.port = port
        self.setup_routes()
        self.server_thread = None
        self.app.debug = True

    def setup_routes(self):
        """
        Configure routes for mock server
        """

        @self.app.route('/alive', methods=['GET'])
        def alive():
            """
            Endpoint to check the liveliness of the server.
            Returns a JSON response indicating that the server is running.
            """
            return jsonify({'message': 'Server is running'}), 200

        @self.app.route('/negative')
        def negative_route():
            """
            Dummy endpoint to demonstrate a negative response (status code 400).
            Returns a JSON response indicating that this is a negative response.
            """
            return jsonify({"message":'This is a negative response'}), 400
        
        @self.app.route('/post', methods=['POST'])
        def post_route():
            """
            Dummy POST example. Via postman, 'success' value must be bool: true/false
            """
            expected_payload = {"success": True, "message": "This was sent via POST call"}
            received_payload = request.json

            if received_payload == expected_payload:
                return jsonify({"success": True, "message": "Successful POST request"}), 200
            else:
                return jsonify({"success": False, "error": "Invalid payload"}), 400
        
        # SHUTDOWN
        @self.app.route('/shutdown', methods=['POST'])   
        def stop_server():
            """
            Handles a request to shut down the server.

            Expects a JSON payload with a 'message' and 'shutdown' key indicating the shutdown request.
            Initiates a shutdown process by sending a response and shutting down the server in separate threads.
            
            Examples:
            - Call method: 'POST'
            - Body: {"message": "signal shutdown", "shutdown": "true"} - 200 OK
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

        ## AQUAPAY USER BALANCE EXAMPLE
        @self.app.route('/users/v1/userbalance', methods=['GET'])
        def getUserBalance():
            """
            Simulates an Aquapay endpoint to retrieve user balance information.
            Returns a JSON response with user balance details.
            
            Path: /users/v1/userbalance
            @returns object with balance details.
            """
            random_decimal = float(decimal.Decimal(random.randrange(10, 460))/1000)

            return jsonify({
                    "pendingTransfer": 0,
                    "totalBalance": random_decimal,
                    "availableBalance": random_decimal,
                    "symbol": "BTC",
                    "updatedAt": 1569964868574,
                    "depositAddress": "-"
                })
        
        ## NETELLER
        # DEPOSIT
        @self.app.route('/cashier/neteller/deposit', methods=['POST'])
        def deposit_neteller():
            """
            Simulates a Neteller deposit transaction.

            Expects a JSON payload with 'amount' and 'email' keys.
            Generates a unique ID and internal ID for the transaction.
            Stores payment data in an in-memory dictionary.
            Returns a JSON response indicating the status of the deposit transaction.
            """
            required_keys = ['amount', 'email']
            received_payload = request.json
            if not received_payload or not all(key in received_payload for key in required_keys):
                return jsonify({"success": False, "error": "Invalid payload"}), 400

            # Generate unique IDs for the transaction
            id = random.randint(1000, 9999)
            payment_id = str(uuid.uuid4())

            # Store payment data in the in-memory dictionary
            amount = received_payload['amount']
            email = received_payload['email']
            payment_data[payment_id] = {
                "id": id,
                "internalId": payment_id,
                "amount": amount,
                "email": email
            }

            # Construct and return the response
            response = {
                "approval": "PROCESSING",
                "amount": amount,
                "email": email,
                "internalId": payment_id,
                "id": id,
                "payment_info": payment_data
            }
            return jsonify(response), 200
        
        # Necessary?
        @self.app.route('/manageFunding/neteller/success', methods=['GET'])
        def deposit_neteller_success():
            """
                Dummy endpoint to handle Neteller deposit success.
                Returns a message indicating that JavaScript needs to be enabled.
            """
            return "You need to enable JavaScript to run this app."
        
        # FINISH PAYMENT
        @self.app.route('/mercury/api2/cashier/neteller/paysafe/finishPayment/<string:payment_id>', methods=['POST'])
        def finish_payment(payment_id):
            """
            Simulates an endpoint for completing a payment transaction.

            Example: '/mercury/api2/cashier/neteller/paysafe/finishPayment/{payment_id}'
            
            Expects the payment ID in the URL path.
            Retrieves payment information from the in-memory payment data store based on the payment ID.
            If the payment information is found and complete, returns a successful response.
            Otherwise, returns an error response indicating that the payment ID was not found.
            """
            if payment_id not in payment_data:
                return jsonify({
                    "success": False,
                    "error": "Internal ID not found",
                    "paymentId": payment_id,
                    "paymentData": payment_data
                }), 404

            # Retrieve payment information
            payment_info = payment_data[payment_id]
            try:
                amount = payment_info['amount']
                email = payment_info['email']
                internal_id = payment_info['internalId']
                id = payment_info['id']
            except KeyError:
                return jsonify({
                    "success": False,
                    "error": "Missing key in payment info",
                    "paymentId": payment_id,
                    "paymentData": payment_info
                }), 500

            response = {
                "approval": "COMPLETED",
                "amount": amount,
                "email": email,
                "id": id,
                "internalId": internal_id
            }
            return jsonify(response), 200
        
        # PAYMENT HANDLE
        @self.app.route('/paymenthub/v1/paymenthandles', methods=['POST'])
        def neteller_payment_handle():
            received_payload = request.json
            neteller_uuid = uuid.uuid4()
            payment_handle_token = uuid.uuid4()
            now = datetime.datetime.utcnow()
            txn_time = now.replace(microsecond=0).isoformat() + "Z"
            updated_time = txn_time
            status_time = txn_time
            expected_keys = ['merchantRefNum', 'transactionType', 'neteller', 'paymentType', 'amount', 'currencyCode',
                     'customerIp', 'billingDetails', 'returnLinks']
            
            response={
                "id": neteller_uuid,
                "paymentType":"NETELLER",
                "paymentHandleToken": payment_handle_token,
                "merchantRefNum":"65eb1f34-5728-4d8b-a315-618d05a2133c",
                "currencyCode": received_payload['currencyCode'],
                "dupCheck": True,
                "status": "INITIATED",
                "liveMode":True,
                "usage":"SINGLE_USE",
                "action":"REDIRECT",
                "executionMode":"SYNCHRONOUS",
                "amount": received_payload['amount'],
                "billingDetails":{
                    "street":received_payload['billingDetails']['street'],
                    "street2":received_payload['billingDetails']['street2'],
                    "city":received_payload['billingDetails']['city'],
                    "zip":received_payload['billingDetails']['zip'],
                    "country":received_payload['billingDetails']['country']
                },
                "customerIp":received_payload['customerIp'],
                "timeToLiveSeconds": random.randint(111, 999),
                "gatewayResponse":{
                    "orderId": f"ORD_${uuid.uuid4()}",
                    "totalAmount":3599,
                    "currency": received_payload['currencyCode'],
                    "status":"pending",
                    "lang":"en_US",
                    "processor":"NETELLER"
                },
                "neteller":{
                    "consumerId": received_payload['neteller']['consumerId'],
                    "detail1Description": received_payload['neteller']['detail1Description'],
                    "detail1Text":received_payload['neteller']['detail1Text']
                },
                "returnLinks":[
                    {
                        "rel": "on_completed",
                        "href": "https://jenkins.3et.com/manageFunding/neteller/success"
                    },
                    {
                        "rel": "on_failed",
                        "href": "https://jenkins.3et.com/manageFunding/neteller/error"
                    },
                    {
                        "rel": "default",
                        "href": "https://jenkins.3et.com/manageFunding"
                    }
                ],
                "txnTime": txn_time,
                "updatedTime": updated_time,
                "statusTime": status_time,
                "links":[
                    {
                        "rel":"redirect_payment",
                        "href":"https://jenkins.3et.com/manageFunding/neteller/success"
                    }
                ]
            }

            if not received_payload or not all(key in received_payload for key in expected_keys):
                return jsonify({"success": False, "error": "Invalid payload"}), 400
            else:
                return jsonify(response)

    # SHUTDOWN
    def send_shutdown_response(self):
        """
        Method is called in the response_thread to send the JSON response
        """
        print("Sending shutdown request...")

    def shutdown_server(self):
        """
        Method which contains the logic to shut down the server
        and is called in the shutdown_thread.
        Based on 'os' getpid() and killing running process.
        """
        print('Server has shutdown.')
        os.kill(os.getpid(), signal.SIGINT)

    # START  
    def start(self):
        print(' * Server has started.')
        self.server_thread = threading.Thread(target=self.app.run(), kwargs={})
        self.server_thread.start()

if __name__ == '__main__':
    server = MockServer()
    server.start()
