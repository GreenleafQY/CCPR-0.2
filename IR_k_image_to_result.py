import numpy as np
from PIL import Image
import csv
import copy
import pandas as pd


def Image_to_data(image_name):
    #图像转换为矩阵
    matrix=np.asarray(Image.open('./check/pre_settlement/{}.jpg'.format(image_name)))

    list_image = matrix.tolist()

    #print(list_image)

    count_deep = 0
    count_deep_list = []
    flag = 0
    array_after_chosen_shape = ()

    for i in list_image:
        flag += 1
        for j in i:
            count_deep = j[0]+j[1]+j[2]
            count_deep_list.append(count_deep)

    max_deep_list = max(count_deep_list)

    for i in list_image:
        index_i = list_image.index(i)
        for j in i:
            index_j = i.index(j)
            count_deep = j[0] + j[1] + j[2]
            if count_deep < (max_deep_list - 350):
                list_image[index_i][index_j]= [0, 0, 0]

    array_after_chosen = np.array(list_image)
    array_after_chosen_shape = array_after_chosen.shape
    a = array_after_chosen.reshape(array_after_chosen_shape[0],int(array_after_chosen_shape[1])*int(array_after_chosen_shape[2]))
    list_shu = a.tolist()

    index_i = 0

    for i in list_shu:
        for j in i:
            if i != 255:
                i = 1

    df = pd.DataFrame(list_shu)

    mark_index = df.loc[(df==0).all(axis=1)].index
    df = df.drop(mark_index)
    df = df.T

    mark_columns = df.loc[(df==0).all(axis=1)].index
    df = df.drop(mark_columns)
    df = df.T

    df.to_csv('./check/image_to_data/check_{}.csv'.format(image_name), index=False, header = None)

