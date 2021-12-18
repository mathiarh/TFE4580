#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 13 09:47:43 2021

@author: mathiasrammhaugland
"""

#based on paper: https://www.hindawi.com/journals/cmmm/2015/607407/

import numpy as np
from PIL import Image
import cv2

HEIGHT = 512
WIDTH = 512

def loadIm(path):
    im = Image.open(path).convert('RGB') #path contains filename.type
    #returns a numpy array of image, RGB
    im = im.resize((WIDTH,HEIGHT))
    return np.asarray(im)

def displayArrayIm(im):
    img = Image.fromarray(im, "RGB")
    img.show()
    return None


def rgbToYCbCr(im):
    r = im[:,:,0]
    g = im[:,:,1]
    b = im[:,:,2]
    
    y = 0.257*r + 0.504*g + 0.098*b + 16
    cb = -0.148*r -0.291*g + 0.439*b + 128
    cr = 0.439*r -0.368*g -0.071*b + 128

    return y,cb,cr
    

def normalize(x, x_min, x_max):
    #input image is a monochromatic matrix
    x_norm = np.zeros(x.shape)
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(x)[1]):
            x_norm[i,j] = (x[i,j]-x_min)/x_max
    return x_norm
    
def calculateAverageChrominance(locate,chrom):
    count = 0
    summ = 0
    for m in range(np.shape(locate)[0]):
        for n in range(np.shape(locate)[1]):
            if locate[m,n] == 0:
                summ += chrom[m,n]
                count += 1
    return summ/count


def newChrominance(y,y_t,cb_t,cr_t):
    #gives new chrominance values to be applied on y
    
    #new chrominance matrices:
    cb_n = np.zeros(y.shape)
    cr_n = np.zeros(y.shape)
    
    for i in range(np.shape(y)[0]):
        print(i)
        for j in range(np.shape(y)[1]):

            #subtract Yi,j from Yt and put in new matrix
            locate = y_t - y[i,j]
            #now we got 0, 1 or more 0s in the locate matrix
            
            #count zeros in the locate matrix
            num_of_zeros = locate[np.where(locate == 0)].size
            
            if num_of_zeros == 0:
                #use chrominance values of cb_t and cr_t at i,j
                cb_n[i,j] = cb_t[i,j]
                cr_n[i,j] = cr_t[i,j]
            else:
                #calculate average chrominance values in cb_t and cr_t
                #at positions where locate == 0
                #this also works when num_of_zeros == 1
                cb_n[i,j] = calculateAverageChrominance(locate,cb_t)
                cr_n[i,j] = calculateAverageChrominance(locate,cr_t)
    
    return cb_n, cr_n

def yCbCrToRGB(y,cb,cr):
    r = 1.164*(y-16) + 1.596*(cr-128)
    g = 1.164*(y-16) -0.392*(cb-128) -0.813*(cr-128)
    b = 1.164*(y-16) +2.017*(cb-128)
    
    """
    #to fit r,g & b into the dynamic range
    np.putmask(r,r >255, 255)
    np.putmask(r,r <0, 0)

    np.putmask(g,g >255, 255)
    np.putmask(g,g <0, 0)

    np.putmask(b,b >255, 255)
    np.putmask(b,b <0, 0)
    """
    
    
    maxval = abs(max(np.amax(r),np.amax(g),np.amax(b)))
    minval = abs(min(np.amin(r), np.amin(g), np.amin(b)))
    
    r = (r+minval)*255/maxval
    g = (g+minval)*255/maxval
    b = (b+minval)*255/maxval
    
    return r, g, b
            

def unNormalize(x_new, x_t):
    x_min = np.amin(x_t)
    x_max = np.amax(x_t)
    return (x_new*x_max)+x_min

def getCutoff(y):
    return np.average(y)

def getGain(y,k):
    A = 100
    Sm = 6
    Sn = 5
    g = A*np.log(Sm/Sn)*k
    return g

def sigmoid(y, k=0, g=1):
    y_sig = 1/(1+np.exp(g*(k-y)))
    return y_sig

def histogram(y):
    p = np.zeros(256)
    for i in range(256):
        p[i] = np.count_nonzero(y == i)/y.size
    return p

def uniformDistribution(y,p):
    y_uni = np.zeros(y.shape)
    for i in range(np.shape(y)[0]):
        for j in range(np.shape(y)[0]):
            p_m = int(y[i,j])
            #print(np.sum(p[:p_m]))
            
            y_uni[i,j] = np.floor((256-1)*np.sum(p[:p_m]))
            
    return y_uni

import matplotlib.pyplot as plt

def plothist(y):
    y_sort = np.sort(y.flatten())
    plt.figure()
    plt.plot(y_sort)
    plt.xlabel("Number of pixels")
    plt.ylabel("CDF")
    plt.show()

def main():
    
    #im_path = "cju5b9oyda4yr0850g9viziyv_clip.jpg"
    im_path = "im2.jpg"
    im_t_path = "theme4.png"
     
    #load images as numpy arrays
    im = loadIm(im_path) 
    im_t = loadIm(im_t_path)
    
    displayArrayIm(im)
    
    #im = cv2.detailEnhance(im, sigma_s=10, sigma_r=0.15)
    #displayArrayIm(im)
     
    #convert im and im_t to YCbCr from RGB
    #also splits into the three components
    y,cb,cr = rgbToYCbCr(im)
    y_t,cb_t,cr_t = rgbToYCbCr(im_t)


    #normalize Y, Y_t, Cb_t and Cr_t
    #progress is getting faster
    y_min = np.amin(y)
    y_max = np.amax(y)
    
    y_t_min = np.amin(y_t)
    y_t_max = np.amax(y_t)
    
    y_norm = normalize(y,y_min,y_max)
    y_t_norm = normalize(y_t,y_t_min,y_t_max)
    cb_t_norm = normalize(cb_t, y_t_min, y_t_max)
    cr_t_norm = normalize(cr_t, y_t_min, y_t_max)

    
    ###########
    #Enhancement on y component
    
    #get cutoff and gain
    k = getCutoff(y_norm)
    g = getGain(y_norm,k)
        
    #sigmoid function, using cutoff and gain

    y_sig = sigmoid(y_norm,k,g)
    #y_sig is nosw an integer matrix of a sigmoid image, with values from 0 to 255
    y_sig_ref = np.round(y_sig*255) #reference for making p

    p = histogram(y_sig_ref)

    #Uniform distribution of sigmoid pixels to increase the contrast level.
    y_uni = uniformDistribution(y_sig_ref, p)/255
    
    ############
    
    #y_uni = y_norm #quickfix to use if sigmoid enhancement will not be used
    
    #color change to retreive new chrominance values
    cb_new, cr_new = newChrominance(y_uni, y_t_norm, cb_t_norm, cr_t_norm)
    
    #unNormalize
    
    cb_new = unNormalize(cb_new, y_t)
    cr_new = unNormalize(cr_new, y_t)
    y = unNormalize(y_uni,y_t)
    
    
    #make RGB image of y, cb_n and cr_n
    r_new, g_new, b_new = yCbCrToRGB(y, cb_new, cr_new)
    im_new = (np.dstack((r_new,g_new,b_new))).astype(np.uint8)
    
    #im_new = cv2.detailEnhance(im_new, sigma_s=10, sigma_r=0.15)
    #displayArrayIm(im_new)
    
    #display (saving function later)
    displayArrayIm(im_new)
    
            
main()
        
            
            
            
            
            
            
            
            
            
            
            
            
            