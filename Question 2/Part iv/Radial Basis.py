# -*- coding: utf-8 -*-
"""Q2Part4iiiRadial.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Mml2CJ9Zg5Z4Rx0l5pfPWdfTC5YOAaoM
"""

#importing all the libraries to be used 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
uploaded=files.upload()

#load the data file here 
def loadData():
  df=pd.read_csv('Dataset.csv',header=None)
  df=df.to_numpy()
  n=df.shape[0]
  m=df.shape[1]
  return (df,n,m)

def trans(df,n,m):
  dft=np.zeros((m,n))
  for i in range(m):
    for j in range(n):
      dft[i][j]=df[j][i]
  return dft

#calculating the kernel matrix
def kernelCompute(factor,df,dft,n,m):
  k=np.zeros((n,n));
  for i in range(n):
    for j in range(n):
      diff=df[i,:]-df[j,:]
      val=np.matmul(diff,np.transpose(diff))
      val=val*-1
      val=val/(2*factor*factor)
      val=np.exp(val)
      k[i][j]=val
  return k

def kernelCenter(k,n,m):
  I=np.zeros((n,n))
  for i in range(n):
    for j in range(n):
      if i==j:
        I[i][j]=1
  #identity matrix is ready 
  one=np.zeros((n,n))
  for i in range(n):
    for j in range(n):
      one[i][j]=1/n;
  diff=I-one
  #centering the kernel matrix
  res=np.matmul(diff,k)
  res2=np.matmul(res,diff)
  k=res2
  return k

def computeEigen(k_matrix, k):
  w,v=np.linalg.eig(k_matrix)
  idx=w.argsort()[::-1]
  w=w[idx]
  v=v[:,idx]
  w=w[0:k]
  v=v[:,0:k]
  return v
#now v will become the new data matrix

#pick any k random data point and call them as cluster
import random
def randomCentroids(k,df,n,m):
  centroids=[]
  for i in range(k):
    index=random.randint(0,n)
    centroids.append(df[index,:])
  return centroids

def calculateDistance(x,y):
  #these x and y are supposed to be m dimensional vectors
  dist=0;
  for i in range(len(x)):
    diff=x[i]-y[i]
    diff=diff*diff
    dist=dist+diff
  return dist
#function correctly computes the norm

#we need to assign for the first time data point to each cluster
def assign(df,centroids,k,n,m):
  #points are there in the data frame, z is the assignment list
  z=[]
  for i in range(n):
    x=df[i,:]
    temp_dist=[]
    for j in range(k):
      y=centroids[j]
      dist=calculateDistance(x,y)
      temp_dist.append(dist)
    index=np.argmin(temp_dist)
    z.append(index)
  return z
#assign is correctly working

def calculateMean(z,centroids,k,df,n,m):
  #we have to calulate mean for all 4 clusters i.e meu
  meu=[]
  for i in range(k):
    sum=[]
    num=0;
    for j in range(n):
      if z[j]==i:
        num=num+1
        sum.append(df[j,:])
    meu.append(np.mean(sum,axis=0))
  return meu
#this will return all the meu

#i have all the basic functionality now
def reassign(z,meu,k,df,n,m):
  #meu contains all the means of the clusters
  #check all points if they want to switch their means
  flag=False
  znew=[]
  for i in range(n):
    znew.append(z[i])
  for i in range(n):
    #for every point
    temp=[]
    for j in range(k):
      nextDist=calculateDistance(df[i,:],meu[j])
      temp.append(nextDist)
    idx=np.argmin(temp)
    if idx!=z[i]:
      znew[i]=idx
      flag=True
  return (flag,znew)

def computeErrors(meu,z,df,n,m):
  #we know the mean matrix and the point assignment, compute the error
  error=0
  for i in range(n):
    error=error+calculateDistance(df[i,:],meu[z[i]])
  return error

def plotOriginal(df):
  print("The Original Dataset")
  plt.scatter(df[:,0],df[:,1])
  plt.xlabel("Dimension 1")
  plt.ylabel("Dimension 2")
  plt.title("Original Data without Clustering")
  plt.show()

def normalizeEv(v):
  z=[]
  n=v.shape[0]
  m=v.shape[1]
  for i in range(n):
    temp=[]
    for j in range(m):
      temp.append(v[i][j])
    idx=np.argmax(temp)
    z.append(idx)
  return z

def radial(factor):
  k=4
  print("Running for the value of k as :: ",k)
  print("Running for the value of factor as :: ",factor)
  df,n,m=loadData()
  plotOriginal(df)
  dft=trans(df,n,m)
  k_mat=kernelCompute(factor,df,dft,n,m)
  k_mat=kernelCenter(k_mat,n,m)
  k_mat=computeEigen(k_mat,k)
  z=normalizeEv(k_mat)
  colors={0:'r',1:'g',2:'b',3:'coral',4:'cyan'}
  for i in range(n):
    plt.scatter(df[i][0],df[i][1],color=colors[z[i]])
  plt.xlabel("Dimension 1")
  plt.ylabel("Dimension 2")
  plt.title("After K Means Radial Basis")
  plt.show()
  #plot the errors over the iterations 
  # for i in range(count+2):
  #   plt.scatter(i, err[i])
  # plt.xlabel("Iteration Number")
  # plt.ylabel("Error")
  # plt.title("Error Plot")
  # plt.show()

factor=0.1
while factor<=1:
  radial(factor)
  factor=factor+0.1