import os
import numpy as np
import cv2
import pandas as pd

path = r"V:\grid_layout"
file = r"combined.csv"

combined_df = pd.read_csv(os.path.join(path, file))
# lines_df = pd.read_csv(os.path.join(path, "lines_data_text_files", "lines_30.txt"), header = None, sep = ",")
combined_df.head()

grid = np.zeros((64,64),np.uint)

df = combined_df.copy()

df['bbox'] = df['bbox'].apply(eval)

df['width'] = df['bbox'].apply(lambda x: x[2] - x[0])
df['height'] = df['bbox'].apply(lambda y: y[3] - y[1])
df['image_height'] = df['shape'].apply(lambda z: z.split(" ")[1])
df['image_width'] = df['shape'].apply(lambda z: z.split(" ")[0])

def cal_row(n_rows, x_left, text_width, image_width):
    row_i = n_rows*(x_left + (text_width/2))/image_width
    return row_i

def cal_col(n_cols, y_top, text_height, image_height):
    col_i = n_cols*(y_top + (text_height/2))/image_height
    return col_i

rows, cols = [], []
for i in df.index:
    rows.append(cal_row(64, df['bbox'][i][0], df['width'][i], int(df['image_width'][i])))
    cols.append(cal_col(64, df['bbox'][i][2], df['height'][i], int(df['image_height'][i])))

df['row'] = rows
df['col'] = cols

import math
df['int_row'] = df['row'].apply(lambda x: int(x))
df['int_col'] = df['col'].apply(lambda x: int(x))
df['floor_row'] = df['row'].apply(lambda x: math.ceil(x))
df['floor_col'] = df['col'].apply(lambda x: math.ceil(x))

df_ = df.copy()
df_ = df_[df['image']=='30.png']

rows = df_['floor_row'].to_list()

z = zip(rows[:-1], rows[1:])

# count = 0
# for i, j in z:
#     if i == j:
#         rows[1:][count] = rows[1:][count]+1
        
count = 0
for i, j in z:
    if i == j:
        print(count, i, j)
    count+=1
        # rows[1:][count] = rows[1:][count]+1