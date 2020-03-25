import pandas as pd


def is_label_in_roi(x_pt, y_pt, x_left, x_right, y_top, y_bottom):
    # Where x_pt and y_pt are the coordinate location of x and y
    # x_left and x_right are the vertical bounds
    # y_top and y_bottom are the horizontal bounds of the square
    # Note that the point (0, 0) is in the top left corner
    
    # We'll just assume the point is positive 
    if (x_left < x_pt < x_right) and (y_top < y_pt < y_bottom):
        return True
    else:
        return False
    
    
def get_label_roi(x_pt, y_pt, list_coors):
    # Where there's a list of lists
    # The sublists have the following order
    
    result_dict = {}
    
    for coor in list_coors:
        result_dict[coor[0]] = is_label_in_roi(x_pt, y_pt, coor[1], coor[2], coor[3], coor[4])
        
    return result_dict

def df_coor_to_list(df_coor):
    # Given a dataframe with 7 rows, 1 per crop
    # Transform into a list
    # That can be consumed by get_label_roi
    keep_cols = ['crop_number', 'x_crop_left',
       'x_crop_right', 'y_crop_top', 'y_crop_bottom']
    list_coors = df_coor[keep_cols].values.tolist()
    return list_coors