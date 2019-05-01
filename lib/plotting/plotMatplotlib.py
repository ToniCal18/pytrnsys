
#!/usr/bin/python

"""
Class to plot using matplotlib

Author : Daniel Carbonell
Date   : 05-05-2018
ToDo :
"""

import matplotlib.pyplot as plt
import numpy as num
import matplotlib
import utilsSpf as utils
import time
import plotGle as gle

class PlotMatplotlib():
    
    def __init__(self):        
    
        self.initialize()
        self.setDefaultColors()

    def initialize(self):

        self.sizeFigX = 10
        self.sizeFigY = 6

        self.sizeLegend = 15
        self.sizeAxis = 15

        self.yearlyFactor = 10

        self.useXLimits = 0
        self.lowXLimit = 0
        self.highXLimit = 1

        self.useYLimits = 0
        self.lowYLimit = 0
        self.highYLimit = 1

    def setXLimits(self,xmin,xmax):

        self.useXLimits = 1
        self.lowXLimit = xmin
        self.highXLimit = xmax

    def setYLimits(self, ymin, ymax):

        self.useYLimits = 1
        self.lowYLimit  = ymin
        self.highYLimit = ymax

    def setDefaultColors(self):

        myColorsIn = plt.rcParams['axes.prop_cycle'].by_key()['color']
        
        self.myColorsIn = myColorsIn+myColorsIn
        self.myColorsOut = self.myColorsIn[::-1]

        self.myColorsImb = 'k'

        self.colorGLE = ['#1f77b4','#ff7f0e','#2ca02c','#d62728','9467bd','8c564b','e377c2','7f7f7f','bcbd22',\
        '17becf','lightblue','slateblue','khaki','darkorange','firebrick','deepskyblue','gray50']

        # "#1f77b4" #blue
        # "#ff7f0e" #orange
        # "#2ca02c" #green
        # "#d62728" #red
        # "#9467bd" #violet
        # "#8c564b" #brown
        # "#e377c2" #pink
        # "#7f7f7f" #grey
        # "#bcbd22" #yellow
        # "#17becf" #cyan

        #        self.myColorsIn  = ['y','0.75','r','#FF9933','#CCFF33','#CCFFFF','g']
#        self.myColorsOut = ['b','m','#FF9933','g','c','#CCFF33','#CCFFFF''r']

    def setPath(self,_path):
        
        self.path = _path
        self.gle = gle.PlotGle(_path)
   
#    var = [1,....,12]
    def plotMonthly(self,var,myLabel,nameFile,yearlyFactor,useYearlyFactorAsValue=False,startMonth=1,myTitle=None,plotEmf=False,printData=False):
               
        move = 0
        N = 13
        width = 0.35        # the width of the bars
        ind = num.arange(N)  # the x locations for the groups

        fig = plt.figure(1,figsize=(12,8))
        
        plot = fig.add_subplot(111)
       
        #More processing is necessary if we want to have the yearly value at the 13 position as in Task44A38 
                
        if(startMonth != 1):
            if(len(var)==13):
                yearly = var[12]
                
            var = utils.reorganizeMonthlyFile(var,startMonth)
            
            if(len(var)==13):
                var[12]=yearly
        
        if(len(var)==12):          
            var13 = utils.addYearlyValue(var,yearlyFactor=yearlyFactor)
        elif(len(var)==13):
            var13 = var
        
        if(useYearlyFactorAsValue): var13[12]=yearlyFactor
        
        plot.bar(ind-move*width, var13, width, color='b')   

        plot.set_ylabel(myLabel,size=self.sizeAxis)
        
        box = plot.get_position()        
        plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        if(myTitle != None):
            plot.set_title(myTitle,size=20)
            
        plot.set_xticks(ind)
        
        if(yearlyFactor==1 or useYearlyFactorAsValue==True):
            yearTag="Year"
        else:
            yearTag = "Year/%d"%yearlyFactor
            
        monthSequence = utils.getMonthNameSequence(startMonth)
        monthSequence.append(yearTag)
        
        plot.set_xticklabels(monthSequence,fontsize=10,rotation='45')                       
                
        namePdf = '%s.pdf'%nameFile
        nameWithPath = '%s\%s' % (self.path,namePdf)

        print "plotMonthly name:%s"%nameWithPath
        
        plt.xlim([-0.5,12.5])
        
        plt.savefig(nameWithPath)
        
        if(plotEmf):
            
            nameEmf = '%s.jpg'%nameFile
            nameEmfWithPath = '%s\%s' % (self.path,nameEmf)
        
            plt.savefig(nameEmfWithPath)
            
        plt.close()
        
        if(printData==True):
            
            lines = ""
            line = "!nMonth %s\n"%(myLabel);lines=lines+line            
            
            for i in range(N):                
                line="%d\t%f\n"%(i+1,var13[i]);lines=lines+line
                                            
            nameWithPath = '%s\%s.dat' % (self.path,nameFile)
            outfile=open(nameWithPath,'w')    
            outfile.writelines(lines)
            outfile.close() 

            legends=[]
            legends.append(myLabel)
            
