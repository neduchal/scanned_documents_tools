#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cv2
import numpy as np
import glob
import os.path

# SETTINGS PART
input_dir_ext = './input/*.jpg' # Input directory and extension
output_dir = './output/' # output directory
border = 30 # Border width [size of the border should be proportional to the siye of the image] 


def main():
    files = glob.glob(input_dir_ext)
    files = sorted(files)
    for file in files:
        basename = os.path.basename(file)
        print basename
        if os.path.isfile(output_dir + "bg_" +basename[:-4] + ".jpg"):
            continue
        image_full_rgb = cv2.imread(file)
        image_full = cv2.imread(file, 0)
        blur = cv2.blur(image_full, (128, 128))
        val = np.mean(blur)
        ret, ret2 = cv2.threshold(image_full, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = np.ones((2, 2), np.uint8)
        ret2 = cv2.dilate(ret2, kernel, iterations=2)
        ret2 = cv2.blur(ret2, (5, 5))
        result = image_full_rgb.copy()

        result_b = result[:,:,0]
        result_g = result[:,:,1]
        result_r = result[:,:,2]

        val = []
        val.append(np.mean(result_b[ret2 == 0]))
        val.append(np.mean(result_g[ret2 == 0]))
        val.append(np.mean(result_r[ret2 == 0]))

        result_b[ret2 > 0] = val[0]
        result_g[ret2 > 0] = val[1]
        result_r[ret2 > 0] = val[2]
        result[:,:,0] = result_b
        result[:,:,1] = result_g
        result[:,:,2] = result_r


        j, i = np.nonzero(ret2)

        for l in range(3):
            for k in range(len(j)):
                if i[k] < border or j[k] < border:
                    result[j[k],i[k], l] = val[l]
                elif i[k] > ret2.shape[1] - border or  j[k] > ret2.shape[0] - border:
                    result[j[k],i[k], l] = val[l]
                else:
                    result[j[k],i[k], l] = np.median(result[j[k]-border:j[k]+border, i[k]-border:i[k]+border, l])

        cv2.imwrite(output_dir + "bg_" +basename[:-4] + ".jpg", result)

if __name__ == "__main__":
    main()
