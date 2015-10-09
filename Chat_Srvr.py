#!/usr/bin/env python
#Chat server program that uses TCP sockets as connection endpoints
#It assigns a thread to each individual connection in order to increase efficiency of the server

#import necessary modules

import threading
import socket
from time import localtime,asctime
#logging module is used to debug the program
#Has been commented out after debugging is complete
#import logging

#broadcast function that broadcasts message sent by one of the clients to the rest of the clients
def broadcast(thrd,skt,mssg,hst):
  lcl_tym=localtime()
  tym=asctime(lcl_tym)  
  for t in threads:
    if thrd!=t :
      try:
        fmssg="(%s)From: %s >>>"%(tym,hst)+mssg
        fmssg=fmssg.encode('utf-8')
        skt.send(fmssg)
      except socket.error as e:
        #logging.debug(e.code)
        return



#logging.basicConfig(level=logging.DEBUG,format='[%(asctime)s]  %(message)s', )

#Custom thread class that subclasses Thread class and has custom attributes ie host name,port number and client socket        
class cliThread(threading.Thread):
  def __init__(self,host,port,sockt):
    threading.Thread.__init__(self)
    self.host=host
    self.port=port
    self.sockt=sockt
  def run(self):
    try:
      
      self.crrnt=threading.currentThread()     
      #logging.debug('Connection established successfully to..',host)
      print('Connection established successfully to .....%s'%host)
      self.msg='Welcome to nerdherd chat server'
      self.msg=self.msg.encode('utf-8')
      self.sockt.send(self.msg)
      while True:
        self.data=self.sockt.recv(1024)
        self.data+=self.data
        self.data=self.data.decode('utf-8')
        if self.data == 0:
          logging.debug('connection lost with ',host)
          self.txt="[%s] Connection to %s lost!!"%(asctime,self.host)
          broadcast(self.crrnt,self.sockt,self.text,self.host)
          self.sockt.close()
        #logging.debug('>>>>',data,'>From: ',(host,port))
        broadcast(self.crrnt,self.sockt,self.data,self.host)
              
                     
    finally:
      self.sockt.close()

                 
      
prt=2457
threads=[]
try:
   SrvrSock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
except socket.error:
  #logging.debug('Error!Socket could not be created')
   pass 
SrvrSock.bind(('',prt))
SrvrSock.listen(5)
#semaphore used to control access to server connection pool:max 5 connections
S=threading.Semaphore(5)
#logging.debug('Server listening in for connection...')
print('Connection established successfully')
while True:
   with S:
             cliSock,(host,port)=SrvrSock.accept()
             cli=cliThread(host,port,cliSock)
             cli.start()
             
             threads.append(cli)
             
for t in threads:
      t.join()
    