#            self.gle.getBarPlot(nameFile,nameWithPath,myLabel,xnames=monthSequence)
#            self.gle.getBarBalancePlot(nameFile,nameWithPath,myLabel,1,0,xnames=monthSequence)

        return namePdf

#If the yearly value needs to be set from outside, use avector with 13 positions as input and the yearly value will be unchanged.
        
    def plotMonthly2Bar(self,var1,var2,legends,myLabel,nameFile,yearlyFactor,startMonth=1,myTitle=None,plotEmf=False):
               
        move = 0.5
        N = 13
        width = 0.35        # the width of the bars
        ind = num.arange(N)  # the x locations for the groups

        fig = plt.figure(1,figsize=(12,8))
        
        plot = fig.add_subplot(111)
       
        #More processing is necessary if we want to have the yearly value at the 13 position as in Task44A38 
        if(startMonth != 1):
            if(len(var1)==13):
                yearly = var1[12]
                
            var1 = utils.reorganizeMonthlyFile(var1,startMonth)
            
            if(len(var1)==13):
                var1[12]=yearly

            if(len(var2)==13):
                yearly = var2[12]
                
            var2 = utils.reorganizeMonthlyFile(var2,startMonth)
            
            if(len(var2)==13):
                var2[12]=yearly                
                
        if(len(var1)==12):
            var13_1 = utils.addYearlyValue(var1,yearlyFactor=yearlyFactor)
        else:
            var13_1 = var1
            
        if(len(var2)==12):
            var13_2 = utils.addYearlyValue(var2,yearlyFactor=yearlyFactor)
        else:
            var13_2 = var2
            
        bar1 = plot.bar(ind-move*width, var13_1, width, color='b')   
        bar2 = plot.bar(ind+move*width, var13_2, width, color='y')           

        plot.set_ylabel(myLabel,size=self.sizeAxis)
        
        box = plot.get_position()        
        plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
        plot.legend([bar1,bar2],legends, bbox_to_anchor=(1.05,1),loc=2, borderaxespad=0.,fontsize=self.sizeLegend)

        if(myTitle != None):
            plot.set_title(myTitle,size=20)
            
        plot.set_xticks(ind)
        
        if(yearlyFactor==1):
            yearTag="Year"
        else:
            yearTag = "Year/%d"%yearlyFactor
        
        monthSequence = utils.getMonthNameSequence(startMonth)
        monthSequence.append(yearTag)


        plot.set_xticklabels(monthSequence,fontsize=10,rotation='45')                       
                
        namePdf = '%s.pdf'%nameFile
        nameWithPath = '%s\%s' % (self.path,namePdf)

        print "plotMonthly name:%s"%nameWithPath
        
        plt.xlim([-0.5,12.5])
        
        plt.savefig(nameWithPath)
        
        if(plotEmf):
            
            nameEmf = '%s.jpg'%nameFile
            nameEmfWithPath = '%s\%s' % (self.path,nameEmf)
        
            plt.savefig(nameEmfWithPath)
            
        plt.close()
        
        return namePdf

#inVar(nVar,nMonth)
    def plotMonthlyBalance(self,inVar,outVar,legends,myLabel,nameFile,unit,startMonth=1,colors=False,printImb=True,yearlyFactor=1,useYear=False,plotEmf=False,printData=False):
                       
        move=0
      
        if(startMonth != 1):
            for i in range(len(inVar)):
                inVar[i] = utils.reorganizeMonthlyFile(inVar[i],startMonth)

            for i in range(len(outVar)):            
                outVar[i] = utils.reorganizeMonthlyFile(outVar[i],startMonth)
                

        if(useYear==True):

            nMonth = 13        
            inVar13 = []
            outVar13 = []
            
            for i in range(len(inVar)):
