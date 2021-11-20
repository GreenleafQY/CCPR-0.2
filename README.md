# What's CCPR?
  
  CCPR is the abbreviation of Chinese Calligraphy and Painting Recognition.
  
  This project's purpose is to try using the way of comparison to recognize the famous Chinese calligraphies and Paintings. The algorithm is based on the judicial expertise principles.

# Version

- This CWPR 0.0.2 includes the methods of decerning regular script, running script and cursive script , with 57 famous ancient Chinese calligraphers' characteristic values(if a calligrapher both good at regular script and running script, he was double-counted).  

- The ongoing version will be extended to more calligraphers,  and paintings.

- Updated to intelligent pretreatment.

# System

- Windows 10

# Python Version

- Python 3.6

# Necessary libs

- numpy 1.19.5
- PIL
- csv
- pandas 1.1.5

# How to use

- Preparation
 -Choose a to-be-tested regular script image, turn it into black-and_white model with photoshop. If the charactors are in black, use reverse to make the handwritings into white, and the background into black.
 -Take out the following strokes with the pen tool of photoshop, rub the background as clean as possible.
  For regular script（k)： 
  - Five vertical("shu") images
  - Five right-falling stroke("na") images
  - Five horizontal-turning("hengzhe") images
  - The widest vertical and the slimmest vertical images
  For running script（x):
  - Five hook("gou") images
  - Cut five lines, and then  take the first charactor of a line as h_(num of this line, from 1 to 5)_s, and the charactor most near the right edge(if the line right-tilt) or left edge(if the line left-tilt) as h_(num of this line, from 1 to 5)_x. 	
 For cursive script（c):
  - Five joined-up ("zhuan") images
  - Five ending images if they are horizontal("hzg").	
 -Replace those images of the following dir: /check/pre_settlement with correct file_names("kuan_1" for the widest vertical and "kuan_2" for the  slimmest vertical for regular script(k))
 -Use IR_k/x/c_image_to_result.py to get the characteristic values of the testing script.

- If you want to compare the  to-be-tested handwriting with one of the 57  calligraphers, use the function "Check_if_somebody("")" in K/X/C_check.py, and enter the abbreviation of the  calligrapher' name plus "k"/"x"/"c" and a "_" ahead of the name.

- If you don't know who to compare with, use the function " Check_similarity()" function in K/X/C_check.py, it may provide three of the neareast and the similiarity with this calligrapher's style.


  - A complete list of the abbreviation of the Chinese calligraphers' names:
    -“hx" for "Huang Xiang"("皇象")
    - "zhzh" for "Zhang Zhi"("张芝") 
    - "lj" for "Lu Ji"("陆机") 
    - "sj" for "Suo Jing"("索靖") 
    - "zy" for "Zhong You"("钟繇")
    - "wxz" for "Wang Xizhi"("王羲之")
    - "xianzhi" for "Wang Xianzhi"("王献之")
    - "wx" for "Wang Xun"("王珣") 
    - "csl" for "Chu Suiliang"("褚遂良")
    - "ysn" for "Yu Shinan"("虞世南")
    - "oyx" for "Ouyang Xun"("欧阳询")
    - "yzq" for "Yan Zhenqing"("颜真卿")
    - "lgq" for "Liu Gongquan"("柳公权")
    - "dm" for "Du Mu"("杜牧")
    - "lb" for "Li Bai"("李白")
    - "zhx" for "zhang Xu"("张旭")
    - "hs" for "Huai Su"("怀素")
    - "yns" for "Yang Ningshi"("杨凝式")
    - "ss" for "Su Shi"("苏轼")
    - "mf" for "Mi Fu"("米芾")
    - "cx" for "Cai Xiang"("蔡襄")
    - "zj" for "Zhao Ji"(宋徽宗"赵佶")
    - "zmf" for "Zhao Mengfu"("赵孟頫")
    - "nz" for "Ni Zan"("倪瓒")
    - "dqc" for "Dong Qichang"("董其昌")
    - "wzm" for "Wen Zhengming"("文征明")
    - "ty" for "Tang Yin"("唐寅")
    - "wd" for "Wang Duo"("王铎")
    - "hl" for "Hong Li"(乾隆皇帝"弘历")
    - "dsr" for "Deng Shiru"("邓石如")
    - "qg" for "Qi Gong"("启功")


# License and Use

Greenleaf © 2021 



    

  


