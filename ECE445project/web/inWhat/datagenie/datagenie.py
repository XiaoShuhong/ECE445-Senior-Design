# from nl4dv.utils import constants, helpers
import json
import numpy as np
import os
import random
from tqdm import tqdm
import cv2
import random
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
# macro configration
Comb2idx = {
    ('tops', 'bottoms'):9,
    ('all-body', 'outerwear'):33,
    ('bottoms', 'outerwear'):43,
    ('tops', 'outerwear'):42,
}
colors_per_class = {
    'tops' : [254, 202, 87],
    'outerwear' : [255, 107, 107],
    'bottoms' : [10, 189, 227],
    'all-body' : [255, 159, 243]
}

# scale and move the coordinates so they fit [0; 1] range
def scale_to_01_range(x):
    # compute the distribution range
    value_range = (np.max(x) - np.min(x))

    # move the distribution so that it starts from zero
    # by extracting the minimal value from all its values
    starts_from_zero = x - np.min(x)

    # make the distribution fit [0; 1] by dividing by its range
    return starts_from_zero / value_range

def draw_rectangle_by_class(image, label):
    image_height, image_width, _ = image.shape

    # get the color corresponding to image class
    color = colors_per_class[label]
    image = cv2.rectangle(image, (0, 0), (image_width - 1, image_height - 1), color=color, thickness=5)

    return image

def scale_image(image, max_image_size):
    image_height, image_width, _ = image.shape

    scale = max(1, image_width / max_image_size, image_height / max_image_size)
    image_width = int(image_width / scale)
    image_height = int(image_height / scale)

    image = cv2.resize(image, (image_width, image_height))
    return image

# Compute the coordinates of the image on the plot
def compute_plot_coordinates(image, x, y, image_centers_area_size, offset):
    image_height, image_width, _ = image.shape

    # compute the image center coordinates on the plot
    center_x = int(image_centers_area_size * x) + offset

    # in matplotlib, the y axis is directed upward
    # to have the same here, we need to mirror the y coordinate
    center_y = int(image_centers_area_size * (1 - y)) + offset

    # knowing the image center,
    # compute the coordinates of the top left and bottom right corner
    tl_x = center_x - int(image_width / 2)
    tl_y = center_y - int(image_height / 2)

    br_x = tl_x + image_width
    br_y = tl_y + image_height

    return tl_x, tl_y, br_x, br_y

class DataGenie:
    def __init__(self, inWhat_instance, pathDict):
        self.inWhat_instance = inWhat_instance
        with open(pathDict["im2index"], 'r') as file_obj:
            self.im2index = json.load(file_obj)
        with open(pathDict["category2IMGS"], 'r') as file_obj:
            self.category2IMGS = json.load(file_obj)
        with open(pathDict["im2type"], 'r') as file_obj:
            self.im2type = json.load(file_obj)
        self.embeddings = np.load(pathDict["embeddings"])
    
    def tsneVis(self, catogoryComb):
        imgs_root =  os.path.join(self.inWhat_instance.data_root, "figure_data/polyvore_outfits/images/"),
        imgs_root = imgs_root[0]
        catoComb = catogoryComb
        catoCombIdx = Comb2idx[catoComb]
        imgPool = self.category2IMGS[catoComb[0]]+self.category2IMGS[catoComb[1]]
        # random.shuffle(imgPool)
        imgPool = random.sample(imgPool,1000)
        embeddings = self.embeddings

        ##1. construct the feature matrix for samples
        labels = []
        image_paths = []
        #first img
        curImgId = imgPool[0]
        curImgLabel = self.im2type[curImgId]
        labels.append(curImgLabel)
        image_paths.append(imgs_root+str(curImgId)+".jpg")
        curImgIdx = self.im2index[curImgId]
        curImgEmbedding1 = embeddings[curImgIdx][catoCombIdx]
        #second img
        curImgId = imgPool[1]
        curImgLabel = self.im2type[curImgId]
        labels.append(curImgLabel)
        image_paths.append(imgs_root+str(curImgId)+".jpg")
        curImgIdx = self.im2index[curImgId]
        curImgEmbedding2 = embeddings[curImgIdx][catoCombIdx]
        #starting features
        features = np.stack((curImgEmbedding1,curImgEmbedding2))
        # print(features)
        for i in range(2,len(imgPool)):
            curImgId = imgPool[i]
            curImgLabel = self.im2type[curImgId]
            labels.append(curImgLabel)
            image_paths.append(imgs_root+str(curImgId)+".jpg")
            curImgIdx = self.im2index[curImgId]
            curImgEmbedding = embeddings[curImgIdx][catoCombIdx]
            features = np.concatenate((features,curImgEmbedding[None, :]) )

        ##2. get the TSNE result
        tsne = TSNE(n_components=2).fit_transform(features)

        ##3. draw result
        # extract x and y coordinates representing the positions of the images on T-SNE plot
        tx = tsne[:, 0]
        ty = tsne[:, 1]

        tx = scale_to_01_range(tx)
        ty = scale_to_01_range(ty)

        plot_size = 1000
        max_image_size=100
        offset = max_image_size // 2
        image_centers_area_size = plot_size - 2 * offset
        images = image_paths

        # we'll put the image centers in the central area of the plot
        # and use offsets to make sure the images fit the plot

        # init the plot as white canvas
        tsne_plot = 255 * np.ones((plot_size, plot_size, 3), np.uint8)

        # now we'll put a small copy of every image to its corresponding T-SNE coordinate
        for image_path, label, x, y in tqdm(
                zip(images, labels, tx, ty),
                desc='Building the T-SNE plot',
                total=len(images)
        ):
            image = cv2.imread(image_path)

            # scale the image to put it to the plot
            image = scale_image(image, max_image_size)

            # draw a rectangle with a color corresponding to the image class
            image = draw_rectangle_by_class(image, label)

            # compute the coordinates of the image on the scaled plot visualization
            tl_x, tl_y, br_x, br_y = compute_plot_coordinates(image, x, y, image_centers_area_size, offset)

            # put the image to its t-SNE coordinates using numpy sub-array indices
            tsne_plot[tl_y:br_y, tl_x:br_x, :] = image

        cv2.imshow('t-SNE', tsne_plot)
        cv2.waitKey()