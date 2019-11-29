from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# change 'user' to your user name and directory!
authorizer = DummyAuthorizer()
authorizer.add_user("user", "8231335704", "Uploadalunos", perm="elradfmw")
authorizer.add_anonymous("Uploadalunos", perm="elradfmw")

handler = FTPHandler
handler.authorizer = authorizer

server = FTPServer(("127.0.0.1", 6157), handler) #host goes here
server.serve_forever()