#                print "useYear i:%d (inVar below)"%i
#                print inVar[i]
                
                inVar13.append(utils.addYearlyValue(inVar[i],yearlyFactor=yearlyFactor))

#                print "useYear i:%d (inVar13 below)"%i
#                print inVar13[i]

                
            for i in range(len(outVar)):
                outVar13.append(utils.addYearlyValue(outVar[i],yearlyFactor=yearlyFactor))
        else:
            nMonth = 12
            inVar13  = inVar
            outVar13 = outVar
            
        width = 0.35        # the width of the bars
        ind = num.arange(nMonth)  # the x locations for the groups
        imbPlus = num.arange(nMonth)
        imbNeg = num.arange(nMonth)
        imb = num.arange(nMonth)
        
        fig = plt.figure(1,figsize=(12,8))        
        plot = fig.add_subplot(111)                   
           
        for m in range(nMonth):
            sumIn = 0.
            for i in range(len(inVar13)):
                sumIn = sumIn + inVar13[i][m]
#                if(m==3):
#                print "month:%d i:%d sumIn:%f inVar:%f"%(m,i,sumIn,inVar13[i][m])
                
            sumOut = 0.
            for i in range(len(outVar13)):
                sumOut = sumOut + outVar13[i][m]

#                print "month:%d i:%d sumOut:%f outVar:%f"%(m,i,sumOut,outVar13[i][m])
                
            imbNeg[m]   = max(sumIn-sumOut,0)
            imbPlus[m]  = max(sumOut-sumIn,0)
            imb[m]      = imbNeg[m]+imbPlus[m]
#            if(m==3):            
#                print "month:%d imbNeg:%f imbPos:%f imb:%f"%(m,imbNeg[m],imbPlus[m],imb[m]) 
            
        bar = []
        
        addVar=0
        for i in range(len(inVar13)):
#            print "i:%d colorsIn:%s"%(i,self.myColorsIn[i])
            bar.append(plot.bar(ind-move*width, inVar13[i], width, color=self.myColorsIn[i],bottom=addVar))        
            addVar = addVar+inVar13[i]
#            if(i==0):               
#                bar.append(plot.bar(ind-0.5*width, inVar13[i], width, color=self.myColorsIn[i]))
#                addVar = inVar13[i]
#            else:                    
#                bar.append(plot.bar(ind-0.5*width, inVar13[i], width, color=self.myColorsIn[i],bottom=addVar))        
#                addVar = addVar+inVar13[i]
                
        if(printImb==True):
            plot.bar(ind-move*width, imbPlus, width, color=self.myColorsImb,bottom=addVar)
        
        for i in range(len(outVar13)):
            if(i==0):               
                bar.append(plot.bar(ind-move*width, -outVar13[i], width, color=self.myColorsOut[i]))
                addVar = -outVar13[i]
            else:                    
                bar.append(plot.bar(ind-move*width, -outVar13[i], width, color=self.myColorsOut[i],bottom=addVar))        
                addVar = addVar-outVar13[i]

        if(printImb==True):
            bar.append(plot.bar(ind-move*width, -imbNeg, width, color=self.myColorsImb,bottom=addVar))
                                             
        myLabel = myLabel+" [%s]"%unit
        plot.set_ylabel(myLabel,size=self.sizeAxis)
        
        box = plot.get_position()        
        plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
