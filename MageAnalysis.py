# -*- coding: utf-8 -*-
"""
Created on Wed May  1 20:20:32 2019

@author: Meng
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from skimage import data
from skimage.filters import threshold_otsu
from skimage.segmentation import clear_border
from skimage.measure import label
from skimage.morphology import closing, square
from skimage.measure import regionprops
from skimage.color import label2rgb

class ImageAnalysis():
    def __init__(self, value1, value2):
        self.img_before_tem = value1
        self.img_after_tem = value2
        self.Img_before = self.img_before_tem.copy()
        self.Img_after = self.img_after_tem.copy()
    def ApplyMask(self):
        thresh = threshold_otsu(self.Img_before)
        #mask = img_before > thresh # generate mask
        binarymask = closing(self.Img_before > thresh, square(3))
        self.mask = closing(self.Img_before > thresh, square(3))
        
        #fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        #ax.imshow(bw)# fig 2
        
        Segimg_bef = self.mask*self.Img_before.copy()
        Segimg_aft = self.mask*self.Img_after.copy()
              
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        ax.imshow(Segimg_bef) #fig 3
        
        return Segimg_bef, Segimg_aft, binarymask
    
        
    def Ratio(self, value1, value2):
        self.Segimg_bef_ratio = np.where(value1 == 0, 1, value1)
        Ratio = value2/self.Segimg_bef_ratio
        
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        ax.imshow(Ratio) #fig 3 
        return Ratio
    
    def ShowLabel(self, smallest_size, theMask, original_intensity):
        # remove artifacts connected to image border
        self.Labelmask = theMask
        self.OriginImag = original_intensity
        cleared = self.Labelmask.copy()
        clear_border(cleared)
        
        # label image regions
        label_image = label(cleared)
        #image_label_overlay = label2rgb(label_image, image=image)
        
        fig, ax = plt.subplots(ncols=1, nrows=1, figsize=(6, 6))
        ax.imshow(label_image)
        
        for region in regionprops(label_image,intensity_image=self.OriginImag):
        
            # skip small images
            if region.area < smallest_size:
                continue
        
            # draw rectangle around segmented coins
            minr, minc, maxr, maxc = region.bbox
            rect = mpatches.Rectangle((minc, minr), maxc - minc, maxr - minr,
                                      fill=False, edgecolor='red', linewidth=2)
            ax.add_patch(rect)
            centroidint1 = int(region.centroid[0])
            centroidint2 = int(region.centroid[1])
            ax.text(centroidint1+50, centroidint2+55, round(region.mean_intensity,3),fontsize=15,
                            style='italic',bbox={'facecolor':'red', 'alpha':0.5, 'pad':10})
            print(region.mean_intensity)
        
        plt.show() # fig 5