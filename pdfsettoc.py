#!/usr/bin/env python
# coding: utf-8

"""
Spyder Editor

This is a temporary script file.
"""

#%% 导入必要的库
import sys, fitz, re
import pandas as pd
import re
import os
import textwrap
import math
import copy
'''
基本思想： 把读入的目录，化为这种格式  [数字， 字符串， 数字]， 第一个数字代表层级， 最后一个数字代表页码，最后生成data.frame
首先，把读入进来的文本，每一行进行空格切割（这个空格前面不能是\t和空格开头，后面必须要有文字）

然后，一般情况下，按照上述分割后，会分割成3列（理想的）， 对于非理想的情形进行处理，比如检查空字符串和空列表，以及分割以后不是3个的怎么办？

最后， 存为data.frame即可
'''


## 读取目录txt文件

def readtoc(filetxt):
    '''
    读取目录txt文件，返回一个list
    '''
    txt_raw = []
    with open(filetxt, "r", encoding='UTF-8') as f:
        for line in f.readlines():
            txt_raw.append(line.strip('\n')) # 读取文件时，删除换行符
    '''
    文本可能存在缩进，用缩进来代表目录层级关系。
    读取进来的文本按照空格进行分割， 这个空格要求 前面不能以 空格和\t开头， 空格后面非空格与\t的字符 
    '''
    txt = [re.split("(?<=[^ \t]) {1,10}(?=[^ \t])",x) for x in txt_raw]
    '''
    对分割后的数据进行检查处理
    1. 对空行的处理 -- 删除
    2。 对每一行，如果存在空字符串 “”  则删除
    '''

    while [] in txt:
        txt.remove([])
    while [""] in txt:
        txt.remove([""])
    [x.remove(y) for x in txt for y in x if y == ""]
    return txt


def txttotoc(txt,add_prefix=True):
    '''
    最终的目的: 返回一个:  [数字， 字符串， 数字] 这样的数据框,前三列
    第一个:代表层级(cengji),  第二个: 目录的内容(title),  第三个为页码(pages)
    其余后面的都是辅助列
    '''
    ###### 1.创建一个空的dataframe
    df = pd.DataFrame(columns = ["cengji", "title", "pages","three",  "txt","txt_count","newtxt","newtxt_one","newtxt_two","newtxt_three","newtxt_count"]) 
    # 其中 cengji 为整数，从 title 中提取的, 为: max(\t的个数, 小数点的个数) , 这里的小数点的前后都应该有数字
    # txt 为切割后的文本， txt_count 为 txt 每一行的个数
    # newtxt 表示是一个完全是三列的一个list 组成，即对txt的处理，把不是3的变成3 
    # newtxt_one newtxt_two newtxt_three 为newtxt拆分出来的第一列  第二列  第三列
    
    ##### 2. 生成 df[:, ['txt','txt_count']] 
    k = 0
    newtxt = copy.deepcopy(txt)
    for x in newtxt:
        n = len(x)
        if n == 0:
            newtxt.remove(x) # 理论上不可能，前面已经删除了
        if n == 1:
            # 默认为 newtxt_two
            x.insert(0," ")
            x.append(" ")
        if n == 2:
            # 检查第一个元素是否包含数字
            is_match_1 = re.findall(re.compile('[0-9一二三四五六七八九十]+?'), x[0])
            
            s0 = re.findall(re.compile('^([ \t]+)(?=[^\t ])'), x[0]) # 提取第一个元素中以 \t 开头的字符串
            if s0 == []:
                s0 = " "
            else:
                s0 = s0[0]
            # 检查第二个元素是否包含数字
            is_match_2 = re.findall(re.compile('[0-9]+?'), x[1])
            # 判断x[1] 是否能转为数字
            if is_match_2:
                try:
                    temp = int(x[1])
                    is_num = True
                except:
                    is_num = False
            else:
                is_num = False 
            
            
            ## 做选择
            if is_num:
                x.insert(0,s0)
            else:
                if is_match_1 and (not is_match_2):
                    x.append(" ")
                elif (not is_match_1) and is_match_2:
                    x.insert(0,s0)
                else:
                    x.append(" ")
        if n > 3:
            newtxt[k] = [x[0],"".join(x[1:-1]), x[-1]]
        df.loc[k, "txt"] = newtxt[k]
        df.loc[k, 'txt_count'] = n
        k = k + 1

    ##### 3. 生成 df[:,["newtxt","newtxt_one","newtxt_two","newtxt_three","newtxt_count"]]
    k = 0
    for x in newtxt:
        n = len(x)
        df.loc[k, "newtxt"] = x
        df.loc[k, 'newtxt_count'] = n
        k = k + 1
    val = df.apply(lambda x: x['newtxt_count'] == 3,axis=1)
    if all(val):
        print('数据处理正确')
    else:
        print("数据处理有问题")

    df['newtxt_one'] = df.apply(lambda x: x['newtxt'][0],axis=1)
    df['newtxt_two'] = df.apply(lambda x: x['newtxt'][1],axis=1)
    df['newtxt_three'] = df.apply(lambda x: x['newtxt'][2],axis=1)


    ''' 
    对层级的处理, 自定义一个函数， 统计字符串中出现  点的个数  和 \t的个数 两者的最大值 + 1
    点的个数，要求:这个点前后都要有数字
    '''
    def cengji_count(s):
        s.replace(" ",'')
        tab_count = re.findall(re.compile('\t'), s)
        tab_count = len(tab_count)
        dot_count = re.findall(re.compile('(?<=[0-9])(\\.)(?=[0-9])'), s)
        dot_count = len(dot_count)
        return max([tab_count+1, dot_count+1])

    df['cengji'] = df.apply(lambda x: cengji_count(x["newtxt_one"]),axis=1)

    '''
    对内容的处理 即 ， newtxt_one 和 newtxt_two 进行合并，即显示前面的前缀
    '''
    if add_prefix:
        df['title'] = df.apply(lambda x: re.sub(re.compile('[ \t]{1,100}'), "", x['newtxt_one']) + str(x['newtxt_two']),axis=1)
    else:
        df['title'] = df.apply(lambda x: str(x['newtxt_two']) ,axis=1)


    '''
    对页码的处理
    '''
    def yema(s):
        try:
            x = int(s)
        except:
            x = 0
        return x
    
    
    df['pages'] = df.apply(lambda x: yema(x["newtxt_three"]) ,axis=1)
    return df