#        plot.set_title('Title',size=20)
        plot.set_xticks(ind)
        
        if(yearlyFactor==1):
            yearTag="Year"
        else:
            yearTag = "Year/%d"%yearlyFactor
            
        monthSequence = utils.getMonthNameSequence(startMonth)
        monthSequence.append(yearTag)

        plot.set_xticklabels(monthSequence,fontsize=self.sizeAxis,rotation='45')                       
        
        allbar =  []
        for b in bar:
            allbar.append(b[0])
            
        plot.legend(allbar,legends, bbox_to_anchor=(1.05,1),loc=2, borderaxespad=0.,fontsize=self.sizeLegend)

        
        namePdf = '%s.pdf'%nameFile
        nameWithPath = '%s\%s' % (self.path,namePdf)

        print "PlotMonthlyBalance name:%s"%nameWithPath
        
        if(useYear==True):
            plt.xlim([-0.5,13.5])        
        else:
            plt.xlim([-0.5,12.5])
        
        plt.savefig(nameWithPath)
        
        if(plotEmf):
            
            nameEmf = '%s.jpg'%nameFile
            nameEmfWithPath = '%s\%s' % (self.path,nameEmf)
        
            plt.savefig(nameEmfWithPath)
            
        plt.close()
        
        if(printData==True):
            
            lines = ""
            line = "!nMonth\t";lines=lines+line
            
            for label in legends:
                line="%s\t"%label;lines=lines+line
            line="\n";lines=lines+line
            
            #inVar(nVar,nMonth)

            for j in range(nMonth):
                line="%d\t"%(j+1);lines=lines+line
                
                sumVar = 0.
                for i in range(len(inVar13)):
                    
                    sumVar=sumVar+inVar13[i][j]
                    line="%.2f\t"%sumVar;lines=lines+line

                sumVar=0
                for i in range(len(outVar13)):
                    
                    sumVar=sumVar-outVar13[i][j]
                    line="%.2f\t"%sumVar;lines=lines+line
            
                line="\n";lines=lines+line
                
            nameWithPath = '%s\%s.dat' % (self.path,nameFile)
            outfile=open(nameWithPath,'w')    
            outfile.writelines(lines)
            outfile.close() 
            
#            if(len(outVar)==0):
#                self.gle.getBarPlot(nameFile,nameWithPath,legends,xnames=monthSequence)
#            else:
            self.gle.getBarBalancePlot(nameFile,nameWithPath,legends,len(inVar13),len(outVar13),xnames=monthSequence)
                
#        self.addLatexMonthlyData("",legends,unit,inVar,outVar,imb)
        
        return namePdf

    def plotDaily(self,var,myLabel,nameFile,plotJpg=False):
               
        N = 365
        width = 0.1        # the width of the bars
        ind = num.arange(N)  # the x locations for the groups

        fig = plt.figure(1,figsize=(50,8))
        
        plot = fig.add_subplot(111)
                                                                             
        plot.bar(ind-0.5*width, var, width, color='b')   

        plot.set_ylabel(myLabel,size=25)
        
        box = plot.get_position()        
        plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
#        plot.set_title('Title',size=20)
#        plot.set_xticks(ind)
#        plot.set_xticklabels(('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep','Oct', 'Nov', 'Dec','Year/10'),fontsize=20)                       
                
        namePdf = '%s.pdf'%nameFile
        nameWithPath = '%s\%s' % (self.path,namePdf)

        plt.xlim([-0.5,365])
        
        plt.savefig(nameWithPath)
        
        if(plotJpg):
            
            nameJpg = '%s.jpg'%myLabel 
            nameJpgWithPath = '%s\%s' % (self.path,nameJpg)
        
            plt.savefig(nameJpgWithPath)
            
        plt.close()        
        return namePdf
    
    #xvar 1d yVar 2D, so several lines
    def plotDynamic(self,xVar,yVar,legends,nameFile=None,xLabel="Days",plotJpg=False,printData=False,printEvery=1):
        
        
        try:
            size = len(xVar)
        except:            
            xVar = num.arange(len(yVar[0]))
        
        
        fig = plt.figure(1,figsize=(self.sizeFigX,self.sizeFigY))
        
        axes = fig.add_subplot(111)
            
        matplotlib.rcParams.update({'font.size':17})

        for i in range (len(yVar)):
            axes.plot(xVar,yVar[i],'-',color=self.myColorsIn[i])       
            
        axes.legend(legends,loc='upper left', borderaxespad=0.)
            
        axes.set_xlabel('%s'%xLabel,fontsize=20)        
