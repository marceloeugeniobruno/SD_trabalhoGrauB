import os
from getpass import getpass
from ftplib import FTP

nonpassive = False
nomearquivo = 'README'
dir_nome = 'pasta'
ip = '127.0.0.1'
usua = []
print('conectando')
conexao = FTP(ip)
