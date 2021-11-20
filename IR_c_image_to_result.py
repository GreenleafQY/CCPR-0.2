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

    mark_index = df.loc[(df == 0).all(axis=1)].index
    df = df.drop(mark_index)

    df.to_csv('./check/image_to_data/check_{}.csv'.format(image_name), index=False, header=None)

def ke_data_extract(writer, num):

    list_data = []
    outer_ratio = 0
    inner_ratio = 0
    count_outer_right = []
    count_inner_right = []
    left_outer_edge = 0
    right_outer_edge = 0
    left_inner_edge = 0
    right_inner_edge = 0

    #1.读取csv数据
    with open("./check/image_to_data/{}_ke_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            list_data.append(row)

    # 2.提取外侧最右值并计算外侧转角的X轴映射长度
    for i in list_data:
        for j in range(0, len(i)):
            if i[j] == "0" and i[j - 1] != "0" and i[j - 2] != "0":
                count_outer_right.append(j)

    left_outer_edge = 0
    right_outer_edge = max(count_outer_right)

    # 3.提取内侧最左、最右值，并计算内侧转角的X轴映射长度
    for i in list_data:
        for j in range(0, len(i)-2):
            if i[j] == "0" and i[j + 1] != "0" and i[j + 2] != "0":
                count_inner_right.append(j)

    left_inner_edge = min(count_inner_right)
    right_inner_edge = max(count_inner_right)

    # 4.计算内外转角与纵轴的比例
    outer_ratio = round((right_outer_edge-left_outer_edge)/len(list_data),2)
    inner_ratio = round((right_inner_edge - left_inner_edge) / len(list_data), 2)

    return outer_ratio, inner_ratio

def Pool_ke_extract(writer):

    outer_ratio_list = []
    inner_ratio_list = []
    inter_ratio = 0
    z_ratio_expect = 0
    sum_outer_ratio = 0
    sum_inner_ratio = 0
    outer_ratio_expect = 0
    inner_ratio_expect = 0

    for num in range(1,4):
        outer_ratio, inner_ratio = ke_data_extract(writer, num)
        outer_ratio_list.append(outer_ratio)
        sum_outer_ratio += outer_ratio
        inner_ratio_list.append(inner_ratio)
        sum_inner_ratio += inner_ratio

    outer_ratio_expect = round(sum_outer_ratio/3, 2)
    inner_ratio_expect = round(sum_inner_ratio / 3, 2)

    print("expect_outer", outer_ratio_expect)
    print("inner_outer", inner_ratio_expect)

    with open("./check/result/{}_ke_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(outer_ratio_list)
        content.writerow([outer_ratio_expect])
        content.writerow(inner_ratio_list)
        content.writerow([inner_ratio_expect])

def Zhuan_data_extract(writer,num):

    zhuan_list = []
    right_a = 0
    right_b = 0
    tan_right_ratio = 0
    right_b_list = []
    right_value = 0
    index_i = 0

    # 1.读取csv数据
    with open("./check/image_to_data/{}_zhuan_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            zhuan_list.append(row)

    # 2.提取右侧夹角Tan值
    for i in zhuan_list[0]:
        index_i = zhuan_list[0].index(i)
        if i != "0 " and i != "0" and i != "":
            right_a = zhuan_list[0].index(i)

    for i in zhuan_list:
        index_i = zhuan_list.index(i)
        for j in range(0, len(i)):
            if i[j] == "0" and i[j-1] != "0" and i[j-2] != "0":
                right_b_list.append([index_i,j])

    right_b_list_1 = copy.deepcopy(right_b_list)
    for i in right_b_list:
        for j in right_b_list_1:
            if int(i[1]) > int(j[1]):
                right_b_list_1.remove(j)
            elif int(i[1]) == int(j[1]) and int(i[0]) < int(j[0]):
                right_b_list_1.remove(j)

    right_b = int(right_b_list_1[0][0])
    length = len(zhuan_list[0])

    zhuan_ratio = round(right_b/(length- right_a), 2)

    return zhuan_ratio

def Pool_zhuan_extract(writer):

    zhuan_ratio_list = []
    sum_zhuan_ratio = 0
    expected_zhuan_ratio = 0

    for num in range(1, 6):
        zhuan_ratio = Zhuan_data_extract(writer, num)
        zhuan_ratio_list.append(zhuan_ratio)
        sum_zhuan_ratio += zhuan_ratio

    expected_zhuan_ratio = round(sum_zhuan_ratio/5, 2)

    print("zhuan_ratio_list", zhuan_ratio_list)
    print("expect_zhuan", expected_zhuan_ratio)

    with open("./check/database/{}_zhuan_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(zhuan_ratio_list)
        content.writerow([expected_zhuan_ratio])

def hzg_data_extract(writer, num):

    hzg_data = []

    mid_x = 0
    left_half = 0
    right_half = 0

    count_mid = []
    count_left = []
    count_right = []

    mid_y = 0
    left_y = 0
    right_y = 0

    # 1.读取csv数据
    with open("./check/image_to_data/{}_hzg_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            hzg_data.append(row)

    # 2.提取三个点的Y值
    mid_x = int(len(hzg_data[0])/2)
    left_half = int(mid_x/2)
    right_half = int(mid_x + int(mid_x/2))

    for i in hzg_data:
        if i[mid_x] != "0":
            count_mid.append(i[mid_x])

    # print("count_mid", count_mid)

    mid_y = max(count_mid)
    # print("mid_y", mid_y)

    for i in hzg_data:
        if i[left_half] != "0":
            count_left.append(i[left_half])

    left_y = max(count_left)
    # print("left_y", left_y)

    for i in hzg_data:
        if i[right_half] != "0":
            count_right.append(i[right_half])

    right_y = max(count_right)
    # print("right_y", right_y)

    if int(mid_y)-int(left_y) != 0:
        hzg_ratio = round((int(mid_y) - int(right_y))/(int(mid_y) - int(left_y)), 2)
    else:
        hzg_ratio = 0

    return hzg_ratio

def Pool_hzg_extract(writer):

    hzg_ratio_list = []
    sum_hzg_ratio = 0

    for num in range(1, 6):
        hzg_ratio = hzg_data_extract(writer, num)
        hzg_ratio_list.append(hzg_ratio)
        sum_hzg_ratio += hzg_ratio

    expected_hzg_ratio = round(sum_hzg_ratio / 5, 2)

    print("hzg_ratio_list", hzg_ratio_list)
    print("expected_hzg_ratio", expected_hzg_ratio)

    with open("./check/result/{}_hzg_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(hzg_ratio_list)
        content.writerow([expected_hzg_ratio])


if __name__ == "__main__":

    #1. Image to Data
    for i in range(1, 4):
        image_name = "ke_" + str(i)
        Image_to_data(image_name)

    for i in range(1, 6):
        image_name = "zhuan_" + str(i)
        Image_to_data(image_name)

    for i in range(1, 6):
        image_name = "hzg_" + str(i)
        Image_to_data(image_name)

    # 2. ke提取值
    Pool_ke_extract("check")

    # 3. zhuan提取值
    Pool_zhuan_extract("check")

    # 4. hzg提取值
    Pool_hzg_extract("check")