#        axes.set_ylabel('%s'%myLabel,fontsize=20)
           
        if(self.useXLimits):
            plt.xlim([self.lowXLimit,self.highXLimit])

        if(self.useYLimits):
            plt.ylim([self.lowYLimit,self.highYLimit])

        if(nameFile==None):
            plt.show()
            namePdf = None
            
        else:
                  
            namePdf = '%s.pdf'%nameFile
            nameWithPath = '%s\%s' % (self.path,namePdf)
    
            
            plt.savefig(nameWithPath)
            
            if(plotJpg):
                
                nameJpg = '%s.jpg'%nameFile 
                nameJpgWithPath = '%s\%s' % (self.path,nameJpg)
            
                plt.savefig(nameJpgWithPath)
            
        plt.close()
        
        if(printData==True and nameFile!=None):
            lines = ""
            line = "!x\t";lines=lines+line
            
            for label in legends:
                line="%s\t"%label;lines=lines+line
            line="\n";lines=lines+line
            
            for j in range(len(yVar[0])):
                if(j%printEvery==0):
                    line="%f\t"%xVar[j];lines=lines+line                
                    for i in range(len(yVar)):
                        line="%f\t"%yVar[i][j];lines=lines+line
            
                    line="\n";lines=lines+line
                
            nameWithPath = '%s\%s.dat' % (self.path,nameFile)
            outfile=open(nameWithPath,'w')    
            outfile.writelines(lines)
            outfile.close()         
            
            markers=self.gle.useMarkers
            self.gle.useMarkers=False
            self.gle.getEasyPlot(nameFile,nameWithPath,legends)
            self.gle.useMarkers=markers
            
        return namePdf

    def plotDynamicBalance(self, xVar, yVarPos,yVarNeg, legends, nameFile=None, xLabel="Days", plotJpg=False, printData=False, printEvery=1):

        try:
            size = len(xVar)
        except:
            xVar = num.arange(len(yVar[0]))

        fig = plt.figure(1, figsize=(self.sizeFigX, self.sizeFigY))

        axes = fig.add_subplot(111)

        matplotlib.rcParams.update({'font.size': 17})

        for i in range(len(yVarPos)):
            axes.plot(xVar, yVarPos[i], '-', color=self.myColorsIn[i])

        k=len(yVarPos)
        for i in range(len(yVarNeg)):
            axes.plot(xVar, -yVarNeg[i], '-', color=self.myColorsIn[k])

        axes.legend(legends, loc='upper left', borderaxespad=0.)

        axes.set_xlabel('%s' % xLabel, fontsize=20)
        #        axes.set_ylabel('%s'%myLabel,fontsize=20)

        if (self.useXLimits):
            plt.xlim([self.lowXLimit, self.highXLimit])

        if (self.useYLimits):
            plt.ylim([self.lowYLimit, self.highYLimit])

        if (nameFile == None):
            plt.show()
            namePdf = None

        else:

            namePdf = '%s.pdf' % nameFile
            nameWithPath = '%s\%s' % (self.path, namePdf)

            plt.savefig(nameWithPath)

            if (plotJpg):
                nameJpg = '%s.jpg' % nameFile
                nameJpgWithPath = '%s\%s' % (self.path, nameJpg)

                plt.savefig(nameJpgWithPath)

        plt.close()

        if (printData == True and nameFile != None):
            lines = ""
            line = "!x\t";
            lines = lines + line

            for label in legends:
                line = "%s\t" % label;
                lines = lines + line
            line = "\n";
            lines = lines + line

            for j in range(len(yVar[0])):
                if (j % printEvery == 0):
                    line = "%f\t" % xVar[j];
                    lines = lines + line
                    for i in range(len(yVarPos)):
                        line = "%f\t" % yVarPos[i][j];
                        lines = lines + line

                    for i in range(len(yVarNeg)):
                        line = "%f\t" % yVarNeg[i][j];
                        lines = lines + line

                    line = "\n";
                    lines = lines + line

            nameWithPath = '%s\%s.dat' % (self.path, nameFile)
            outfile = open(nameWithPath, 'w')
            outfile.writelines(lines)
            outfile.close()

            markers = self.gle.useMarkers
            self.gle.useMarkers = False
            self.gle.getEasyPlot(nameFile, nameWithPath, legends)
            self.gle.useMarkers = markers

        return namePdf

    def plotDynamicOneVar(self,xVar,yVar,myLegend,nameFile,plotJpg=False):
        
        try:
            size = len(xVar)
        except:            
            xVar = num.arange(len(yVar))
            
        fig = plt.figure(1,figsize=(self.sizeFigX,self.sizeFigY))
        
        axes = fig.add_subplot(111)
            
        matplotlib.rcParams.update({'font.size':17})

        axes.plot(xVar,yVar,'-',color='b')       
            
        axes.legend(myLegend,loc='upper left', borderaxespad=0.)
            
        axes.set_xlabel('$Time$ $ [day]$',fontsize=20)        
        axes.set_ylabel('$%s$'%myLegend,fontsize=20)
                             
        
        if(nameFile==None):
            plt.show()
            namePdf = None
            
        else:
                  
            namePdf = '%s.pdf'%nameFile
            nameWithPath = '%s\%s' % (self.path,namePdf)
    
            print "plotDynamic: Save plot name:%s"%nameWithPath
            
            plt.savefig(nameWithPath)
            
            if(plotJpg):
                
                nameJpg = '%s.jpg'%nameFile 
                nameJpgWithPath = '%s\%s' % (self.path,nameJpg)
            
                plt.savefig(nameJpgWithPath)
            
        plt.close()
        
        return namePdf  
    
    def calcAndPrintQVersusT(self,fileName,tFlow,eFlow,legends,printEvery=1,normalized=False):
        
        nVar = len(legends)
        
        if(nVar>0):
            nTimeStep = len(tFlow[0])
        else:
            nTimeStep = len(tFlow)                  
                
        tSortVec   = []
        cumEnerVec = []
        
        for i in range(nVar):
            print "calcAndPrintQVersusT var:%s "%legends[i]
            tSort,cumE = utils.calcQvsT(tFlow[i],eFlow[i])
            tSortVec.append(tSort)
            cumEnerVec.append(cumE)
                    
        lines = ""
        line = "!Postprocessed file of ice storage.\n"; lines = lines + line      
        line = "!File processed with plotMatplotlib.py at %s\n" %(time.strftime('%c')); lines = lines + line
        
        line = "! "; lines = lines + line
        i = 2
        for j in range(nVar):
            line = "(%d) T-%s-sort (%d) cum-%s "%(i,legends[j],i+1,legends[j])
            lines = lines + line
            i=i+2
        line = "\n"; lines = lines + line
        
        for i in range(nTimeStep):                    
            if(i!= 0 and i!=nTimeStep-1 and i%printEvery==0):
                line = "%d "%(i); lines = lines+line
                for j in range(nVar):
                        line = "%f %f " % (tSortVec[j][i],cumEnerVec[j][i]); lines = lines+line
                line = "\n"; lines = lines+line
                
        myFileName = self.path + "//" + fileName + ".dat"
        
        print "File created :%s"%myFileName
        
        outfile=open(myFileName,'w')    
        outfile.writelines(lines)
        outfile.close()         
         
        self.gle.createGleQvsT(fileName,legends,normalized=normalized) #path not nedded becasue it is in the same folder

    #var[nvariables,nMonth] or var[nVariables], labels[nvariables]
    
    def plotPie(self,var,labels,myTitle,nameFile,printData=False,extension="pdf",sort=True,fontSize=10):
        
        fig = plt.figure(1,figsize=(8,8))
        
        fig.add_subplot(111)

