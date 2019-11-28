import socket
udp_ip = '127.0.0.1'
udp_porta = 6156
msg = 'marcelo 127.0.0.2'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.sendto(msg.encode(), (udp_ip, udp_porta))
sock.close()