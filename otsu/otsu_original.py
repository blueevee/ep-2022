from matplotlib import pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D

from PIL import Image

import numpy as np
from numpy import mean
from numpy import isnan
from numpy import asarray

import os
import shutil, glob, os.path

from random import shuffle

import skimage
from skimage import data, io, color, exposure, feature

from skimage.filters import threshold_otsu 
from skimage.feature import canny # edge extraction

from tqdm import tqdm

import math

import time

from random import randint

INPUT_PATH = 'D:/Users/diego/Google Drive/UNEB/ADocencia/EP/datasets/faces'
# 'D:/Users/diego/Google Drive/UNEB/ADocencia/EP/datasets/short_faces'
#'D:/Users/diego/Google Drive/NOTEBOOKS/IA WORKS/datasets/Concrete/Positive'
Files=os.listdir(INPUT_PATH)

nImg=len(Files)

print("number of images: ",nImg)

# preprocessamento das imagens do arquivo -> retorna uma imagem 1D em grayscale normalizada entre 0:255

def image_loader(path,toplt,topltgray):
    Image = io.imread(path) # load image in np.array
    if toplt:
        fig2, ax2 = plt.subplots(1,2, figsize=(12, 5.5))
        ax2[0].imshow(Image)
        ax2[1].hist(Image.ravel(), bins = 64, color = 'orange', alpha = 0.5)
        ax2[1].hist(Image[:, :, 0].ravel(), bins = 64, color = 'red', alpha = 0.5)
        ax2[1].hist(Image[:, :, 1].ravel(), bins = 64, color = 'Green', alpha = 0.5)
        ax2[1].hist(Image[:, :, 2].ravel(), bins = 64, color = 'Blue', alpha = 0.5)
        ax2[1].set_xlim(0, 255)
        ax2[1].set_xlabel('Intensity Value')
        ax2[1].set_ylabel('Count')
        ax2[1].legend(['Total', 'Red_Channel', 'Green_Channel', 'Blue_Channel'])
        plt.show()
    
    if Image.shape[2]>=3: # if RGB or similar
        gray=0
    else: # grayscale input
        gray=1
        
    x=Image.shape[0]
    y=Image.shape[1]
    
    image=[] # vetor 1D de pixels monocromáticos
    
    for i in range(x):
        for j in range(y):
            if gray==0:
                image.append(int(0.2989*Image[i][j][0]+0.5870*Image[i][j][1]+0.1140*Image[i][j][2])) # color to gray scale
            else: # gray inpt image
                image.append(int(Image[i][j]))

 # normalization of grayscale to 0:255 interval for each image (MinMaxScaler)
    image=np.array(image)
    Mx=np.max(image)
    mx=np.min(image)
    image=(255*(image-mx)/(Mx-mx)).astype(int)  
    
    if topltgray:
        gimage=image.reshape(x,y)
        fig2, ax2 = plt.subplots(1,2, figsize=(12, 5.5))
        plt.style.use('grayscale')
        ax2[0].imshow(gimage)
        ax2[1].hist(gimage.ravel(), bins = 64, color = 'orange',alpha = 0.5)
        ax2[1].set_xlim(0, 255)
        ax2[1].set_xlabel('Intensity Value')
        ax2[1].set_ylabel('Count')
        ax2[1].legend(['Total'])
        plt.show()
        
    return Image.shape[0], Image.shape[1], image, Image

# load and preprocess image data set + MAPEA O INTERVALO DE VARIAÇÃO DO TAMANHO n DAS IMAGENS NA PASTA 

X=[]
O=[]
ResX=[]
ResY=[]
n=[]

nImg=4

for file in tqdm(Files[:nImg]): # tqdm(Files[:nImg]): #
    
    path=os.path.join(INPUT_PATH, file)
    X.append([])
    O.append([])
    
    RX, RY, Img, OrigImg = image_loader(path,True,True) # returns a grayscale image of the same size. bool prm: plot RGB & plot grayscale
    
    n.append(Img.shape[0])
    
#    print("n = ",n[-1])
    
    ResX.append(RX)
    ResY.append(RY)
    X[-1].append(Img)
    O[-1].append(OrigImg)

# PLOTA HISTOGRAMA DE TAMANHOS
plt.hist(n,bins=100)
plt.show()
print("menor imagem ",np.min(n)," maior imagem ",np.max(n))

# Y contains the images to process


O=[]
#debb
#print(Y)

def histo(img,M): # input img 1D
    
    p=np.zeros((M),dtype=float)
    n=len(img)
    
    for i in range(n):
        p[img[i]]+=1
        
    return np.max(p), p/n

def BuildOTSUTables2(frq,L):  # L =256
    
    H=np.zeros((L,L),dtype=float)
    
    C=frq[0]
    for i in range(1,L):
        C+=(i+1)*frq[i]

    for i in range(L): # linha
        p = frq[i]
        s = (i+1)*frq[i]
        if p>0: # diagonal elements
            H[i,i]=p*(int(s/p)-C)**2
        for j in range(i+1,L): # off-diagonal elements by recorrencia
            p+=frq[j]
            s+=(j+1)*frq[j]
            if p>0:
                H[i,j]=p*(int(s/p)-C)**2
                
    return H