#        figure(1, figsize=(6,6))        
#        ax = axes([0.1, 0.1, 0.8, 0.8])
        
        # The slices will be ordered and plotted counter-clockwise.
        
        varYear = []
        nVar = len(var)
#        print "nVar:%d"%nVar
        
        try:
            for i in range(nVar):
                #sum for all months
                varYear.append(sum(var[i]))                    
        except:
            for i in range(nVar):
                #yearly value already given
                varYear.append(var[i])
                            
        total = sum(varYear)
            
        fracs = []
        colors = []
        

        for i in range(nVar):
            fracs.append(varYear[i]/total)
            colors.append(self.myColorsIn[i])

        if (sort == True):
            #sort fracs by magnitude and joint those which are very small

            sortIndex = num.argsort(fracs)

    #        print fracs
    #        print sortIndex


            fracsSorted = []
            labelsSorted = []

            sumOthers = 0.
            for i in range(nVar):
                if(fracs[sortIndex[i]]>0.02):
                    fracsSorted.append(fracs[sortIndex[i]])
                    labelsSorted.append(labels[sortIndex[i]])
                else:
                    sumOthers = sumOthers+fracs[sortIndex[i]]

            if(sumOthers>0.):
                fracsSorted.append(sumOthers)
                labelsSorted.append("Others")
        else:
            fracsSorted = fracs
            labelsSorted = labels

