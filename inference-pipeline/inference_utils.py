import pandas as pd
import os

def aggregate_by_test_image(df_final):
    # Get the img_id, heading and crop_num info
    df_final[['img_id', 'heading', 'crop_num']] = df_final['jpg_name'].str.strip('.jpg').str.split('_', expand = True)
    df_final['imgid_heading'] = df_final['img_id'].astype(str) + '_' + df_final['heading'].astype(str)
    
    # Group based on image, prediction and ground_truth
    df_group_final = df_final.groupby(['imgid_heading', 'prediction'])['jpg_name'].count()
    df_group_final = df_group_final.reset_index()
    
    df_group_final = df_group_final.sort_values(['imgid_heading', 'prediction'])
    
    df_group_top_vote = df_group_final.drop_duplicates(subset = 'imgid_heading', keep = 'first')
    
    return df_group_final, df_group_top_vote


def aggregate_by_image_with_groundtruth(df_final):
    # Get the img_id, heading and crop_num info
    df_final[['img_id', 'heading', 'crop_num']] = df_final['jpg_name'].str.strip('.jpg').str.split('_', expand = True)
    df_final['imgid_heading'] = df_final['img_id'].astype(str) + '_' + df_final['heading'].astype(str)
    
    # Group based on image, prediction and ground_truth
    df_group_final = df_final.groupby(['imgid_heading', 'prediction', 'ground_truth'])['jpg_name'].count()
    df_group_final = df_group_final.reset_index()
    
    df_group_final = df_group_final.sort_values(['imgid_heading', 'prediction'])
    
    df_group_top_vote = df_group_final.drop_duplicates(subset = 'imgid_heading', keep = 'first')
    
    return df_group_final, df_group_top_vote