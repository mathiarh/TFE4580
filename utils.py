
import torch
import torchvision
from dataset import PolypDataset
from torch.utils.data import DataLoader
from torch.utils.data import Subset
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.metrics import roc_curve, auc


def save_checkpoint(state, filename="my_checkpoint.pth.tar"):
    print("=> Saving checkpoint")
    torch.save(state, filename)

def load_checkpoint(checkpoint, model):
    print("=> Loading checkpoint")
    model.load_state_dict(checkpoint["state_dict"])
    
    
def data_split(dataset, transform = None):
    val_split =.2
    train_idx, val_idx = train_test_split(list(range(len(dataset))), test_size=val_split)
    train_ds = Subset(dataset, train_idx)
    val_ds = Subset(dataset, val_idx)
    
    return train_ds, val_ds
    

def get_loaders(
    data_dir,
    data_maskdir,
    batch_size,
    train_transform,
    val_transform,
    num_workers=4,
    pin_memory=True,
):
    
    
    dataset = PolypDataset(
        image_dir=data_dir,
        mask_dir=data_maskdir,
        transform=train_transform,
    )
    
    train_ds, val_ds = data_split(dataset, transform = train_transform)
    
    train_loader = DataLoader(
        train_ds,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=True,
    )

    val_loader = DataLoader(
        val_ds,
        batch_size=batch_size,
        num_workers=num_workers,
        pin_memory=pin_memory,
        shuffle=False,
    )

    return train_loader, val_loader


def check_accuracy(loader, model, threshold = 0.43, device="cuda"):
    num_correct = 0
    num_pixels = 0
    dice_score = 0
    precision, recall = 0,0
    tot_tp, tot_fp, tot_fn, tot_tn = 0,0,0,0
    model.eval()
    prec3 = []
    with torch.no_grad():
        for x, y in loader:
            x = x.to(device)
            y = y.to(device).unsqueeze(1)
            preds = torch.sigmoid(model(x))
            #preds = (preds > threshold).float()
            #check that values in preds (and y) are only 1.0 or 0.0
            preds[preds>threshold] = 1.0
            preds[preds<=threshold] = 0.0
    
            num_correct += (preds == y).sum()
            num_pixels += torch.numel(preds)
            dice_score += (2 * (preds * y).sum()) / (
                (preds + y).sum() + 1e-8
            )
            
            true_pos = ((preds==1)&(y==1))
            false_neg = ((preds==0)&(y==1))
            false_pos = ((preds==1)&(y==0))
            true_neg = ((preds==0)&(y==0))
            tot_tp += float(torch.sum(true_pos))
            tot_fp += float(torch.sum(false_pos))
            tot_fn += float(torch.sum(false_neg))
            tot_tn += float(torch.sum(true_neg))
    print(
        f"Got {num_correct}/{num_pixels} with acc {num_correct/num_pixels*100:.2f}"
    )
    print(f"Dice score old: {dice_score/len(loader)}")
    print(f"Recall from fn and tp: {tot_tp/(tot_tp+tot_fn)}")
    print(f"Precision fom tp and fp: {tot_tp/(tot_tp+tot_fp)}")
    print(f"Dice from tp, fp and fn: {2*tot_tp/(2*tot_tp+tot_fp+tot_fn)}")
    model.train()
    #return None


def save_predictions_as_imgs(
    loader, model, threshold=0.43, folder="saved_images/", device="cuda"
):
    model.eval()
    for idx, (x, y) in enumerate(loader):
        x = x.to(device=device)
        with torch.no_grad():
            preds = torch.sigmoid(model(x))
            preds = (preds > threshold).float()
        torchvision.utils.save_image(
            preds, f"{folder}/pred_{idx}.png"
        )
        torchvision.utils.save_image(y.unsqueeze(1), f"{folder}{idx}.png")

    model.train()