########## 设置工作目录
# import os
# os.getcwd()   #查看当前工作路径
# os.chdir('/Users/zsc/pythonworkspaces')   #更改当前路径


####### 当前目录下得文本信息,以供选择
print('----  当前的工作路径: ' + os.getcwd() + ' 下的所有(仅包含后缀名为 pdf 和 txt )文件 -----') #获取当前工作目录路径

files_all = os.listdir(r'./')
files_pdf_and_txt = []
for x in files_all:
    if x.endswith(".pdf") or x.endswith(".txt"):
        files_pdf_and_txt.append(x)
files = files_pdf_and_txt # 只要后缀名为pdf和txt的文件
k = 0
for ii in files:
    print(str(k) +": " + ii)
    k = k + 1
print('------------------------------------------------------------------ ')

########### 读取文件
pdf_file_input = input("请输入pdf文件目录(输入数字选项 或 完整的文件名带后缀):")
try:
    xuan = int(pdf_file_input)
    pdf_file_input = files[xuan]
    pdf_file_output  = re.sub('.pdf$', '_含目录py.pdf', pdf_file_input, count=0, flags=0)
    pdf_rawtoc_file_output = re.sub('.pdf$', '_自带目录.txt', pdf_file_input, count=0, flags=0)
except:
    pdf_file_output = re.sub('.pdf$', '_含目录py.pdf', pdf_file_input, count=0, flags=0)
    pdf_rawtoc_file_output = re.sub('.pdf$', '_自带目录.txt', pdf_file_input, count=0, flags=0)

doc = fitz.open(pdf_file_input)
toctext = doc.get_toc(simple=True) # 原始pdf的目录

###### 存储原始文件的目录结构 --- 以缩进为主
file = open(pdf_rawtoc_file_output,'w');
for x in toctext:
    s = '\t'* (int(x[0])-1) + x[1] +" "+ str(x[2]) +'\n'
    file.write(s);
file.close();

filetxt = input("读取目录txt文件【可以用前面的数字选项，也可以选择txt】:")
try:
    xuan = int(filetxt)
    filetxt = files[xuan]
except:
    filetxt = filetxt
    
pdf_noffest = input("请输入偏移量【正整数, 默认为最小值的绝对值 +1，推荐为: 正文首页在整个pdf的页数 - 1 】: ")



################################################################################
####################  正式开始读取文件 ########################################
txt = readtoc(filetxt)
newtoc = txttotoc(txt)

try:
    noffest = int(pdf_noffest) #偏移量 --  一定要使得页码大于等于1,是第一章的页码 - 1
except:
    noffest = abs(newtoc.loc[:,'pages'].min()) + 1

newtoc['pages'] = newtoc.apply(lambda x: noffest + x['pages'], axis=1)

toc_df = newtoc.loc[:,['cengji','title','pages']]
toc_df['title'] = toc_df.apply(lambda x: re.sub("\t| ", "", x['title']), axis=1)

#### 检查输出的目录是否正确
s = toc_df.loc[:,'pages'].diff().dropna() 
if all(s >= 0):
    print('检查通过, 页码为非降序列')
else:
    print('检查不通过, 页码存在降序列')

### 把目录信息输出在终端   
# 空 --- 无意义

### 把data.frame 转为list
toc_list = toc_df.values.tolist() 

#### 输出文件
doc.set_toc(toc_list)
doc.save(pdf_file_output)
print('输出含目录的文件名：' + pdf_file_output)