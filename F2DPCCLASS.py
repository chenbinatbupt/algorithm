# -*- coding: utf-8 -*-
"""
Created on Thu Aug  4 22:02:35 2016

@author: Administrator
"""
import numpy as np
import math
import matplotlib.pyplot as plt
import operator
import csv
import pickle


class F2DPC(object):
    
    def __init__(self,dataset,label):
        self.dataset=dataset
        self.size=len(dataset)
        self.dc=0.2
        self.localdensity=np.zeros(self.size)
        self.dismatrix = np.zeros((self.size,self.size))
        self.dishigher=np.zeros(self.size)
        self.dishigherneighbor=np.zeros(self.size)
        self.label=label
        
    def check_results(self):
        clusterdic={}
        label=self.label
        for i in range(self.size):
            clulabel=str(int(self.instancelist[i][0]))
            if clulabel in clusterdic:
                if label[i] in clusterdic[clulabel]:
                    clusterdic[clulabel][label[i]]=clusterdic[clulabel][label[i]]+1
                else:
                    clusterdic[clulabel][label[i]]=1
            else:
                clusterdic[clulabel]={}
                if label[i] in clusterdic[clulabel]:
                    clusterdic[clulabel][label[i]]=clusterdic[clulabel][label[i]]+1
                else:
                    clusterdic[clulabel][label[i]]=1
        self.clusterdic=clusterdic
        
    def ShowAllMember(self):
        for i,j in vars(self).items():
            print (i,'=',j)
            
    def getdistance(self,X1,X2):
        out=X1-X2
        out=pow(out,2)
        return math.sqrt(sum(out))
        
    def getdismatrix(self):
        for i in range(self.size):
            for j in range(i,self.size):
                self.dismatrix[i,j]=self.getdistance(self.dataset[i],self.dataset[j])
        self.dismatrix=self.dismatrix+self.dismatrix.T        
        
        
    def getdc(self,t):
        lenth=self.size*self.size
        disarray=np.sort(np.array(self.dismatrix.reshape(1,-1))[0])
        count=round(t*lenth)
        dc=disarray[count]
        self.dc=dc
    
    def getlocaldensity(self):
        for i in range(self.size):
            num_sum=0
            disvector=self.dismatrix[i]
            for j in range(self.size):
                if i!=j:
                    num_sum+=math.exp(-(disvector[j]/self.dc)*(disvector[j]/self.dc));  
            self.localdensity[i]=num_sum

    def getdisforhigherdensity(self):
        for i in range(self.size):
            mindis=max(self.dismatrix[i])
            minindex=i
            for j in range(self.size):
                if self.localdensity[j]>self.localdensity[i]:
                    if self.dismatrix[i,j]<mindis and i!=j:
                        mindis=self.dismatrix[i,j]
                        minindex=j
            self.dishigher[i]=mindis
            self.dishigherneighbor[i]=minindex
            
    
    def Get_Center_and_Outlier(self,lowdistance=200,higherdistance=800,density=200):
        enlist=[]
        relist=[]
        for index,value in enumerate(self.dishigher):
            enlist.append([index,value])
        enlist.sort(key=operator.itemgetter(1),reverse=True)
        i=1
        for element in  enlist:
            if element[1]>lowdistance:
                if self.localdensity[element[0]]<density:
                    relist.append([-1,element[0]])
                elif self.localdensity[element[0]]>density and element[1]>higherdistance:
                    relist.append([i,element[0]])
                    i=i+1          
        self.relist=relist
        
    def clustering(self):
        catelist=np.zeros(self.size)
        instancelist=[]
        forlabellist=[]
        for i in range(self.size):
            a=[catelist[i],self.localdensity[i],self.dishigher[i],i]
            instancelist.append(a)
        for k in range(len(self.relist)):
            cate=self.relist[k][0]
            index=self.relist[k][1]
            instancelist[index][0]=cate
        forlabellist=instancelist[:]
        instancelist.sort(key=operator.itemgetter(1,2),reverse=True)
        for i in range(self.size):
                if(int(instancelist[i][0])==0):
                        instancelist[i][0]=forlabellist[int(self.dishigherneighbor[instancelist[i][3]])][0]
        instancelist.sort(key=operator.itemgetter(3))
        self.instancelist=instancelist
        
    def plotscatter(self):
        plt.scatter(self.localdensity,self.dishigher)
        
    def quickcal(self,t):
        self.getdismatrix()
        self.getdc(t)
        self.getlocaldensity()
        self.getdisforhigherdensity()
        self.plotscatter()

