from ftplib import FTP

ftp = FTP('')
ftp.connect('127.0.0.1', 6157)  # address to connect goes here
ftp.login()
ftp.cwd('')  # replace with your directory
ftp.retrlines('LIST')