#!/usr/bin/python
# Author : Dani Carbonell
# Date   : 14.12.2012
import sys, os, time
import subprocess
from subprocess import Popen #, list2cmdline
import logging
logger = logging.getLogger('root')
import pytrnsys.trnsys_util.LogTrnsys as LogTrnsys

#from __future__ import print_function 


def getNumberOfCPU():
    ''' Returns the number of CPUs in the system
    '''
    num = 1
    if sys.platform == 'win32':
        try:
            num = int(os.environ['NUMBER_OF_PROCESSORS'])
        except (ValueError, KeyError):
            pass
    elif sys.platform == 'darwin':
        try:
            num = int(os.popen('sysctl -n hw.ncpu').read())
        except ValueError:
            pass
    else:
        try:
            num = os.sysconf('SC_NPROCESSORS_ONLN')
        except (ValueError, OSError, AttributeError):
            pass

    return num           
       
def getCpuHexadecimal(cpu):

#    Core # = Decimal = Hexadecimal = BitMask
#    Core 1 = 1 = 01 = 00000001
#    Core 2 = 2 = 02 = 00000010
#    Core 3 = 4 = 04 = 00000100
#    Core 4 = 8 = 08 = 00001000
#    Core 5 = 16 = 10 = 00010000
#    Core 6 = 32 = 20 = 00100000
#    Core 7 = 64 = 40 = 01000000
#    Core 8 = -128 = 80 = 10000000

    if(cpu==1):   return 1
    elif(cpu==2): return 2
    elif(cpu==3): return 4
    elif(cpu==4): return 8
    elif(cpu==5): return 10
    elif(cpu==6): return 20
    elif(cpu==7): return 40
    elif(cpu==8): return 80
    elif (cpu == 9):
        return 100
    elif (cpu == 10):
        return 200
    elif (cpu == 11):
        return 400
    else:
        raise ValueError("CPU not existent:%d"%cpu)
        
def runParallel(cmds,reduceCpu=0,outputFile=False,estimedCPUTime=0.33,delayTime=0.3):
    ''' Exec commands in parallel in multiple process 
    (as much as we have CPU)
    '''
    maxNumberOfCPU = max(min(getNumberOfCPU() - reduceCpu,len(cmds)),1)
    newCmds = []
    
    #################### new code
#   initialize dictionary with processes for each core:
    cP = {}
    
    for i in range(maxNumberOfCPU):
        cP['cpu'+str(i+1)]={'cpu':i+1, 'cmd':[], 'process':[], 'case':[]}
        

    #############################
    
    if(outputFile!=False):
#        k=0
        lines = ""
        line  = "============PARALLEL PROCESSING STARTED==============\n";lines=lines+line
        line  = "Number of simulated cases =%d\n"%len(cmds);lines=lines+line
        line  = "Number of CPU used =%d\n"%maxNumberOfCPU;lines=lines+line
        line  = "Estimated time =%f hours, assuming :%f hour per simulation\n"%(len(cmds)*estimedCPUTime/(maxNumberOfCPU*1.0),estimedCPUTime);lines=lines+line
        line  = "============CASES TO BE SIMULATED====================\n";lines=lines+line
        
        i=1
        for cmd in cmds:
            case = cmd.split("\\")[-1]
            line = "Case %d to be simulated %s\n"%(i,case); lines=lines+line
            i=i+1
        line  = "============ALREADY SIMULATED CASES====================\n";lines=lines+line
            
        outfileRun=open(outputFile,'w')    
        outfileRun.writelines(lines)                
        outfileRun.close()

#    cmdExe = os.getenv("COMSPEC")
    
    cpu = 1
    
    for cmd in cmds:                
#        newCmds.append("%s start /affinity %s "%(cmdExe,getCpuHexadecimal(cpu)) + cmd)
#        newCmds.append("start /affinity %s "%(getCpuHexadecimal(cpu)) + cmd)

        newTask = "start /wait /affinity %s "%(getCpuHexadecimal(cpu)) + cmd

        newCmds.append(newTask)

        if(cpu < maxNumberOfCPU):
            cpu = cpu+1
        else:
            cpu = 1      
            
            
    if not newCmds: return # empty list
    
    #####################
    # alternative code:
    

    #list of commands that have not yet been executed:
    openCmds = cmds[:]
    
    #list of commands that have already executed:
    finishedCmds = []
    
    #count cases:
    caseNr = 1
        
    #list to check when finished:
    activeP = [0] * maxNumberOfCPU
    
    for core in cP.keys():
        # print cP[core]
        
        cP[core]['cmd']= "start /wait /affinity %s "%(getCpuHexadecimal(cP[core]['cpu'])) + openCmds.pop(0)
        cP[core]['case']=caseNr
        caseNr +=1


        
    #########################
     
            

    def done(p):

        return p.poll() is not None
    
    def success(p):

        fullDckFilePath = p.args.split(" ")[-2]
        (logFilePath,dckFileName) = os.path.split(fullDckFilePath)
        logFileName = os.path.splitext(dckFileName)[0]
        logInstance = LogTrnsys.LogTrnsys(logFilePath,logFileName)

        if logInstance.logFatalErrors():
            logger.error("======================================")
            logger.error("First fatal error message in log file:")
            logger.error("======================================")
            errorList = logInstance.logFatalErrors()
            for line in errorList:
                logger.error(line.replace("\n",""))
        else:
            logger.info("No fatal errors during simulation")
            logger.warning("Number of warnings during simulation: %s" %logInstance.checkWarnings())
            logger.info("Simulation of %s successful" %dckFileName)

        return p.returncode == 0

    def fail():
        logger.warning("PARALLEL RUN HAS FAILED")
        sys.exit(1)

    processes = []
    
    if(len(processes)>maxNumberOfCPU):
        logger.warning("You are triying tu run %d processes and only have %d CPU\n" % (len(processes),maxNumberOfCPU))
        
