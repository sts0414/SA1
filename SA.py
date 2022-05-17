# -*- coding: utf-8 -*-
"""
Created on Sun May 12 22:12:15 2019

@author: ASUSTek
""" 
#conda create --name TEST python=3.6 basemap
#conda activate TEST
#python -c "from mpl_toolkits.basemap import Basemap"
import math
import random
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap


#讀取資料 
farelist = pd.read_csv('C:\\Users\\ASUSTek\\Desktop\\data.csv')
farelist = np.asmatrix(farelist)
farelist = np.delete(farelist, 0, 1)
citylist = []
with open('C:\\Users\\ASUSTek\\Desktop\\data.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    for i,rows in enumerate(reader):
        if i == 0:
            citylist = rows
citylist = np.delete(citylist, 0, 0)

        
#生成函式
#城市互換
def swap(a):
   randomlist = random.sample(list(citylist[:]), 2)
   temptour = list(a)
   temp = temptour[0:len(citylist[:])]
   index = temp.index(randomlist[0])
   temp[index] = randomlist[1]
   temptour[temptour.index(randomlist[1])] = randomlist[0]
   temptour[index] = temp[index]
   temptour = temptour[0:len(citylist[:])]
   temptour.append(temptour[0])
   return temptour;
#計算票價
def cost(x):
    eachcost = []
    for i in range(20):
      cost = farelist[list(citylist).index(x[i]),list(citylist).index(x[i+1])]
      eachcost.append(cost)
    return sum(eachcost)
#演算法
def coinflip(s,s2,T):
    p = math.exp(-(cost(s2)-cost(s))/T)
    u = np.random.uniform(size=1)
    if u < p:
      return True
    else:
      return False
#畫圖
def plot_conus(s,title):
    fig, ax = plt.subplots(figsize=(12, 9))
    m = Basemap(
        llcrnrlon=119.0, 
        llcrnrlat=21.8,
        urcrnrlon=122.05, 
        urcrnrlat=25.4,
        projection='merc',
        resolution='i')
    m.drawcoastlines()
    m.drawcountries()
    m.drawstates()
    plt.title(title)
    long = [121.51, 121.31, 120.97, 120.68, 120.44,120.21,120.65
            ,120.53,120.30,120.48,121.37,121.60,121.75,121.94
            ,120.54,120.78,121.00,120.82,121.12,121.21]
    lat = [ 25.04,  24.98,  24.80,  24.13,  23.47, 22.99, 22.26
             , 24.08, 22.63, 22.66, 23.49, 23.99, 24.75, 25.01
             , 23.71, 23.82, 22.61, 24.56, 22.79, 23.12]
    x, y = m(long, lat) 
    ax.scatter(x, y, marker = 'o')
    linelong = []
    linelat = []
    for j in range(len(s)):
      linelong.append(long[list(citylist).index(s[j])])
      linelat.append(lat[list(citylist).index(s[j])])
    linex, liney = m(linelong, linelat) 
    ax.plot(linex, liney, color='r')
    for i, (x, y) in enumerate(zip(x, y)):
      if i == 1 or i == 14:
        ax.annotate(citylist[i], (x,y), xytext=(-20, 10), textcoords='offset points')
      elif i == 7 or i == 8:
        ax.annotate(citylist[i], (x,y), xytext=(-20, -15), textcoords='offset points')
      else:
        ax.annotate(citylist[i], (x,y), xytext=(5, 10), textcoords='offset points')
    return m

#執行函式
def exe(T,iteration): #T=1500,iteration=1000
    s = random.sample(list(citylist[:]),20) #initial tour
    s.append(s[0]) 
    mincost = cost(s)
    minTour = list(s)
    title = 'Initial'
    plot_conus(minTour,title)
    file_name = 'C:\\Users\\ASUSTek\\Desktop\\SA\\picture\\initial.png'
    plt.savefig(file_name)
    for o in range(60):
        for k in range(iteration):
            s2 = list(swap(s))
            if cost(s2) < cost(s):
                s = list(s2)
                if cost(s2) < mincost:
                    mincost = cost(s2)
                    minTour = list(s2)
            elif coinflip(s,s2,T):
                s = list(s2)   
        print(mincost)
        title = 'Iteration' + str(o+1)
        plot_conus(minTour,title)
        file_name = 'C:\\Users\\ASUSTek\\Desktop\\SA\\picture\\iteration' + str(o) + '.png'
        plt.savefig(file_name)
        T = T*0.9
        #print(T)
#執行
exe(1500,1000)

 





