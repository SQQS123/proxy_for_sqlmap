# -*-coding:utf-8-*-
import socket
from socket import error
import threading
import random
import time
import requests


localtime = time.asctime(time.localtime(time.time()))


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/").json()

def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


class ProxyServerTest():

    def __init__(self):
        #本地socket服务
        self.ser=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_proxyip()

    def set_proxyip(self):
        self.proxyip = get_proxy().get("proxy")

    def run(self):
        try:
            #本地服务IP和端口
            self.ser.bind( ('127.0.0.1', 9998) )
            #最大连接数
            self.ser.listen(5)
        except error as e:
            print("[-]The local service : " + str(e))
            return "[-]The local service : " + str(e)
        while True:
            try:
                #接收客户端数据
                client, addr = self.ser.accept()
                print( '[*]accept %s connect' % (addr,) )
                data = client.recv(1024)
                if not data:
                    break
                print('[*' + localtime + ']: Accept data...')
            except error as e:
                print("[-]Local receiving client : " + str(e))
                return "[-]Local receiving client : " + str(e)
            while True:
                #目标代理服务器，将客户端接收数据转发给代理服务器
                mbsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print("[!]Now proxy ip:" + str(self.proxyip))
                proxyip = self.proxyip.split(":")
                prip = proxyip[0]
                prpo = int(proxyip[1])
                try:
                    mbsocket.settimeout(3)
                    mbsocket.connect((prip,prpo))
                except:
                    print("[-]RE_Connect...")
                    self.set_proxyip()
                    continue
                break
#                   except :
#                       print("[-]Connect failed,change proxy ip now...")
#                       pass
            try:    
                mbsocket.send(data)
            except error as e:
                print("[-]Sent to the proxy server : "+str(e))
                return "[-]Sent to the proxy server : "+str(e)

            
            while True:
                try:
                    #从代理服务器接收数据，然后转发回客户端
                    data_1 = mbsocket.recv(1024)
                    if not data_1:
                        break
                    print('[*' + localtime + ']: Send data...')
                    client.send(data_1)
                except socket.timeout as e:
                    print(proxyip)
                    print("[-]Back to the client : " + str(e))
                    continue
            #关闭连接
            client.close()
            mbsocket.close()


def Loadips():
    print("[*]Loading proxy ips..")
    ip_list = []
    ip = ['ip','port']
    with open("ips.txt") as ips:
        lines = ips.readlines()
    for line in lines:
        ip[0], ip[1] = line.strip().split(":")
        ip[1] = eval(ip[1])
        nip = tuple(ip)
        ip_list.append(nip)
    return ip_list

    

def main():
    print('''
*Atuhor : 749804235@qq.com.

                         __     __    _       _____ ____    
                         \ \   / /_ _/ |_ __ |___ /|  _ \  
                          \ \ / / _` | | '_ \  |_ \| |_) |  
                           \ V / (_| | | | | |___) |  _ < _
                            \_/ \__,_|_|_| |_|____/|_| \_(_)


    ''')
    # ip_list = Loadips()    
#   ip_list = [('118.89.148.92',8088)]
#   ip_list = tuple(ip_list)
    try:
        pst = ProxyServerTest()
        #多线程
        t = threading.Thread(target=pst.run, name='LoopThread')
        print('[*]Waiting for connection...')
        #关闭多线程
        t.start()
        t.join()
    except Exception as e:
        print("[-]main : " + str(e))
        return "[-]main : " + str(e)



if __name__=='__main__':
    main()
