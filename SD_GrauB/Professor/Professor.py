import threading
import os
import socket
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

udp_ip = '127.0.0.1'
udp_porta = 6156
ftp_upload = 6157
ftp_download = 6158
lista_de_alunos = [('Marcelo', '127.0.0.2', 6156)]


class FTPupload(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        authorizer = DummyAuthorizer()
        # TODO: fazer codificação para ajustar os usuários
        authorizer.add_user("user", "8231335704", "Uploadalunos", perm="elradfmw")
        authorizer.add_anonymous("Uploadalunos", perm="elradfmw")
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer((udp_ip, ftp_upload), handler)  # host goes here
        server.serve_forever()


class FTPdownload(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        authorizer = DummyAuthorizer()
        authorizer.add_user("user", "8231335704", "pasta", perm="elradfmw")
        authorizer.add_anonymous("pasta", perm="elradfmw")
        handler = FTPHandler
        handler.authorizer = authorizer
        server = FTPServer((udp_ip, ftp_download), handler)  # host goes here
        server.serve_forever()


class UDPrec(threading.Thread):
    def __init__(self, ip, porta):
        threading.Thread.__init__(self)
        self.ip = ip
        self.porta = porta
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def run(self):
        self.sock.bind((udp_ip, udp_porta))
        try:
            while True:
                data, addr = self.sock.recvfrom(1024)
                print(f'menensagem recebida de : {data}')
        except:
            print('erro de conexão')
        print('tread UDP')


class Varredura(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):

        arquivos = list(os.scandir('pasta'))
        arquivos2 = []
        arquivo = None
        while len(arquivos) == 0:
            arquivos = list(os.scandir('pasta'))
        li = []
        if len(arquivos) > 0:
            faz = False
            for i in range(0, len(arquivos)):
                li.append((arquivos[i].stat().st_mtime, arquivos[i].name))
                faz = True
            arquivos2 = None
            while faz:
                arquivos2 = list(os.scandir('pasta'))
                """
                Verifica se ha modificação na pasta oou atualização de arquivo
                """
                if len(arquivos) == len(arquivos2):
                    for j in range(0, len(arquivos2)):
                        # print(f' arquivo 1 {li[j][0]} o 2 {arquivos2[j].stat().st_mtime} ')
                        if li[j][0] != arquivos2[j].stat().st_mtime:
                            print('Houve atualização!')
                            faz = False
                else:
                    print(f'Houve alterção no número de arquivos!')
                    faz = False
            arquivo = None
            for i in range(0, len(arquivos2)):
                k = True
                for j in range(len(li)):
                    if li[j][1] == arquivos2[i].name:
                        k = False
                        if li[j][0] != arquivos2[i].stat().st_mtime:
                            arquivo = arquivos2[i]
                            print(f'arquivo atualizado  {arquivos2[i].name}')
                        else:
                            j = len(arquivos2)
                if k:
                    arquivo = arquivos2[i]
                    i = len(arquivos2)
        for i in range(0, len(lista_de_alunos)):
            msg = f'Arquivo_atualizado {arquivo.name}'
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.sendto(msg.encode(), (lista_de_alunos[i][1], lista_de_alunos[i][2]))
            sock.close()
        # TODO: FTP para as pastas dos alunos


tread_FTP = FTPupload()
tread_FTP_d = FTPdownload()
tread_UDP = UDPrec(udp_ip, udp_porta)
tread_var = Varredura()

tread_FTP.start()
tread_FTP_d.start()
tread_UDP.start()
tread_var.start()

treads = [tread_var, tread_UDP,tread_FTP, tread_FTP_d]

for t in treads:
    t.join()
