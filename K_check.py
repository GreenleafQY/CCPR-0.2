import numpy as np
from PIL import Image
import csv
import copy


def Check_if_somebody(writer):

    shu_data = []
    shu_check = []
    na_data = []
    na_check = []
    zhe_data = []
    zhe_check = []
    kuan_data = []
    kuan_check = []

    shu_check_float = []
    shu_data_float = []
    probability_shu = 1
    probability_shu_cal = 0

    na_check_float = []
    na_left_check_float = []
    na_right_check_float = []
    na_data_float = []
    na_left_data_float = []
    na_right_data_float = []
    probability_na = 1
    probability_na_left = 0
    probability_na_right = 0
    probability_na_cal = 0

    zhe_check_float = []
    zhe_left_check_float = []
    zhe_right_check_float = []
    zhe_data_float = []
    zhe_left_data_float = []
    zhe_right_data_float = []
    probability_zhe = 1
    probability_zhe_left = 0
    probability_zhe_right = 0
    probability_zhe_left_right = 0

    kuan_check_float = []
    kuan_data_float = []
    probability_kuan = 1

    probability = 0

    #1. 导入数据库
    #(1)竖
    with open("./check/database/{}_shu_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            shu_data.append(row)

    #print("shu_data", shu_data)

    with open("./check/result/check_shu_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            shu_check.append(row)

    #print("shu_check", shu_check)

    for i in shu_check[2]:
        i_f = float(i)
        shu_check_float.append(i_f)

    shu_check_max = max(shu_check_float)
    #print("max", shu_check_max)
    shu_check_min = min(shu_check_float)
    #print("min", shu_check_min)

    for i in shu_data[2]:
        i_f = float(i)
        shu_data_float.append(i_f)

    shu_data_max = max(shu_data_float)
    shu_data_min = min(shu_data_float)

    # if shu_check_max <= shu_data_max and shu_check_min >= shu_data_min:
    #     probability_shu = 1
    # else:
    #     probability_shu = 0.75

    if float(shu_check[3][0])/float(shu_data[3][0]) > 0:
        probability_shu_cal = 1-abs(float(shu_check[3][0])-float(shu_data[3][0]))/abs(float(shu_data[3][0]))

    probability_shu *= probability_shu_cal

    # print("probability_shu", probability_shu)
    # print("probability_shu_cal", probability_shu_cal)

    #2. 捺
    with open("./check/database/{}_na_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            na_data.append(row)

    #print("na_data", na_data)

    with open("./check/result/check_na_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            na_check.append(row)

    print("na_check", na_check)

    for i in na_check[0]:
        i_f = float(i)
        na_check_float.append(i_f)

    na_check_max = max(na_check_float)
    na_check_min = min(na_check_float)

    for i in na_data[0]:
        i_f = float(i)
        na_data_float.append(i_f)

    na_data_max = max(na_data_float)
    na_data_min = min(na_data_float)

    # if na_check_max <= na_data_max and na_check_min >= na_data_min:
    #     probability_na = 1
    # else:
    #     probability_na = 0.75

    probability_na_cal = 1 - abs(float(na_check[1][0]) - float(na_data[1][0])) / abs(float(na_data[1][0]))
    probability_na_cal_mid = 1 - abs(float(na_check[3][0]) - float(na_data[3][0])) / abs(float(na_data[3][0]))

    probability_na = probability_na_cal * probability_na_cal_mid

    # print("probability_na", probability_na)
    # print("probability_na_cal", probability_na_cal)

    #3.折
    with open("./check/database/{}_zhe_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            zhe_data.append(row)

    #print("zhe_data", zhe_data)

    with open("./check/result/check_zhe_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            zhe_check.append(row)

    #print("zhe_check", zhe_check)

    for i in zhe_check[0]:
        i_f = float(i)
        zhe_left_check_float.append(i_f)

    zhe_left_check_max = max(zhe_left_check_float)
    zhe_left_check_min = min(zhe_left_check_float)

    for i in zhe_data[0]:
        i_f = float(i)
        zhe_left_data_float.append(i_f)

    zhe_left_data_max = max(zhe_left_data_float)
    zhe_left_data_min = min(zhe_left_data_float)

    for i in zhe_check[2]:
        i_f = float(i)
        zhe_right_check_float.append(i_f)

    zhe_right_check_max = max(zhe_right_check_float)
    zhe_right_check_min = min(zhe_right_check_float)

    for i in zhe_data[2]:
        i_f = float(i)
        zhe_right_data_float.append(i_f)

    zhe_right_data_max = max(zhe_right_data_float)
    zhe_right_data_min = min(zhe_right_data_float)

    # if zhe_left_check_max <= zhe_left_data_max and zhe_left_check_min >= zhe_left_data_min and zhe_right_check_max <= zhe_right_data_max and zhe_right_check_min >= zhe_right_data_min:
    #     probability_zhe = 1
    # else:
    #     probability_zhe = 0.75

    if float(zhe_check[1][0])/float(zhe_data[1][0]) > 0:
        probability_zhe_left = 1-abs(float(zhe_check[1][0])-float(zhe_data[1][0]))/abs(float(zhe_data[1][0]))
    if float(zhe_check[3][0]) / float(zhe_data[3][0]) > 0:
        probability_zhe_right = 1 - abs(float(zhe_check[3][0]) - float(zhe_data[3][0])) / abs(float(zhe_data[3][0]))

    probability_zhe_left_right =  (probability_zhe_left + probability_zhe_right)/2

    probability_zhe *= probability_zhe_left_right

    # print("probability_zhe", probability_zhe)
    # print("probability_zhe_left_right", probability_zhe_left_right)

    #4. 宽窄
    with open("./check/database/{}_kuan_result.csv".format(writer), "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            kuan_data.append(row)

    # print("kuan_data", kuan_data)

    with open("./check/result/check_kuan_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            kuan_check.append(row)

    # print("kuan_check", kuan_check)

    probability_kuan = 1 - abs(float(kuan_check[2][0]) - float(kuan_data[2][0])) / abs(float(kuan_data[2][0]))

    # print("probability_kuan", probability_kuan)

    #5. 汇总概率

    if probability_shu >0 and probability_na >0 and probability_zhe >0 and probability_kuan >0:
        probability = (probability_shu + probability_na + probability_zhe + probability_kuan)/4
    elif probability_shu <=0 or probability_na <=0 or probability_zhe <=0 or probability_kuan <=0:
        probability = 0

    # print("probability", probability)

    return probability

def Check_similarity():

    list_data = []
    shu_check = []

    #1. 提取竖的数据
    for name in ["zy", "wxz", "xianzhi", "yzq1", "yzq2", "csl", "ysn", "lgq", "oyx", "ss", "mf", "htj", "zj", "zmf", "nz", "dqc",
                 "wzm", "dsr", "qg"]:
        with open("./check/database/{}_shu_result.csv".format(name), "r", newline='', encoding='GBK') as d:
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
    with open("./check/result/check_shu_result.csv", "r", newline='', encoding='GBK') as d:
        content = csv.reader(d)
        for row in content:
            shu_check.append(row)

    # print("shu_check", shu_check)

    for i in list_data:
        famous = float(i[1])
        similarity_ratio = float(shu_check[3][0])/famous
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
        if float(shu_check[3][0])/float(i[1]) == first_ratio:
            first_name = i[0]
        elif float(shu_check[3][0])/float(i[1]) == second_ratio:
            second_name = i[0]
        elif float(shu_check[3][0])/float(i[1]) == third_ratio:
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








