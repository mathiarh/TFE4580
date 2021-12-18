#https://github.com/aladdinpersson/Machine-Learning-Collection/tree/master/ML/Pytorch/image_segmentation/semantic_segmentation_unet
#yt explenation: https://www.youtube.com/watch?v=IHq1t7NxS8k

import torch
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from tqdm import tqdm
import torch.nn as nn
import torch.optim as optim
from model import UNET
from model_pretrained import UNet11
from utils import (
    load_checkpoint,
    save_checkpoint,
    get_loaders,
    check_accuracy,
    save_predictions_as_imgs
)
from test import test

# Hyperparameters etc.
LEARNING_RATE = 1e-4
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
BATCH_SIZE = 8
NUM_EPOCHS = 15
NUM_WORKERS = 2
IMAGE_HEIGHT = 512
IMAGE_WIDTH = 512  
PIN_MEMORY = False
LOAD_MODEL = True

DATA_IMG_DIR = "/content/Kvasir-SEG/images"
DATA_MASK_DIR =  "/content/Kvasir-SEG/masks"
MODEL_NAME = "UNet11" #or "UNet"


def train_fn(loader, model, optimizer, loss_fn, scaler):
    loop = tqdm(loader)

    for batch_idx, (data, targets) in enumerate(loop):
        data = data.to(device=DEVICE)
        targets = targets.float().unsqueeze(1).to(device=DEVICE)

        # forward
        with torch.cuda.amp.autocast():
            predictions = model(data)
            loss = loss_fn(predictions, targets)

        # backward
        optimizer.zero_grad()
        scaler.scale(loss).backward()
        scaler.step(optimizer)
        scaler.update()

        # update tqdm loop
        loop.set_postfix(loss=loss.item())


def main():
    
    #test(height = IMAGE_HEIGHT, width=IMAGE_WIDTH, model_name = MODEL_NAME, device=DEVICE)
    
    
    train_transform = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Rotate(limit=35, p=1.0),
            A.HorizontalFlip(p=0.5),
            A.VerticalFlip(p=0.1),
            A.Normalize(
                mean=[0.5875, 0.3397, 0.2488],
                std=[.2966, .2138, .1840],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )
    
    val_transforms = A.Compose(
        [
            A.Resize(height=IMAGE_HEIGHT, width=IMAGE_WIDTH),
            A.Normalize(
                mean=[0.5875, 0.3397, 0.2488],
                std=[.2966, .2138, .1840],
                max_pixel_value=255.0,
            ),
            ToTensorV2(),
        ],
    )
    
    if MODEL_NAME == "UNet":
        model = UNET(in_channels=3, out_channels=1).to(DEVICE)
        model_path = "/content/drive/MyDrive/UNet_model.pth.tar"
    elif MODEL_NAME == "UNet11":
        model = UNet11().to(DEVICE)
        model_path = "/content/drive/MyDrive/UNet11_model.pth.tar"
    else:
        print("No model is specified")
    
    loss_fn = nn.BCEWithLogitsLoss()
    optimizer = optim.Adam(model.parameters(), lr=LEARNING_RATE)

    train_loader, val_loader = get_loaders(
        DATA_IMG_DIR,
        DATA_MASK_DIR,
        BATCH_SIZE,
        train_transform,
        val_transforms,
        NUM_WORKERS,
        PIN_MEMORY,
    )

    if LOAD_MODEL:
        load_checkpoint(torch.load(model_path), model)


    check_accuracy(val_loader, model, device=DEVICE)
    scaler = torch.cuda.amp.GradScaler()
    

    
    
    
    #FIND MEAN ANS STD
    channels_sum, channels_squares_sum, num_batches = 0,0,0
    for data, _ in train_loader:
        channels_sum += torch.mean(data, dim=[0,2,3])
        channels_squares_sum += torch.mean(data**2, dim=[0,2,3])
        num_batches+=1
        
    mean = channels_sum/num_batches
    std = (channels_squares_sum/num_batches-mean**2)**0.5
    print("Mean: ",mean)
    print("Std: ",std)
    

    

    
    for epoch in range(NUM_EPOCHS):
        print("Epoch nr: ",epoch+1, "/",NUM_EPOCHS)
        train_fn(train_loader, model, optimizer, loss_fn, scaler)

        # save model
        checkpoint = {
            "state_dict": model.state_dict(),
            "optimizer":optimizer.state_dict(),
        }
        save_checkpoint(checkpoint, model_path)

        # check accuracy
        #print("Train accuracy: ")
        #check_accuracy(train_loader, model, device=DEVICE)
        
        #print("Validation accuracy: ")
        check_accuracy(val_loader, model, device=DEVICE)
        

        # print some examples of validation data to a folder
        save_predictions_as_imgs(
            val_loader, model, folder="/content/drive/MyDrive/saved_images/", device=DEVICE
        )


    
    #find best threshold
    for st in np.arange(0.1,0.9,0.03):
        print("THRESH = ",st)
        check_accuracy(val_loader, model, threshold=st, device=DEVICE)
        

    #for testing after training:
    #test(height = IMAGE_HEIGHT, width=IMAGE_WIDTH, model_name = MODEL_NAME, device=DEVICE)

if __name__ == "__main__":
    main()
    