#            explode=(0,1, 0.1, 0.1, 0.1, 0.1,0.1, 0.1)
        patches, texts, autotexts = plt.pie(fracsSorted, labels=labelsSorted,colors=colors,autopct='%1.0f%%', shadow=False, startangle=0)

        # patches, texts, autotexts = plt.pie(fracsSorted, colors=colors,autopct='%1.0f%%', shadow=False, startangle=0)

        # plt.legend(patches, labelsSorted, bbox_to_anchor=(2, 0.5), loc="upper right", fontsize=fontSize,
        #            bbox_transform=plt.gcf().transFigure)

        for i in range(len(texts)):
            texts[i].set_fontsize(fontSize)

        # The default startangle is 0, which would start
        # the Frogs slice on the x-axis.  With startangle=90,
        # everything is rotated counter-clockwise by 90 degrees,
        # so the plotting starts on the positive y-axis.

        matplotlib.rcParams.update({'font.size':fontSize})

        plt.title(myTitle, bbox={'facecolor':'0.9','pad':10},fontsize=fontSize)

        # pie = plt.pie(fracsSorted, startangle=0)
        #
        # plt.legend(pie[0], labels, bbox_to_anchor=(1, 0.5), loc="center right", fontsize=10,
        #            bbox_transform=plt.gcf().transFigure)
        # plt.subplots_adjust(left=0.0, bottom=0.1, right=0.45)

# This is working , just erase the labels section
#         plt.legend(bbox_to_anchor=(0.15,0.9),loc='upper right', borderaxespad=0.,fontsize=fontSize)

        namePdf = '%s.%s'%(nameFile,extension)
        nameWithPath = '%s\%s' % (self.path,namePdf)
        
        plt.savefig(nameWithPath)


        plt.close()

        if (printData == True):

            lines = ""

            for label in labelsSorted:
                line = "%s\t" % label;
                lines = lines + line
            line = "\n";
            lines = lines + line


            for i in range(len(fracsSorted)):
                line = "%f\t" % fracsSorted[i];
                lines = lines + line

            line = "\n";
            lines = lines + line

            nameWithPath = '%s\%s.dat' % (self.path, nameFile)
            outfile = open(nameWithPath, 'w')
            outfile.writelines(lines)
            outfile.close()


        return namePdf
    
    def plotYearlyEnergyBalance(self,inVar,outVar,legends,myLabel,nameFile,unit,useShares=False,colors=False,printImb=True,plotEmf=False,printData=False,useTwoColumns=False):

        try:
            if(len(inVar[0])>2):
                monthlyDataUsed=True
        except:
            monthlyDataUsed=False
            
        N = 2
        width = 0.65        # the width of the bars
     
        ind = num.arange(N)  # the x locations for the groups
        move = 0

        fig = plt.figure(1,figsize=(12,8))        
        plot = fig.add_subplot(111)        
        
        imbPlus = num.zeros(N)
        imbNeg  = num.zeros(N)
       
        inVarYear  = num.arange(len(inVar)*N,dtype=float).reshape(len(inVar),N)
        outVarYear = num.arange(len(outVar)*N,dtype=float).reshape(len(outVar),N)
        

        for i in range(len(inVar)):
            if(monthlyDataUsed):
                inVarYear[i][0] = sum(inVar[i])
                inVarYear[i][1] = 0.
            else:
                inVarYear[i][0] = inVar[i]
                inVarYear[i][1] = 0.

        positive = 0.
        for i in range(len(inVar)):
            positive = positive + inVarYear[i][0]

        if(useShares):
            for i in range(len(inVar)):
                inVarYear[i][0]=inVarYear[i][0]*100./positive

        for i in range(len(outVar)):
            if(monthlyDataUsed):
                outVarYear[i][1] = sum(outVar[i])
                outVarYear[i][0] = 0.
                
            else:
                outVarYear[i][1] = outVar[i]
                outVarYear[i][0] = 0.

        negative = 0.
        for i in range(len(outVar)):
            negative = negative + outVarYear[i][1]

        if (useShares):
            for i in range(len(outVar)):
                outVarYear[i][1]=outVarYear[i][1]*100./negative

        myImb = positive - negative

#        print inVarYear
#        print outVarYear
        
        if(myImb>0.):
            imbNeg[1] = positive - negative 
        else:
            imbPlus[0] = abs(positive - negative)
            
        addVar=0
        barIn = []
        for i in range(len(inVarYear)):
            barIn.append(plot.bar(ind-move*width, inVarYear[i], width, color=self.myColorsIn[i],bottom=addVar))        
            addVar = addVar+inVarYear[i]
#            print "plotYearEnergyBalance colorIn:%s"%self.myColorsIn[i]
                
        if(printImb==True and useShares==False):
            plot.bar(ind-move*width, imbPlus, width, color=self.myColorsImb,bottom=addVar)

        addVar=0
        barOut = []
        for i in range(len(outVarYear)):
