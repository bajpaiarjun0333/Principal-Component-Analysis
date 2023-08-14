# -*- coding: utf-8 -*-
"""centeredQ1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18fOBknJXQy5u1_X3hk6reUk2M79TzGSW
"""

#importing the librares
import numpy as np
import pandas as pd
import io
from google.colab import files
uploaded=files.upload()

import matplotlib.pyplot as plt
df=pd.read_csv('Dataset.csv',header=None);
df=df.to_numpy();

#finding number of rows
sh=df.shape
n=sh[0]
m=sh[1]
def dataCenter():
  x_mean=0
  y_mean=0
  #calculate the mean of both the column for data centering
  for i in range (n):
    x_mean=x_mean+df[i][0]
    y_mean=y_mean+df[i][1]
  #we have accumulated the values now find the mean 
  x_mean=x_mean/n
  y_mean=y_mean/n
  print("Mean of dimension 1: ",x_mean)
  print("Mean of dimension 2: ",y_mean)
  #calculated the mean of both the columns now center the data
  for i in range(n):
    df[i][0]=df[i][0]-x_mean
    df[i][1]=df[i][1]-y_mean
  print("Data has been mean centered properly")

def computeCov():
  #compute the 2*2 matrix i.e the covariance matrix (XTX)/n
  m=df.shape[1]
  #calculate the product matrix
  data=np.zeros((m,m))
  #calculating the transpose matrix
  dft=np.zeros((2,1000))
  for i in range (m):
    for j in range(n):
      dft[i][j]=df[j][i]
  #calculate the product i.e data for the model
  for i in range(m):
    for j in range(m):
      for k in range(n):
        data[i][j]=data[i][j]+dft[i][k]*df[k][j]
  for i in range(m):
    for j in range(m):
      data[i][j]=data[i][j]/n
  return data

def plotOriginal():
  plt.scatter(df[:,0],df[:,1])
  plt.xlabel("Dimension 1")
  plt.ylabel("Dimension 2")
  plt.title("Original data")
  plt.axline((0,0),(-0.323516, -0.9462227),color = "red",label = 'w1')
  plt.axline((0,0),(-0.9462227, 0.323516),color = "black",label = 'w2')
  plt.legend(bbox_to_anchor = (1.05, 0.6))
  plt.show()

#calculate the eigen vector and eigen values
def computeEigen(data):
  w,v=np.linalg.eig(data)
  idx=w.argsort()[::-1]
  w=w[idx]
  v=v[:,idx]
  #we cant eliminate any direction so project along both directions
  projected=np.zeros((1000,2))
  for i in range(n):
    for j in range(m):
      for k in range(m):
        projected[i][j]=projected[i][j]+df[i][k]*v[k][j];
  print("Projections computed successfully")
  return projected

#project on dimensions
def project(projected):
  plt.scatter(projected[:,0],projected[:,1])
  plt.xlabel("Principal component 1(Largest Eigen Value)")
  plt.ylabel("Principal component 2(Second Largest Eigen Value)")
  plt.title("Plot for centered data")
  plt.show()

def calVar(projected):
  #calculate the variance over principal components
  var_x=0
  var_y=0
  for i in range(n):
    var_x=var_x+projected[i][0]*projected[i][0]
    var_y=var_y+projected[i][1]*projected[i][1]
  var_x=var_x/1000
  var_y=var_y/1000
  total=var_x+var_y
  var_x=var_x/total
  var_x=var_x*100
  var_y=var_y/total
  var_y=var_y*100
  print("Variance along the first principal component",var_x,"%")
  print("Variance along the second principal component",var_y,"%")

dataCenter()
data=computeCov()
projected=computeEigen(data)
plotOriginal()
project(projected)
calVar(projected)

