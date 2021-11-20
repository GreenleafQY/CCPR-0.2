import numpy as np
from PIL import Image
import csv
import copy


def Check_if_somebody(writer):

    h_data = []
    h_check = []

    gou_data = []
    gou_check = []

    z_data = []
    z_check = []

    h_check_float = []
    h_data_float = []
    gou_check_float = []
    gou_data_float = []

    probability_h_cal = 0
    probability_h = 0
    probability_gou_left_cal = 0
    probability_gou_right_cal = 0
    probability_gou = 0
    probability_z_cal = 0
    probability_z = 0
    probability = 0


    #1. 导入数据库
    #(1)上下位移
    with open("./check/database/x_{}_h_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            h_data.append(row)

    #print("h_data", h_data)

    with open("./check/result/check_h_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            h_check.append(row)

    #print("h_check", h_check)

    for i in h_check[0]:
        i_f = float(i)
        h_check_float.append(i_f)

    h_check_max = max(h_check_float)
    #print("max", h_check_max)
    h_check_min = min(h_check_float)
    #print("min", h_check_min)

    for i in h_data[0]:
        i_f = float(i)
        h_data_float.append(i_f)

    h_data_max = max(h_data_float)
    h_data_min = min(h_data_float)

    if float(h_check[1][0])/float(h_data[1][0]) > 0:
        probability_h_cal = 1-abs(float(h_check[1][0])-float(h_data[1][0]))/abs(float(h_data[1][0]))

    probability_h *= probability_h_cal

    # print("probability_h", probability_h)
    # print("probability_h_cal", probability_h_cal)

    gou_left_check_float = []
    gou_left_data_float = []
    gou_right_check_float = []
    gou_right_data_float = []

    #2. 勾
    with open("./check/database/x_{}_gou_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            gou_data.append(row)

    with open("./check/result/check_gou_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            gou_check.append(row)

    for i in gou_check[0]:
        i_f = float(i)
        gou_left_check_float.append(i_f)

    gou_left_check_max = max(gou_left_check_float)
    gou_left_check_min = min(gou_left_check_float)

    for i in gou_data[0]:
        i_f = float(i)
        gou_left_data_float.append(i_f)

    gou_left_data_max = max(gou_left_data_float)
    gou_left_data_min = min(gou_left_data_float)

    for i in gou_check[2]:
        i_f = float(i)
        gou_right_check_float.append(i_f)

    gou_right_check_max = max(gou_right_check_float)
    gou_right_check_min = min(gou_right_check_float)

    for i in gou_data[2]:
        i_f = float(i)
        gou_right_data_float.append(i_f)

    gou_right_data_max = max(gou_right_data_float)
    gou_right_data_min = min(gou_right_data_float)

    probability_gou_left_cal = 1 - abs(float(gou_check[1][0]) - float(gou_data[1][0])) / abs(float(gou_data[1][0]))
    probability_gou_right_cal = 1 - abs(float(gou_check[3][0]) - float(gou_data[3][0])) / abs(float(gou_data[3][0]))

    probability_gou = (probability_gou_left_cal + probability_gou_right_cal)/2

    # print("probability_gou", probability_gou)

    z_check_float = []
    z_data_float = []

    # #3."之"字比例
    # with open("./check/database/x_{}_z_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
    #     content = csv.reader(d)
    #     for row in content:
    #         z_data.append(row)
    #
    # #print("z_data", z_data)
    #
    # with open("./check/result/check_z_result.csv", "r", newline='', encoding='GBK') as d:
    #     content = csv.reader(d)
    #     for row in content:
    #         z_check.append(row)
    #
    # #print("zhe_check", zhe_check)
    #
    # for i in z_check[0]:
    #     i_f = float(i)
    #     z_check_float.append(i_f)
    #
    # z_check_max = max(z_check_float)
    # z_check_min = min(z_check_float)
    #
    # for i in z_data[0]:
    #     i_f = float(i)
    #     z_data_float.append(i_f)
    #
    # z_data_max = max(z_data_float)
    # z_data_min = min(z_data_float)
    #
    # if float(z_check[1][0])/float(z_data[1][0]) > 0:
    #     probability_z_cal = 1-abs(float(z_check[1][0])-float(z_data[1][0]))/abs(float(z_data[1][0]))
    #
    # probability_z *= probability_z_cal
    # # print("probability_z", probability_z)

    #4. 汇总概率

    if probability_h >0 and probability_gou >0:
        probability = (probability_h + probability_gou)/2
    elif probability_h <=0 or probability_gou <=0:
        probability = 0

    # print("probability", probability)

    return probability

def Check_similarity():

    list_data = []
    h_check = []

    #1. 提取左右位移的数据
    for name in ["x_lj", ]:
        with open("./check/database/{}_h_result.csv".format(name), "r", newline='', encoding='GBK') as d:
            content = csv.reader(d)
            for i, rows in enumerate(content):
                if i == 3:
                    row = rows
                    list_data.append([name, row[0]])

    #print("list_data", list_data)

    famous = 0
    similarity_ratio = 0
    similarity_list = []

    #2. 对比竖的数据，找出最接近的三人
    with open("./check/result/check_h_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            h_check.append(row)

    for i in list_data:
        famous = float(i[1])
        similarity_ratio = float(h_check[3][0])/famous
        similarity_list.append(similarity_ratio)

    similarity_list_1 = copy.deepcopy(similarity_list)

    for i in similarity_list_1:
        if i > 1 or i <0:
            similarity_list.remove(i)

    # print("similarity_list", similarity_list)

    similarity_list = sorted(similarity_list, reverse=True)

    # print("similarity_list", similarity_list)

    first_ratio = similarity_list[0]
    second_ratio = similarity_list[1]
    third_ratio = similarity_list[2]

    # print("first_ratio", first_ratio)
    # print("s_ratio", second_ratio)
    # print("t_ratio", third_ratio)

    for i in list_data:
        if float(h_check[3][0])/float(i[1]) == first_ratio:
            first_name = i[0]
        elif float(h_check[3][0])/float(i[1]) == second_ratio:
            second_name = i[0]
        elif float(h_check[3][0])/float(i[1]) == third_ratio:
            third_name = i[0]

    First_similarity_probability = Check_if_somebody(first_name)
    Second_similarity_probability = Check_if_somebody(second_name)
    Third_similarity_probability = Check_if_somebody(third_name)

    return first_name, First_similarity_probability, second_name, Second_similarity_probability, third_name, Third_similarity_probability

if __name__ == "__main__":

    #1. 检测是否某人作品
    probability = Check_if_somebody("x_lj")
    print("probability_by_this_person", probability)

    #2. 检测与某人相似度
    first_name, First_similarity_probability, second_name, Second_similarity_probability, third_name, Third_similarity_probability = Check_similarity()
    print("Name:similarity", first_name, First_similarity_probability)
    print("Name:similarity", second_name, Second_similarity_probability)
    print("Name:similarity", third_name, Third_similarity_probability)








