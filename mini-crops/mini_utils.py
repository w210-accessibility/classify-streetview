# Adapted from crop-images/updated_utils

import s3fs
import boto3

import pandas as pd

import json
from PIL import Image
from io import BytesIO

bucket_img = "streetview-w210"
bucket_crops = "gsv-crops2"

# Load and view the images
fs = s3fs.S3FileSystem()
s3 = boto3.client('s3')
s3_r = boto3.resource('s3')


def sample_rows(df_split_set, num_examples, ground_truth_dict):
    dfs_list = []
    for key, gt_list in ground_truth_dict.items():
        print(f'{key} -> {gt_list}')
        df_part = df_split_set.loc[df_split_set['ground_truth'].isin(gt_list)]
        if num_examples > df_part.shape[0]:
            df_keep_part = df_part.copy()
        else:
            df_keep_part = df_part.sample(n = num_examples).copy()

        df_keep_part['folder_label'] = key
        dfs_list.append(df_keep_part)
    df_sample = pd.concat(dfs_list)
    return df_sample

bucket_img = "streetview-w210"
bucket_crops = "gsv-crops2"

# Load and view the images
fs = s3fs.S3FileSystem()
s3 = boto3.client('s3')
s3_r = boto3.resource('s3')

def make_mini_crops(img_id, bucket_img = bucket_img, bucket_crops=bucket_crops):
    # Create a dictionary of all crop values
    # key = crop_num, value = (sv_x, sv_y, crop_size)
    crop_dict = {'A':(5  ,320,180),
                 'B':(95,320,180),
                 'C':(185,320,180),
                 'D':(275,320,180),
                 'E':(365,320,180),
                 'F':(455,320,180)}
    crop_id_list = ['A', 'B', 'C', 'D', 'E', 'F']
    # Get the original image file
    path_to_image = "gsv/" + img_id + ".jpg"
    img_file = s3.get_object(Bucket=bucket_img, Key=path_to_image)['Body'].read()
    im = Image.open(BytesIO(img_file))
    
    s3.put_object(Bucket=bucket_crops, Key=(r'mini-crops/'))
    # Loop over all image crops here so we don't have to pull the image 6 times
    for ii, crop_num in enumerate(crop_id_list):
        img_filename  = 'mini-crops/' + img_id + '_' + str(crop_num) + '.jpg' 
        
        # Create the cropped image using passed in x,y coordinates as upper left corner
        sv_x, sv_y, crop_size = crop_dict[crop_num]
        cropped_square = im.crop((sv_x, sv_y, sv_x + crop_size, sv_y + crop_size))
        
        # Save the cropped file to S3
        buffer = BytesIO()
        cropped_square.save(buffer,'JPEG')
        buffer.seek(0)
        s3.put_object(Bucket=bucket_crops, Key=img_filename, Body=buffer)


def make_sliding_window_crops(list_img_id, bucket_crops = bucket_crops, bucket_img = bucket_img):
    ''' take a text file containing a list of panos and add to dir'''

    num_panos = 0
    num_suc = 0
    num_fail  = 0

    for img_id in list_img_id:

        try:
            make_mini_crops(img_id, bucket_img, bucket_crops)
            num_suc += 1
        except Exception as e:
            print("\t cropping failed for {}".format(img_id))
            print(e)
            num_fail += 1
        num_panos += 1
    print("Finished. {} panos succeeded, {} failed.".format(num_suc, num_fail))
                  
                  