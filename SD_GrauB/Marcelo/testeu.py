from ftplib import FTP
from os import rename

ftp = FTP('')
ftp.connect('127.0.0.1', 6157)  # address to connect goes here
ftp.login()
ftp.cwd('')  # replace with your directory
ftp.retrlines('LIST')
# upload to server function


def uploadFile():
    filename = 'Marcelo - ' + 'alu.txt'  # replace with your file in your home folder
    rename('alu.txt', 'Marcelo - ' + 'alu.txt')
    ftp.storbinary('STOR ' + filename, open(filename, 'rb'))
    ftp.quit()

# download from server function
def downloadFile():
    filename = 'alu.txt'  # replace with your file in the directory ('directory_name')
    localfile = open(filename, 'wb')
    ftp.retrbinary('RETR ' + filename, localfile.write, 1024)
    ftp.quit()
    localfile.close()

# uploadFile()
downloadFile()