#    while True:
        
#        cpu = 1
        
        
        
        ###############
        #alternative code:
#        while openCmds:
        
    running = True
    
    while running:
        
        for core in cP.keys():
            
            p = cP[core]['process']
            # start processes:
            if (not p) and cP[core]['cmd']:
                cP[core]['process']= Popen(cP[core]['cmd'],stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
                
                activeP[cP[core]['cpu']-1] = 1

                time.sleep(delayTime) # we delay 5 seconds for each new running to avoid that they read the same source file.
                
            # if process is finished, assign new command:
            
            if p:

                if done(p):
                    
                    if success(p):
                        if(outputFile!=False):
    #                        lines = "Finished simulated case %d\n"%(k,p.stdout.read(),p.stderr.read())
                            lines = "Finished simulated case %d at %s\n"%(cP[core]['case'],time.strftime("%H:%M:%S of day %d-%m-%y"))
                            outfileRun=open(outputFile,'a')    
                            outfileRun.writelines(lines)                
                            outfileRun.close()
                        
                        # empty process:
                        cP[core]['process']=[]
                        finishedCmds.append(cP[core]['cmd'])
                        cP[core]['cmd'] = []
                        cP[core]['case'] = []
                        
                        activeP[cP[core]['cpu']-1] = 0
    
                        
                        # assign new command if there are open commands:
                        
                        if openCmds:
                            cP[core]['cmd']= "start /wait /affinity %s "%(getCpuHexadecimal(cP[core]['cpu'])) + openCmds.pop(0)
                            cP[core]['case']=caseNr
                            caseNr +=1
                            activeP[cP[core]['cpu']-1] = 1
    
                        
    
                    else:
                        # print ('p')%p
    #                    print 'processes', processes
                        fail()

#        
#        for 
#             processes.append(Popen(newTask,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True))
#            newTask = "start /wait /affinity %s "%(getCpuHexadecimal(cpu)) + openCmds.pop(0)
#            
#            currentCmds.append(newTask)

        #############
        
        
        
#        while newCmds and len(processes) < maxNumberOfCPU:
                        
            #use the first value of the vector and erase it from cmds 
#            newTask = newCmds.pop(0)
            
#            print "RunParallel task:%s of nParallelProcesses:%d" % (task,len(processes))

#            newTask = "start /wait /affinity %s "%(getCpuHexadecimal(cpu)) + task

#            cpu =cpu+1
    
#            processes.append(Popen(newTask,stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True))

#        print "PROCESSES"
#        print processes
        
#        for p in processes:
#        
##            o,e = p.communicate()
##            print o
##            print "for p in process %d"%p.poll()
#            
##                print "%s returnCode=NONETYPE"%p
#            if done(p):
#                
#                if success(p):
#                    if(outputFile!=False):
##                        lines = "Finished simulated case %d\n"%(k,p.stdout.read(),p.stderr.read())
#                        lines = "Finished simulated case %d\n"%(k+1)
#                        outfileRun=open(outputFile,'a')    
#                        outfileRun.writelines(lines)                
#                        outfileRun.close()
#                        k=k+1
#                    processes.remove(p)
#                    
#
#                else:
#                    print 'p', p
#                    print 'processes', processes
#                    fail()
#                
                    

        if all(process == 0 for process in activeP) and not openCmds:
                   
#        if not processes and not newCmds:
            break
        else:
            time.sleep(0.05)
        
def sortCommandList(cmds, keyWord):

    """
    function to put all commands that contain a keyWord string on top of a command list, so they will be evaluated first.

    Parameters
    ----------
    cmds : list of strings
        includes all commands to be evaluated

    keyWord : string
        acts as filter; commmands including this string will be evaluated first

    Returns
    -------
    cmdsNew : list of strings
        all commands to be evaluated in new order
    """

    cmdsNew = []

    for line in cmds:
        if keyWord in line:
            cmdsNew.insert(0, line)
        else:
            cmdsNew.append(line)

    return cmdsNew

