import numpy as np
from PIL import Image
import csv
import copy
import pandas as pd


def Image_to_data(image_name):
    #图像转换为矩阵
    matrix=np.asarray(Image.open('./check/pre_settlement/{}.jpg'.format(image_name)))

    list_image = matrix.tolist()

    array_after_chosen = np.array(list_image)
    array_after_chosen_shape = array_after_chosen.shape
    a = array_after_chosen.reshape(array_after_chosen_shape[0],int(array_after_chosen_shape[1]) * int(array_after_chosen_shape[2]))
    list_shu = a.tolist()

    df = pd.DataFrame(list_shu)

    # mark_index = df.loc[(df == 0).all(axis=1)].index
    # df = df.drop(mark_index)

    df.to_csv('./check/image_to_data/check_{}.csv'.format(image_name), index=False, header=None)

def Z_data_extract(writer, num):

    list_data = []
    z_ratio = 0

    #1.读取csv数据
    with open("./check/image_to_data/{}_z_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            list_data.append(row)

    z_ratio = round(len(list_data[0])/ len(list_data), 2)
    #print("z_ratio", z_ratio)

    return z_ratio

def Pool_z_extract(writer):

    z_ratio_list = []
    sum_z_ratio = 0
    z_ratio_expect = 0

    for num in range(1,6):
        z_ratio = Z_data_extract(writer, num)
        z_ratio_list.append(z_ratio)
        sum_z_ratio += z_ratio

    #print("sum", sum_z_ratio)

    z_ratio_expect = round(sum_z_ratio/5, 2)

    print("expect_z", z_ratio_expect)

    with open("./check/result/{}_z_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(z_ratio_list)
        content.writerow([z_ratio_expect])

def H_data_extract(writer,num):

    h_s_data = []
    h_x_data = []
    count_left_s = []
    count_right_s = []
    count_left_x = []
    count_right_x = []

    #1.读取数据
    with open("./check/image_to_data/{}_h_{}_s.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            h_s_data.append(row)

    #print("h_s", h_s_data)

    with open("./check/image_to_data/{}_h_{}_x.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            h_x_data.append(row)

    #print("h_x", h_x_data)

    # 2.提取上方数据
    for i in h_s_data:
        for j in range(0, len(i)-2):
            if i[j] == "0" and i[j+1] != "0" and i[j+2] != "0":
                count_left_s.append(j)

    if count_left_s != []:
        left_edge_s = min(count_left_s)
    else:
        left_edge_s = 0

    for i in h_s_data:
        for j in range(0, len(i)):
            if i[j] == "0" and i[j - 1] != "0" and i[j - 2] != "0":
                count_right_s.append(j)

    if count_right_s != []:
        right_edge_s = max(count_right_s)
    else:
        right_edge_s = len(h_s_data)

    #print("left_edge_s", left_edge_s)
    #print("right_edge_s", right_edge_s)

    mid_s = int((right_edge_s - left_edge_s)/2)

    #print("mid_s", mid_s)

    # 3.提取下方数据
    for i in h_x_data:
        for j in range(0, len(i) - 2):
            if i[j] == "0" and i[j + 1] != "0" and i[j + 2] != "0":
                count_left_x.append(j)

    if count_left_x != []:
        left_edge_x = min(count_left_x)
    else:
        left_edge_x = 0

    for i in h_x_data:
        for j in range(0, len(i)):
            if i[j] == "0" and i[j - 1] != "0" and i[j - 2] != "0":
                count_right_x.append(j)

    if count_right_x != []:
        right_edge_x = max(count_right_x)
    else:
        right_edge_x = len(h_x_data)

    #print("left_edge_x", left_edge_x)
    #print("right_edge_x", right_edge_x)

    mid_x = int((right_edge_x - left_edge_x) / 2)

    #print("mid_x", mid_x)

    h_ratio = round((mid_x - mid_s)/len(h_s_data),2)

    print("h_ratio", h_ratio)

    return h_ratio

def Pool_h_extract(writer):

    h_ratio_list = []
    sum_h_ratio = 0
    expected_h_ratio = 0

    for num in range(1, 6):
        h_ratio = H_data_extract(writer, num)
        h_ratio_list.append(h_ratio)
        sum_h_ratio += h_ratio

    expected_h_ratio = round(sum_h_ratio/5, 2)

    print("expect_h", expected_h_ratio)

    with open("./check/result/{}_h_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(h_ratio_list)
        content.writerow([expected_h_ratio])

def Gou_data_extract(writer, num):

    gou_data = []
    count_left = []
    count_right = []
    left_edge = 0
    right_edge = 0
    lowest_point = 0

    index_a = 0
    index_b = 0

    # 1.读取csv数据
    with open("./check/image_to_data/{}_gou_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            gou_data.append(row)

    #print("gou_list", gou_data)

    # 2.提取最左值
    for i in gou_data:
        for j in range(1, len(i)-2):
            if i[j] == "0" and i[j+1] != "0" and i[j+2] != "0":
                count_left.append(j)

    #print("count_left", count_left)
    left_edge = min(count_left)
    #print("left_edge", left_edge)

    # 3.提取最右值
    for i in gou_data:
        for j in range(0, len(i)):
            if i[j] == "0" and i[j-1] != "0" and i[j-2] != "0":
                count_right.append(j)

    #print("count_right", count_right)
    right_edge = max(count_right)
    #print("right_edge", right_edge)

    # 4.提取最下值
    for i in gou_data[-1]:
        index_i = gou_data[-1].index(i)
        if i != "0 " and i != "0" and i[-1] != "":
            a = copy.deepcopy(i)
            index_a = gou_data[-1].index(i)
            break

    for i in gou_data[-1]:
        index_i = gou_data[-1].index(i)
        if i != "0 " and i != "0" and i[-1] != "":
            b = copy.deepcopy(i)
            if (gou_data[-1][index_i + 1] and gou_data[-1][index_i + 1] == b) and (gou_data[-1][index_i + 2] and gou_data[-1][index_i + 2]== b):
                index_b = index_i + 2
            else:
                index_b = index_i

    lowest_point = int((index_b + index_a)/2)

    #print("lowset_point", lowest_point)

    # if int(lowest_point) < int(left_edge):
    #     left_edge = lowest_point

    width = int(right_edge) - int(left_edge)
    mid_left_ratio = round((int(lowest_point)-int(left_edge))/width, 2)
    right_mid_ratio = round((int(right_edge)-int(lowest_point))/width, 2)

    print("mid_left_ratio", mid_left_ratio)
    print("right_mid_ratio", right_mid_ratio)

    return mid_left_ratio, right_mid_ratio

def Pool_gou_extract(writer):

    mid_left_ratio_list = []
    right_mid_ratio_list = []
    sum_mid_left_ratio = 0
    sum_right_mid_ratio = 0

    for num in range(1, 6):
        mid_left_ratio, right_mid_ratio = Gou_data_extract(writer, num)
        mid_left_ratio_list.append(mid_left_ratio)
        right_mid_ratio_list.append(right_mid_ratio)
        sum_mid_left_ratio += mid_left_ratio
        sum_right_mid_ratio += right_mid_ratio

    expected_mid_left_ratio = round(sum_mid_left_ratio / 5, 2)
    expected_right_mid_ratio = round(sum_right_mid_ratio / 5, 2)

    #print("expected_mid_left_ratio", expected_mid_left_ratio)
    #print("expected_right_mid_ratio", expected_right_mid_ratio)

    with open("./check/result/{}_gou_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(mid_left_ratio_list)
        content.writerow([expected_mid_left_ratio])
        content.writerow(right_mid_ratio_list)
        content.writerow([expected_right_mid_ratio])


if __name__ == "__main__":

    #1. Image to Data
    for i in range(1, 6):
        image_name = "h_" + str(i) + "_s"
        Image_to_data(image_name)

    for i in range(1, 6):
        image_name = "h_" + str(i) + "_x"
        Image_to_data(image_name)

    for i in range(1, 6):
        image_name = "gou_" + str(i)
        Image_to_data( image_name)

    for i in range(1, 6):
        image_name = "z_" + str(i)
        Image_to_data(image_name)

    # 2. Z提取值
    Pool_z_extract("check")

    # 3. H提取值
    Pool_h_extract("check")

    # 4. Gou提取值
    Pool_gou_extract("check")




