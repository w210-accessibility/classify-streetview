# Adapted from crop-images/updated_utils

import s3fs
import boto3

from pano_feats import Pano as Pano

import json
from PIL import Image
from io import BytesIO

bucket_img = "streetview-w210"
bucket_crops = "gsv-crops2"

# Load and view the images
fs = s3fs.S3FileSystem()
s3 = boto3.client('s3')
s3_r = boto3.resource('s3')


def make_mini_crops(pano_id, img_id, bucket_img = bucket_img, bucket_crops=bucket_crops):
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
    
	s3.put_object(Bucket=bucket_crops, Key=('mini-crops/')
    # Loop over all image crops here so we don't have to pull the image 7 times
	for crop_num in crop_id_list:
		img_filename  = 'mini-crops/' + img_id + '_' + str(crop_num) + '.jpg' 
        
		# Create the cropped image using passed in x,y coordinates as upper left corner
		sv_x, sv_y, crop_size = crop_dict[crop_num]
		cropped_square = im.crop((sv_x, sv_y, sv_x + crop_size, sv_y + crop_size))
        
		# Save the cropped file to S3
		buffer = BytesIO()
		cropped_square.save(buffer,'JPEG')
		buffer.seek(0)
		s3.put_object(Bucket=bucket_crops, Key=img_filename, Body=buffer)


def make_sliding_window_crops(list_of_panos, bucket_crops = bucket_crops, bucket_img = bucket_img):
    ''' take a text file containing a list of panos and add to dir'''

    num_panos = 0
    num_suc = 0
    num_fail  = 0

    for pano in list_of_panos:
        pano_id = pano.pano_id
        img_id = pano.img_id

        try:
            make_crops(pano_id, img_id, bucket_img, bucket_crops)
            num_suc += 1
        except Exception as e:
            print("\t cropping failed for {}".format(img_id))
            print(e)
            num_fail += 1
        num_panos += 1
    print("Finished. {} panos succeeded, {} failed.".format(num_suc, num_fail))
