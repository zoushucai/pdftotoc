# 导入必要的库
import sys
import fitz
import pandas as pd
import re
import os

########################################################################
################### 通过前面数字和点这种格式来识别生成目录   ########################
########################################################################


def readtoc(filetxt,isrmt = True,isrmn = True):
    txt = []
    with open(filetxt, "r") as f:
        for line in f.readlines():
            if isrmn:
                line = line.strip('\n')  #去掉列表中每一个元素的换行符
            if isrmt:
                line = line.strip('\t')
            txt.append(line)
            #print(line)
    return txt



## 对删除了换行符和制表符的文本进行处理--- 处理成我们想要的格式
def txtTotoc(txt,offset = 0 ,isrmnum = False):
    '''
    参数txt：表示文本经过删除换行符和制表符处理后的文本数据，一行一个字符串
    offset：表示目录的偏移量， 支持负数
    '''
    newtxt =list()
    k=0
    for i in txt:
        # 第一层
        s = re.findall(r'^[0-9 \.]{1,10}(?=[^0-9])',i)
        s = ''.join(s)#把list转为str，每个list之间用‘’链接
        s_temp = s.strip()#删除字符串两边的空格
        first_ceng = s_temp.count('.')+1
        ## 第三层
        jiewei_num = r'-?[\d ]+$'
        s3=re.findall(jiewei_num,i)
        three_ceng = ''.join(s3).strip()
        ## 第二层
        scend_ceng = re.split(jiewei_num,i)[0]
        scend_ceng = scend_ceng.strip()
        if isrmnum:
            scend_ceng = scend_ceng.replace(s_temp,'').strip()
        if three_ceng == '':
            three_ceng = 0
        else:
            three_ceng = int(three_ceng)
        three_ceng = three_ceng + offset
        ss = [int(first_ceng), scend_ceng, three_ceng]
        newtxt.append(ss)
    return newtxt


def readtocToNewtoc(file_txt,offset=14, is_tab = True, is_num=True, isrm_num = False):
    if is_tab and is_num:
        txt1 = readtoc(file_txt,isrmt=False)
        newtoc1 = txtTotoc(txt1, offset = offset, isrmnum=isrm_num)
        txt2 = readtoc(file_txt)
        newtoc2 = txtTotoc(txt2, offset = offset, isrmnum=isrm_num)
        newtoc = list()
        for i in range(len(newtoc2)):
            fisrt_ceng = max(newtoc2[i][0],newtoc2[i][0])
            ss = [ fisrt_ceng, newtoc2[i][1], newtoc2[i][2] ]
            newtoc.append(ss)
    elif is_tab and not(is_num):
        txt = readtoc(file_txt,isrmt=False)
        newtoc = txtTotoc(txt, offset = offset, isrmnum=isrm_num)
    elif not(is_tab) and is_num:
        txt = readtoc(file_txt)
        newtoc = txtTotoc(txt, offset = offset, isrmnum=isrm_num)
    else:
        print('出错')
    return newtoc

print('------------------------------ ')
print("当前的工作路径: " + os.getcwd()) #获取当前工作目录路径

######## 当前目录下的所有文件 

'''
src_dir = r'./'      # 源文件目录地址
def list_all_files(rootdir):
    _files = []
    #列出文件夹下所有的目录与文件
    list_file = os.listdir(rootdir)
    for i in range(0,len(list_file)):
        # 构造路径
        path = os.path.join(rootdir,list_file[i])
        # 判断路径是否是一个文件目录或者文件
        # 如果是文件目录，继续递归
        if os.path.isdir(path):
            _files.extend(list_all_files(path))
        if os.path.isfile(path):
             _files.append(path)
    return _files
files = list_all_files(src_dir)
'''

files = os.listdir(r'./')
print('------ 当前目录下的所有文件 ----- ')
for ii in files:
    print(ii)
print('------------------------------ ')
###########

# 读取文件

pdf_file_input = input("请输入pdf文件目录(包含该文件的后缀，回车结束输入):")
pdf_file_output = re.sub('.pdf$', '_含目录py.pdf', pdf_file_input, count=0, flags=0)

pdf_pianyiliang = input("请输入偏移量(整数，一定要使得页码大于等于1):")
n = int(pdf_pianyiliang) #偏移量 --  一定要使得页码大于等于1

doc = fitz.open(pdf_file_input)
toctext = doc.get_toc(simple=True)

## 读取目录txt文件
filetxt = input("读取目录txt文件:")
txt = readtoc(filetxt=filetxt,isrmt=True,isrmn=True)
print("从目录txt中提取的目录结构：")
print(txt[0:5])
newtoc1 = txtTotoc(txt, offset=n, isrmnum=False)# 结尾不能有空格


# 二维list 美化代码
df = pd.DataFrame(newtoc1, columns=['one', 'two', 'three'])
print('新的目录结构：')
print(df.head(10))
newtoc = readtocToNewtoc(filetxt,offset=n)
newtoc_df = pd.DataFrame(newtoc, columns=['one', 'two', 'three'])
print('处理以后，要写入的目录：')
print(newtoc_df.head(10))

doc.setToC(newtoc)
doc.save(pdf_file_output)
print('输出含目录的文件名：' + pdf_file_output)