def FUNOBJ_PC(T,K,H,L): # função objetivo OTSU original
    
    t=[-1]+list(np.array(T)-1)+[L-1]
    
    Q=0
    for i in range(K):
        Q+=H[t[i]+1,t[i+1]]
           
    return Q
def segment(K,L,img):
         
    if K<2 or K>6:
        print("K fora do intervalo 2-4")
        return []
    else:  
        
        bg=time.time()
        Qmax=0
        fMax=[]

        # calcula histograma

        hist_max, p = histo(img,L)
        
        H=BuildOTSUTables2(p,L)
    
        f=[]
        for i in range(K-1):
            f.append(i)
 
        init_time=time.time()-bg   
        
        bg=time.time()
        itera=0
        a=L-K+2
        
        if K==2:
            for f[0] in range(0,a):
                itera+=1
                Q=FUNOBJ_PC(f,K,H,L)
#                 print('calculo com thresholds',f,Q)
                if Q>Qmax:
                    Qmax=Q
                    fMax=f.copy()
                    
        elif K==3:
            b=a+1 #
            for f[0] in range(0,a):
                e=f[0]+1
                for f[1] in range(e,b): 
                    itera+=1
                    Q=FUNOBJ_PC(f,K,H,L)
#                     print('calculo com thresholds',f,Q)
                    if Q>Qmax:
                        Qmax=Q
                        fMax=f.copy()

        elif K==4:
            b=a+1 # M-(K-1)+2
            d=b+1 # M-(K-2)+2
            for f[0] in range(0,a):
                e=f[0]+1
                for f[1] in range(e,b): 
                    g=f[1]+1
                    for f[2] in range(g,d):
                        itera+=1
                        Q=FUNOBJ_PC(f,K,H,L)
                        if Q>Qmax:
                            Qmax=Q
                            fMax=f.copy()

        elif K==5:
            b=a+1 # M-(K-1)+2
            d=b+1 # M-(K-2)+2
            h=d+1 # M-(K-3)+2
            for f[0] in range(0,a):
                e=f[0]+1
                for f[1] in range(e,b): 
                    g=f[1]+1
                    for f[2] in range(g,d):
                        l=f[2]+1
                        for f[3] in range(l,h):
                            itera+=1
                            Q=FUNOBJ_PC(f,K,H,L)
                            if Q>Qmax:
                                Qmax=Q
                                fMax=f.copy()

        elif K==6:
            b=a+1 # M-(K-1)+2
            d=b+1 # M-(K-2)+2
            h=d+1 # M-(K-3)+2
            q=h+1 # M-(K-4)+2
            for f[0] in range(0,a):
                e=f[0]+1
                for f[1] in range(e,b): 
                    g=f[1]+1
                    for f[2] in range(g,d):
                        l=f[2]+1
                        for f[3] in range(l,h):
                            s=f[3]+1
                            for f[4] in range(s,q):
                                itera+=1
                                Q=FUNOBJ_PC(f,K,H,L)
                                if Q>Qmax:
                                    Qmax=Q
                                    fMax=f.copy()

        iter_time=(time.time()-bg)   
                            
    return init_time, iter_time, itera, fMax
                    
test=1 # SELECIONA UMA IMAGEM DADA PARA FAZER O TESTE DOS CODIGOS FONTE 

my_color = []
my_color.append('#%06X' % 0)
my_color.append('#%06X' % 0xFFFFFF)
for i in range(20):
    my_color.append('#%06X' % randint(0, 0xFFFFFF))

# PARAMETERS

plt.style.use('classic')

L=256 # numero de escalas de cinza

nexp=1 # repetições do experimento

Kmax=4
    
# loop por imagens - test

for j in range(nImg):
    
    print("n   K   inTime (Std) itTime (Std) best_thresholds")
    x=ResX[j]
    y=ResY[j]
    N=x*y

    for K in range(2,Kmax+1):

        InTime=[]
        ItTime=[]

        for i in range(nexp):

            inittime,itertime, iterations, thresholds = segment(K,L,Y[j])

            InTime.append(inittime)
            ItTime.append(itertime)

        print(N,K,np.mean(InTime),'(',np.std(InTime),')',np.mean(ItTime),'(',np.std(ItTime),')',thresholds)

        # fill image

        f=[-1]+list(np.array(thresholds)-1)+[L-1]

        # classificando pixels

        Mask=[]
        for i in range(N):
            for k in range(K):
                if Y[j][i]>f[k] and Y[j][i]<=f[k+1]:
                    Mask.append(colors.hex2color(my_color[k]))
                    break

         #PLOT 

        fig, ax = plt.subplots(1,2, figsize=(12, 5.5))
        ax[0].imshow(np.array(Mask).reshape(x,y,-1))
        ax[1].hist(oI[j].ravel(), bins = 64, color = 'orange',alpha = 0.5)
        ax[1].set_xlim(0, L-1)
        hist_max, p=histo(Y[j],L)
        ax[1].vlines(f[1:K],0,hist_max,linewidths=3,colors='black')
        ax[1].set_xlabel('Intensity Value')
        ax[1].set_ylabel('Count')
        ax[1].set_title('solid black lines are the thresholds')
        plt.show()
   
    