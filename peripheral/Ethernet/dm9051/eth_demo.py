import ethernet
import usocket

dm9051 = ethernet.DM9051(b'\x12\x34\x56\x78\x9a\xbc','192.168.31.115', '', '')
dm9051.set_dns('8.8.8.8', '114.114.114.114')
dm9051.set_up()

sock = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
sockaddr=usocket.getaddrinfo('www.tongxinmao.com', 80)[0][-1]
print(sockaddr)
sock.connect(sockaddr)
ret=sock.send('GET /News HTTP/1.1\r\nHost:www.tongxinmao.com\r\nAccept-Encoding: deflate\r\nConnection: keep-alive\r\n\r\n')
data=sock.recv(256)
print(data.decode())
sock.close()