#            print "plotYearEnergyBalance colorOut:%s"%self.myColorsOut[i]

            barOut.append(plot.bar(ind-move*width, outVarYear[i], width, color=self.myColorsOut[i],bottom=addVar))        
            addVar = addVar+outVarYear[i]
                
        if(printImb==True):
            plot.bar(ind-move*width, imbNeg, width, color=self.myColorsImb,bottom=addVar)

        myLabel = myLabel+" [%s]"%unit
        plot.set_ylabel(myLabel,size=self.sizeAxis)
        
        box = plot.get_position()        
        plot.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        
#        plot.set_title('Title',size=20)
        plot.set_xticks(ind)
        plot.set_xticklabels(('In', 'Out'),fontsize=self.sizeAxis,rotation='45')                       
        
        allbar =  []
        for i in range(len(barIn)):
#            print "plotYearlyEnergyBalance size BarIn:%d i:%d"%(len(barIn),i)
            if(printImb==True and i==len(barIn)-1):
#                print "plotYearlyEnergyBalance IGNORED i:%d"%(i)
                pass
            #Otherwise the legend should include the imbalabce between in and out variables
            else:
                allbar.append(barIn[i][0])
            
        for b in barOut:
            allbar.append(b[1])
            
        plot.legend(allbar,legends, bbox_to_anchor=(1.05,1),loc=2, borderaxespad=0.,fontsize=self.sizeLegend)
        
        namePdf = '%s.pdf'%nameFile
        nameWithPath = '%s\%s' % (self.path,namePdf)

        print "PlotMonthlyBalance name:%s"%nameWithPath
        
        plt.xlim([-0.5,1.5])        
        
        plt.savefig(nameWithPath)
        
        if(plotEmf):
            
            nameEmf = '%s.jpg'%nameFile
            nameEmfWithPath = '%s\%s' % (self.path,nameEmf)
        
            plt.savefig(nameEmfWithPath)
            
        plt.close()
        
        if(printData==True):
            
            lines = ""
            line = "!nMonth\t";lines=lines+line
            
            for label in legends:
                line="%s\t"%label;lines=lines+line
            line="\n";lines=lines+line
            
            #inVar(nVar,nMonth)

            if(useTwoColumns): #Uses two columns
                for j in range(2):
                    line="%d\t"%(j+1);lines=lines+line
                    
                    sumVar = 0.
                    for i in range(len(inVarYear)):
                        
                        sumVar=sumVar+inVarYear[i][j]
                        line="%f\t"%sumVar;lines=lines+line
    
                    sumVar=0
                    for i in range(len(outVarYear)):
                        
                        sumVar=sumVar-outVarYear[i][j]
                        line="%f\t"%sumVar;lines=lines+line
                
                    line="\n";lines=lines+line
            else: #Use one column
                j=0
                linesOne = ""
                linesEmpty = ""
                line="%d\t"%(j+1);linesOne=linesOne+line
                lineEmpty = "%d\t"%(j+2); linesEmpty = linesEmpty+lineEmpty
                sumVar = 0.
                for i in range(len(inVarYear)):
                    
                    sumVar=sumVar+inVarYear[i][j]
                    line="%f\t"%sumVar;linesOne=linesOne+line
                    lineEmpty = "0.0\t"; linesEmpty = linesEmpty+lineEmpty

                j=1
                sumVar=0
                for i in range(len(outVarYear)):
                    
                    sumVar=sumVar-outVarYear[i][j]
                    line="%f\t"%sumVar;linesOne=linesOne+line
                    lineEmpty = "0.0\t"; linesEmpty = linesEmpty+lineEmpty
            
                line="\n";linesOne=linesOne+line
                lineEmpty = "\n"; linesEmpty = linesEmpty+lineEmpty

                #I copy the same think twice 
                lines = lines + linesOne
                lines = lines + linesEmpty
#                 lines = lines + linesOne
                
            nameWithPath = '%s\%s.dat' % (self.path,nameFile)
            outfile=open(nameWithPath,'w')    
            outfile.writelines(lines)
            outfile.close() 
            
            self.gle.getBarPlot(nameFile,nameWithPath,legends,xmin=0.5,xmax=1.5,xnames=["In","Out"])
            
        
        return namePdf

        ##########################################HERE
