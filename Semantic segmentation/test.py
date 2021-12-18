#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 30 13:54:26 2021

@author: mathiasrammhaugland
"""

from model import UNET
from model_pretrained import UNet11
from dataset import PolypDataset
import albumentations as A
from albumentations.pytorch import ToTensorV2
from utils import (load_checkpoint, check_accuracy, save_predictions_as_imgs)
import torch
from torch.utils.data import DataLoader
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image


def get_test_loader(img_path, mask_path, transform, batch_size = 1, num_workers=2, pin_memory = False):
    test_set = PolypDataset(
        image_dir=img_path,
        mask_dir=mask_path,
        transform=transform,
    )
    test_loader = DataLoader(
        test_set,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=False,
    )
    return test_loader

def prcurve(loader, model, device="cuda"):
    num_correct = 0
    num_pixels = 0
    dice_score = 0
    precision, recall = 0,0
    model.eval()
    tp,fp, fn, tn, tptp,fpfp, tntn, fnfn=[],[],[],[], [],[],[],[]
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device).unsqueeze(1)
            modd = model(x)
            #preds = (preds > threshold).float()
            #check that values in preds (and y) are only 1.0 or 0.0
            precisionarr =[]
            recallarr=[]
            for threshold in np.arange(0.0,1.0,0.01):
                preds = torch.sigmoid(modd)
                preds[preds>threshold] = 1.0
                preds[preds<=threshold] = 0.0
                
                #num_correct += (preds == y).sum()
                #num_pixels += torch.numel(preds)
                
                true_pos = ((preds==1)&(y==1))
                false_neg = ((preds==0)&(y==1))
                false_pos = ((preds==1)&(y==0))
                true_neg = ((preds==0)&(y==0))

                tp.append(float(torch.sum(true_pos)))
                fp.append(float(torch.sum(false_pos)))
                fn.append(float(torch.sum(false_neg)))
                tn.append(float(torch.sum(true_neg)))
            #print("---")
            #print(precisionarr[15])
            #print(recallarr[15])
            fpfp.append(fp)
            tptp.append(tp)
            fnfn.append(fn)
            tntn.append(tn)
            tp,fp,fn,tn=[],[],[],[]
    print("fp:")
    print(np.average(fpfp,axis=0))
    print("tp.")
    print(np.average(tptp,axis=0))
    print("tn:")
    print(np.average(tntn,axis=0))
    print("fn:")
    print(np.average(fnfn,axis=0))


def test(height, width, model_name, device):
    
    test_transform = A.Compose(
        [
            A.Resize(height=height, width=width),
            A.Normalize(
                mean=[0.5875, 0.3397, 0.2488],
                std=[.2966, .2138, .1840],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )

    test_img_path = "/content/CVC-ClinicDB/CVC_612/images"
    test_mask_path = "/content/CVC-ClinicDB/CVC_612/masks"
    #test_img_path = "/content/Kvasir-SEG/images"
    #test_mask_path =  "/content/Kvasir-SEG/masks"
    
    #For testing and getting individual images
    #test_img_path = "/content/testbilder/tr3/images"
    #test_mask_path = "/content/testbilder/tr3/masks"
    
    model_name = "UNet"
    if model_name == "UNet":
        model = UNET(in_channels=3, out_channels=1).to(device)
        model_path = "/content/drive/MyDrive/UNet_model.pth.tar"
    elif model_name == "UNet11":
        model = UNet11().to(device)
        model_path = "/content/drive/MyDrive/UNet11p_model.pth.tar"
        #rewrite to ...UNet11p.... if using pretrained
    else:
        print("No model is specified")
    
    load_checkpoint(torch.load(model_path), model)
    
    test_loader = get_test_loader(test_img_path, test_mask_path, test_transform)
    
    check_accuracy(test_loader, model, device=device)
    prcurve(test_loader,model,device=device)
    
    
    
    
    
    #save_predictions_as_imgs(test_loader, model, folder = "/content/drive/MyDrive/preds", device=device)
    print("DONE TESTING")