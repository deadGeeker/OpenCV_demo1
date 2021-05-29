import cv2
import argparse
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("--image", action = "append", type = str, help = "image path")
args = ap.parse_args()

if args.image:
    if len(args.image) > 1:
        image1 = cv2.imread(args.image[0])
        image2 = cv2.imread(args.image[1])
    else:
        image = cv2.imread(args.image[0])