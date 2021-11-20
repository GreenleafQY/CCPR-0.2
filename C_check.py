import numpy as np
from PIL import Image
import csv
import copy


def Check_if_somebody(writer):

    hzg_data = []
    hzg_check = []

    ke_data = []
    ke_check = []

    zhuan_data = []
    zhuan_check = []

    hzg_check_float = []
    hzg_data_float = []
    ke_check_float = []
    ke_data_float = []

    probability_hzg_cal = 0
    probability_hzg = 0
    probability_ke_outer_cal = 0
    probability_ke_inner_cal = 0
    probability_ke = 0
    probability_zhuan_cal = 0
    probability_zhuan = 0
    probability = 0

    #1. 导入数据库
    #(1)横折钩曲度
    with open("./check/database/x_{}_hzg_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            hzg_data.append(row)

    #print("h_data", h_data)

    with open("./check/result/check_hzg_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            hzg_check.append(row)

    #print("h_check", h_check)

    for i in hzg_check[0]:
        i_f = float(i)
        hzg_check_float.append(i_f)

    hzg_check_max = max(hzg_check_float)
    #print("max", hzg_check_max)
    hzg_check_min = min(hzg_check_float)
    #print("min", hzg_check_min)

    for i in hzg_data[0]:
        i_f = float(i)
        hzg_data_float.append(i_f)

    hzg_data_max = max(hzg_data_float)
    hzg_data_min = min(hzg_data_float)

    if float(hzg_check[1][0])/float(hzg_data[1][0]) > 0:
        probability_hzg_cal = 1-abs(float(hzg_check[1][0])-float(hzg_data[1][0]))/abs(float(hzg_data[1][0]))

    probability_hzg *= probability_hzg_cal

    # print("probability_hzg", probability_hzg)
    # print("probability_hzg_cal", probability_hzg_cal)

    ke_outer_check_float = []
    ke_outer_data_float = []
    ke_inner_check_float = []
    ke_inner_data_float = []

    #2. "可"字转角比例
    with open("./check/database/x_{}_ke_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            ke_data.append(row)

    with open("./check/result/check_ke_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            ke_check.append(row)

    for i in ke_check[0]:
        i_f = float(i)
        ke_outer_check_float.append(i_f)

    ke_outer_check_max = max(ke_outer_check_float)
    ke_outer_check_min = min(ke_outer_check_float)

    for i in ke_data[0]:
        i_f = float(i)
        ke_outer_data_float.append(i_f)

    ke_outer_data_max = max(ke_outer_data_float)
    ke_outer_data_min = min(ke_outer_data_float)

    for i in ke_check[2]:
        i_f = float(i)
        ke_inner_check_float.append(i_f)

    ke_inner_check_max = max(ke_inner_check_float)
    ke_inner_check_min = min(ke_inner_check_float)

    for i in ke_data[2]:
        i_f = float(i)
        ke_inner_data_float.append(i_f)

    ke_inner_data_max = max(ke_inner_data_float)
    ke_inner_data_min = min(ke_inner_data_float)

    probability_ke_outer_cal = 1 - abs(float(ke_check[1][0]) - float(ke_data[1][0])) / abs(float(ke_data[1][0]))
    probability_ke_inner_cal = 1 - abs(float(ke_check[3][0]) - float(ke_data[3][0])) / abs(float(ke_data[3][0]))

    probability_ke = (probability_ke_outer_cal + probability_ke_inner_cal)/2

    # print("probability_ke", probability_ke)

    z_check_float = []
    z_data_float = []

    #3.转连笔比例
    with open("./check/database/x_{}_zhuan_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            zhuan_data.append(row)

    #print("z_data", z_data)

    with open("./check/result/check_zhuan_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            zhuan_check.append(row)

    #print("zhe_check", zhe_check)

    for i in zhuan_check[0]:
        i_f = float(i)
        zhuan_check_float.append(i_f)

    zhuan_check_max = max(zhuan_check_float)
    zhuan_check_min = min(zhuan_check_float)

    for i in zhuan_data[0]:
        i_f = float(i)
        zhuan_data_float.append(i_f)

    zhuan_data_max = max(zhuan_data_float)
    zhuan_data_min = min(zhuan_data_float)

    if float(zhuan_check[1][0])/float(zhuan_data[1][0]) > 0:
        probability_zhuan_cal = 1-abs(float(zhuan_check[1][0])-float(zhuan_data[1][0]))/abs(float(zhuan_data[1][0]))

    probability_zhuan *= probability_zhuan_cal

    # print("probability_zhuan", probability_zhuan)

    #4. 汇总概率

    if probability_hzg >0 and probability_ke >0 and probability_zhuan >0:
        probability = (probability_hzg + probability_ke + probability_zhuan)/3
    elif probability_hzg <=0 or probability_ke <=0 or probability_zhuan <=0:
        probability = 0

    # print("probability", probability)

    return probability

def Check_similarity():

    list_data = []
    h_check = []

    #1. 提取转的数据
    for name in ["c_zhzh"]:
        with open("./check/database/{}_hzg_result.csv".format(name), "r", newline='', encoding='GBK') as d:
            content = csv.reader(d)
            for i, rows in enumerate(content):
                if i == 3:
                    row = rows
                    list_data.append([name, row[0]])

    #print("list_data", list_data)

    famous = 0
    similarity_ratio = 0
    similarity_list = []

    #2. 对比转的数据，找出最接近的三人
    with open("./check/result/check_hzg_result.csv", "r", newline='', encoding='GBK') as d:
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
    probability = Check_if_somebody("ysn")
    print("probability_by_this_person", probability)

    #2. 检测与某人相似度
    first_name, First_similarity_probability, second_name, Second_similarity_probability, third_name, Third_similarity_probability = Check_similarity()
    print("Name:similarity", first_name, First_similarity_probability)
    print("Name:similarity", second_name, Second_similarity_probability)
    print("Name:similarity", third_name, Third_similarity_probability)