def Shu_data_extract(writer, num):

    list_data = []
    j_index = 0
    a = []
    c = []
    d = []
    e = []

    index_a = 0
    index_b = 0
    index_c = 0

    #1.读取csv数据
    with open("./check/image_to_data/{}_shu_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            list_data.append(row)

    #2.提取a/b点(竖的最宽处左右）下标值
    for i in list_data:
        if i[-1] != "0 " and i[-1] != "0":
            a = copy.deepcopy(i)
            index_ab = list_data.index(a)
            break
        else:
            pass

    x_index = []
    for i in range(len(a)):
        if a[i] in a[:i]:
            x_index.append(x_index[-1] + 1)
        else:
            x_index.append(a.index(a[i]))

    index_b = x_index[-1]

    for i in a:
        if i != "0" and i != "0 ":
            index_a = a.index(i)
            break

    index_ab_mid = (index_b-index_a)/2

    #3.提取c点(竖的底部中点，倒数2、3、4行均值）下标值
    c = list_data[-2]
    d = list_data[-3]
    e = list_data[-4]
    index_c = list_data.index(c)

    index_c_1 = 0
    index_c_2 = 0
    index_d_1 = 0
    index_d_2 = 0
    index_e_1 = 0
    index_e_2 = 0

    for i in c:
        if i != "0" and i != "0 ":
            index_c_1 = c.index(i)
            break

    for i in c:
        if i != "0" and i != "0 ":
            index_c_2 = c.index(i)

    index_c_cal_1 = (index_c_1 + index_c_2)/2

    for i in d:
        if i != "0" and i != "0 ":
            index_d_1 = d.index(i)
            break

    for i in d:
        if i != "0" and i != "0 ":
            index_d_2 = d.index(i)

    index_c_cal_2 = (index_d_1 + index_d_2) / 2

    for i in e:
        if i != "0" and i != "0 ":
            index_e_1 = e.index(i)
            break

    for i in e:
        if i != "0" and i != "0 ":
            index_e_2 = e.index(i)

    index_c_cal_3 = (index_e_1 + index_e_2) / 2

    index_c_mid = (index_c_cal_1 + index_c_cal_2 + index_c_cal_3) / 3

    # print("index_c_mid", index_c_mid)

    #计算最终比值（竖高/ab在水平线上的投影与c点的距离）
    height = index_c - index_ab
    shade_point = index_ab_mid - index_c_mid

    if shade_point != 0:
        mark_1_shu = height/shade_point
    elif shade_point == 0:
        mark_1_shu = 0

    # print("h", height)
    # print("p", shade_point)
    # print("m1", mark_1_shu)

    return height, shade_point, mark_1_shu

def Pool_shu_extract(writer):
    height_list = []
    shade_point_list = []
    mark_1_shu_list = []

    mark_1_shu_sum = 0
    mark_1_shu_expect = 0

    for num in range(1,6):
        height, shade_point, mark_1_shu = Shu_data_extract(writer, num)
        height_list.append(height)
        shade_point_list.append(shade_point)
        mark_1_shu_list.append(mark_1_shu)

    for i in mark_1_shu_list:
        mark_1_shu_sum += i

    mark_1_shu_expect = mark_1_shu_sum/20

    with open("./check/result/{}_shu_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(height_list)
        content.writerow(shade_point_list)
        content.writerow(mark_1_shu_list)
        content.writerow([mark_1_shu_expect])

def Kuan_data_extract(writer):

    kuan_data = []
    xi_data = []
    count_j = 0
    count_data = []
    max_data = 0
    max_min_ratio = 0

    #1.读取最宽笔画数据
    with open("./check/image_to_data/{}_kuan_1.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            kuan_data.append(row)

    # 2.读取最窄笔画数据
    with open("./check/image_to_data/{}_kuan_2.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            xi_data.append(row)

    #3.提取最宽值
    for i in kuan_data:
        if i[0] == "0" or i[0] == "0 ":
            for j in range(1, len(i)):
                if i[j] != "0" and i[j] != "0 ":
                    count_j += 1
            count_data.append(count_j)
            count_j = 0

    max_data = max(count_data)

    count_k = 0
    count_xi_data = []

    # 4.提取最窄值
    for i in xi_data:
        # if i[0] == "0" or i[0] == "0 ":
        for j in range(1, len(i)):
            if i[j] != "0" and i[j] != "0 ":
                count_k += 1
        count_xi_data.append(count_k)
        count_k = 0

    min_data = min(count_xi_data)

    max_min_ratio = max_data/min_data

    with open("./check/result/{}_kuan_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow([max_data])
        content.writerow([min_data])
        content.writerow([max_min_ratio])

    return max_data, min_data, max_min_ratio

def Na_data_extract(writer, num):
    na_list = []
    a = ""
    b = ""
    index_a = 0
    index_b = 0

    length = 0
    height = 0
    na_ratio = 0

    #1.读取csv数据
    with open("./check/image_to_data/{}_na_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            na_list.append(row)

    #print("na_list", na_list)
    index_i = 0
    lowest_point = 0

    #2.提取最低值
    for i in na_list[-1]:
        index_i = na_list[-1].index(i)
        if i != "0 " and i != "0" and i[-1] != "":
            a = copy.deepcopy(i)
            index_a = na_list[-1].index(i)
            break

    for i in na_list[-1]:
        index_i = na_list[-1].index(i)
        # print("index_i", index_i)
        # print("na_list[-1][index_i]", na_list[-1][index_i])
        # print("na_list[-1][index_i+1]", na_list[-1][index_i+1])
        # print("na_list[-1][index_i+2]", na_list[-1][index_i + 2])
        if i != "0 " and i != "0" and i[-1] != "":
            b = copy.deepcopy(i)
            if (na_list[-1][index_i + 1] and na_list[-1][index_i + 1] == b) and (na_list[-1][index_i + 2] and na_list[-1][index_i + 2]== b):
                index_b = index_i + 2
            else:
                index_b = index_i

    # print("a",a)
    # print('b', b)
    # print("index_a", index_a)
    # print("index_b", index_b)
    lowest_point = round((index_b + index_a)/2, 0)

    print("lowest_point", lowest_point)

    index_right_top = 0
    index_right_bottom = 0

    # 3.提取最右值
    for i in na_list:
        index_i = na_list.index(i)
        if i[-1] != "0 " and i[-1] != "0" and i[-1] != "":
            index_right_top = index_i
            break

    for i in na_list:
        index_i = na_list.index(i)
        if i[-1] != "0 " and i[-1] != "0" and i[-1] != "":
            index_right_bottom = index_i

    right_point = round((index_right_top + index_right_bottom)/2,0)

    length = len(na_list[-1]) - lowest_point
    height = len(na_list) - right_point

    print("length", length)

    #4. 计算斜率
    na_ratio = round(height / length, 2)

    #5. 计算斜线上的二分点、四分点的斜率
    k_mid = 0
    k_left = 0
    k_right = 0
    index_j = 0
    len_list = 0

    mid_point = int(lowest_point + length/2)

    len_list = len(na_list)

    for i in range(0, len_list):
        if na_list[i][mid_point] == "0":
            k_mid = round(int(i)/(int(mid_point)-length), 2)
        else:
            k_mid = 0

    print("na_ratio, k_mid", na_ratio, k_mid)

    return na_ratio, k_mid

def Pool_na_extract(writer):

    low_ratio_list = []
    right_ratio_list = []
    sum_low_ratio = 0
    sum_right_ratio = 0
    na_ratio_list = []
    k_mid_list = []
    k_left_list = []
    k_right_list = []
    sum_na_ratio = 0
    sum_k_mid = 0
    sum_k_left = 0
    sum_k_right = 0
    expected_na_ratio = 0
    expected_k_mid = 0
    expected_k_left = 0
    expected_k_right = 0

    for num in range(1, 6):
        na_ratio, k_mid = Na_data_extract(writer, num)
        na_ratio_list.append(na_ratio)
        k_mid_list.append(k_mid)
        sum_na_ratio += na_ratio
        sum_k_mid += k_mid

    expected_na_ratio = round(sum_na_ratio/5, 2)
    expected_k_mid = round(sum_k_mid/5, 2)

    with open("./check/result/{}_na_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(na_ratio_list)
        content.writerow([expected_na_ratio])
        content.writerow(k_mid_list)
        content.writerow([expected_k_mid])

def Zhe_data_extract(writer, num):

    zhe_list = []

    # 1.读取csv数据
    with open("./check/image_to_data/{}_zhe_{}.csv".format(writer, num), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            zhe_list.append(row)

    index_i = 0
    left_a = 0
    left_b = 0
    tan_left_ratio = 0

    right_a = 0
    right_b = 0
    tan_right_ratio = 0
    right_b_list = []

    # 2.提取左侧夹角Tan值
    for i in zhe_list[0]:
        index_i = zhe_list[0].index(i)
        if i != "0 " and i != "0" and i != "":
            a = copy.deepcopy(i)
            left_a = zhe_list[0].index(i)
            print("index", zhe_list[0].index(i))
            break

    print("left_a", writer, num, left_a)

    for i in zhe_list:
        index_i = zhe_list.index(i)
        if i[0] != "0 " and i[0] != "0" and i[0] != "":
            b = copy.deepcopy(i[0])
            left_b = zhe_list.index(i)
            break

    #print("left_b", left_b)

    tan_left_ratio = round(left_b/left_a, 2)

    #print("tan_left_ratio", tan_left_ratio)

    # 3.提取右侧夹角Tan值
    for i in zhe_list[0]:
        index_i = zhe_list[0].index(i)
        if i != "0 " and i != "0" and i != "":
            right_a = zhe_list[0].index(i)

    #print("right_a", right_a)

    right_value = 0

    for k in range(0, 10):
        for i in zhe_list[k]:
            index_i = zhe_list[k].index(i)
            if i != "0 " and i != "0" and i != "":
                right_value = zhe_list[k].index(i)
        right_b_list.append([right_value, k])

    #print("right_b_list", right_b_list)

    right_b_list_1 = copy.deepcopy(right_b_list)
    for i in right_b_list:
        for j in right_b_list_1:
            if i[0] > j[0]:
                right_b_list_1.remove(j)
            elif i[0] == j[0] and i[1] < j[1]:
                right_b_list_1.remove(j)

    right_b = right_b_list_1[0][1]

    #print("right_b", right_b)

    tan_right_ratio = round(right_b/right_a, 2)

    #print("tan_right_ratio", tan_right_ratio)

    return tan_left_ratio, tan_right_ratio

def Pool_zhe_extract(writer):

    tan_left_list = []
    tan_right_list = []
    sum_left_ratio = 0
    sum_right_ratio = 0

    for num in range(1, 6):
        tan_left_ratio, tan_right_ratio = Zhe_data_extract(writer, num)
        tan_left_list.append(tan_left_ratio)
        tan_right_list.append(tan_right_ratio)
        sum_left_ratio += tan_left_ratio
        sum_right_ratio += tan_right_ratio

    expected_tan_left_ratio = round(sum_left_ratio / 5, 2)
    expected_tan_right_ratio = round(sum_right_ratio / 5, 2)

    with open("./check/result/{}_zhe_result.csv".format(writer), "w", newline='', encoding='UTF-8') as d:
        content = csv.writer(d)
        content.writerow(tan_left_list)
        content.writerow([expected_tan_left_ratio])
        content.writerow(tan_right_list)
        content.writerow([expected_tan_right_ratio])


if __name__ == "__main__":

    #1. Image to Data
    for i in range(1, 6):
        image_name = "shu_"+ str(i)
        Image_to_data(image_name)

    for i in range(1, 6):
        image_name = "zhe_"+ str(i)
        Image_to_data(image_name)

    for i in range(1, 6):
        image_name = "na_"+ str(i)
        Image_to_data(image_name)

    for i in range(1, 3):
        image_name = "kuan_"+ str(i)
        Image_to_data(image_name)

    #2. Data to Result
    #(1)Shu提取值
    Pool_shu_extract("check")

    #(2)Kuan提取值
    Kuan_data_extract("check")

    #(3)Na提取值
    Pool_na_extract("check")

    #(4)Zhe提取值
    Pool_zhe_extract("check")



