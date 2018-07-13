# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 22:37:39 2018

@author: toto
"""


###CLASS FOR SENDING RECEIVING MESSAGE OF ANY LENGHT AND BYTES OF DATA THAT MUST BE STORED INTO A FILE

class communicator:
    def __init__(self , sockLocal):
        self.sockLocal = sockLocal 
        self.packetLen = 0
        self.clearMessage = ""
        self.encodedMessage = ""
        self.encoder = "utf-8"
        
    def calculateLenght(self , message):
        self.encodedMessage = message.encode(self.encoder)
        self.packetLen = len(self.encodedMessage)
        return self.packetLen 
    
    
    def send(self , mess ):
        #print("DEBUG -> Message to send = " , mess)
        
        self.sockLocal.send(str(self.calculateLenght(mess)).encode(self.encoder))
        #print("DEBUG -> Packet Lenght = " , self.packetLen)
        confirm = self.sockLocal.recv(16).decode(self.encoder)
        #print("DEBUG -> Confirmation received -> " , confirm)
        self.sockLocal.send(mess.encode(self.encoder))
    
    def receive(self):
        #print("DEBUG ->  Preparing to receive a packet ")
        lenght = int(self.sockLocal.recv(16).decode(self.encoder))
        #print("DEBUG -> Packet lenght = " , lenght)
        self.sockLocal.send("ACK".encode(self.encoder))
        #print("DEBUG -> ACK sended ")
        recv = self.sockLocal.recv(lenght).decode(self.encoder)
        #print("DEBUG -> message Received = " , recv )
        return recv 
    
    def sendBytes(self , byte):
        #self.sockLocal.send(str(len(byte)).encode(self.encoder))
        #print("DEBUG -> len of file = " , len(byte))
        #self.sockLocal.recv(16).decode(self.encoder)
        #print("DEBUG -> ACK received ")
        self.sockLocal.send(byte)
        #print("DEBUG -> BYTES SENDED ")
    
    def receiveBytes(self , pathToStore):
        #lenght = int(self.sockLocal.recv(16).decode(self.encoder))
        #print("DEBUG -> Bytes to receive = " , lenght)
        #self.sockLocal.send("ACK".encode(self.encoder))
        #print("DEBUG -> ACK SENDED")
        f = open(pathToStore , "wb")
        temp = b''
        while( True):
            temp = self.sockLocal.recv(1024)
            f.write(temp)
            if (len(temp) < 1024):
                break
        f.close()
   
        #recv = self.sockLocal.recv(lenght)
        #print("DEBUG -> TOTAL BYTES RECEIVED  = " , len(data))
        

    