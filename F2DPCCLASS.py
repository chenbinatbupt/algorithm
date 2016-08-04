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
    
    def __init__(self,dataset):
        self.dataset=dataset
        self.size=len(dataset)
        self.dc=0.2
        self.localdensity=np.zeros(self.size)
        self.dismatrix = np.zeros((self.size,self.size))
        self.dishigher=np.zeros(self.size)
        self.dishigherneighbor=np.zeros(self.size)
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
        self.dc=t
    
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
            for j in range(self.size):
                if self.localdensity[j]>self.localdensity[i]:
                    if self.dismatrix[i,j]<mindis and i!=j:
                        mindis=self.dismatrix[i,j]
            self.dishigher[i]=mindis
            self.dishigherneighbor[i]=j
    
    def Get_Center_and_Outlier(self):
        enlist=[]
        relist=[]
        for index,value in enumerate(self.dishigher):
            enlist.append([index,value])
        enlist.sort(key=operator.itemgetter(1),reverse=True)
        i=1
        for element in  enlist:
            if element[1]>800:
                if localdensity[element[0]]<200:
                    relist.append([-1,element[0]])
                elif self.localdensity[element[0]]>200 and element[1]>800:
                    relist.append([i,element[0]])
                    i=i+1          
        self.relist=relist
        
    def clustering(self):
        catelist=np.zeros(self.size)
        instancelist=[]      
        for i in range(self.size):
            a=[catelist[i],self.localdensity[i],self.dishigher[i],i]
            instancelist.append(a)
        for k in range(len(self.relist)):
            cate=self.relist[k][0]
            index=self.relist[k][1]
            instancelist[index][0]=cate
        instancelist.sort(key=operator.itemgetter(1,2),reverse=True)
        for i in range(self.size):
                if(instancelist[i][0]==0):
                        instancelist[i][0]=instancelist[int(self.dishigherneighbor[i])][0]
        instancelist.sort(key=operator.itemgetter(3))
        self.instancelist=instancelist
        
    def quickcal(self,t):
        self.getdismatrix()
        self.getdc(t)
        self.getlocaldensity()
        self.getdisforhigherdensity()
        self.Get_Center_and_Outlier()
        self.clustering()