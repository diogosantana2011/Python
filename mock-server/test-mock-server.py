from mock_server import MockServer

def mock_server():
    server = MockServer()
    server.start()
    
mock_server()
