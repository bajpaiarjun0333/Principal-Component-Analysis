# -*- coding: utf-8 -*-
"""Q2Part4iid3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1g69rSvORUKsi2mRxeeHDNbSIxSlQ6Eyn
"""

#importing all the libraries to be used 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files
uploaded=files.upload()

#load the data file here 
df=pd.read_csv('Dataset.csv',header=None)
df=df.to_numpy()
n=df.shape[0]
m=df.shape[1]

dft=np.zeros((m,n))
for i in range(m):
  for j in range(n):
    dft[i][j]=df[j][i]

def computeKernel():
  k=np.zeros((n,n));
  for i in range(n):
    for j in range(n):
      val=0
      for o in range(m):
        val=val+df[i][o]*dft[o][j]
      val=val+1;
      val=val*val*val
      k[i][j]=val
  return k

def kernelCenter(k):
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
def randomCentroids(k):
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
  dist=np.sqrt(dist)
  return dist
#function correctly computes the norm

#we need to assign for the first time data point to each cluster
def assign(centroids,k):
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

def calculateMean(z,centroids,k):
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
def reassign(z,meu,k):
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

def computeErrors(meu,z):
  #we know the mean matrix and the point assignment, compute the error
  error=0
  for i in range(n):
    error=error+calculateDistance(df[i,:],meu[z[i]])
  return error

def plotOriginal():
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

#driver code
plotOriginal()
k=4
print("Running for the value of k as :: ",k)
err=[]
k_mat=computeKernel()
k_mat=computeEigen(k_mat,k)
z=normalizeEv(k_mat)
colors={0:'r',1:'g',2:'b',3:'coral',4:'cyan'}
for i in range(n):
  plt.scatter(df[i][0],df[i][1],color=colors[z[i]])
plt.xlabel("Dimension 1")
plt.ylabel("Dimension 2")
plt.title("After K Means Clustering Polynomial d=3 argmax")
plt.show()