# 导入必要的库
import sys, fitz, re
import pandas as pd
import re
import os
import textwrap
import math
########################################################################
################### 通过前面数字和点这种格式来识别生成目录   ########################
########################################################################


def readtoc(filetxt,is_rmt = True,is_rmn = True):
    ''' 
    is_rmt  是否删除目录中的 制表符 \t, 默认删除
    is_rmn  是否删除目录中的 换行符  \n， 默认删除
    '''
    txt = []
    with open(filetxt, "r") as f:
        for line in f.readlines():
            if is_rmn:
                line = line.strip('\n')  #去掉列表中每一个元素的换行符
            if is_rmt:
                line = line.strip('\t')
            txt.append(line)
            #print(line)
    return txt



## 对删除了换行符和制表符的文本进行处理--- 处理成我们想要的格式
def txtTotoc(txt,offset = 0 ,isrmnum = True,isrmt = True):
    '''
    参数txt：表示文本经过删除换行符和制表符处理后的文本数据，一行一个字符串
    offset：表示目录的偏移量， 支持负数
    isrmnum 是否删除 第二层中的 章节标号
    isrmt 是否删除 \t, 不删除，则会在原有章节的层次计数
    '''
    if isrmt==True: 
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
            if not(isrmnum):
                scend_ceng = scend_ceng.replace(s_temp,'').strip()
            if three_ceng == '':
                three_ceng = 0
            else:
                three_ceng = int(three_ceng)
            three_ceng = three_ceng + offset
            ss = [int(first_ceng), scend_ceng, three_ceng]
            newtxt.append(ss)
        return newtxt
    else:
        newtxt =list()
        k=0
        for i in txt:
            # 第一层
            s = re.findall(r'^[0-9 \.]{1,10}(?=[^0-9])',i)
            s = ''.join(s)#把list转为str，每个list之间用‘’链接
            s_temp = s.strip()#删除字符串两边的空格
            first_ceng = s_temp.count('.')+1
            ## 按照 . 进行分层， 然后在. 的基础上 增加\t 分层
            ## 即， 如果当前层含有点， 则不计算\t, 如果没有，则增加\t分层
            first_t_ceng = i
            if first_t_ceng.startswith('\t'):
                first_ceng += first_t_ceng.count('\t') # toc中文字中间也不能有\t
            else:
                first_ceng += 0
            ## 第三层
            jiewei_num = r'-?[\d ]+$'
            s3=re.findall(jiewei_num,i)
            three_ceng = ''.join(s3).strip()
            ## 第二层
            scend_ceng = re.split(jiewei_num,i)[0]
            scend_ceng = scend_ceng.strip()
            if not(isrmnum):
                scend_ceng = scend_ceng.replace(s_temp,'').strip()
            if three_ceng == '':
                three_ceng = 0
            else:
                three_ceng = int(three_ceng)
            three_ceng = three_ceng + offset
            ss = [int(first_ceng), scend_ceng, three_ceng]
            newtxt.append(ss)
        return newtxt
        
# def str_count_width(s):
#     # 需要re模块
#     hanzi_regex = re.compile(r'[？！：\u4E00-\u9FA5]')
#     t_regex= re.compile(r'\t')
#     s_hanzi = len(hanzi_regex.findall(s))# 计算字符串中汉字的个数
#     s_t = len(t_regex.findall(s)) # 计算字符串中\t 的个数
#     raw_s_len = len(s) # 把汉字以及\t都计算，即原始字符串的长度， 一个汉字长度为1
#     s_width = raw_s_len - s_hanzi - s_t + s_hanzi*2 + s_t*8
#     return s_width

def readtocToNewtoc(file_txt,offset=14, is_rmt = True,is_rmn = True, isrmnum = True, isrmt = True):
    ''' 参数解释：
    offset：表示目录的偏移量， 支持负数
    is_rmt  是否删除目录中的 制表符 \t, 默认删除
    is_rmn  是否删除目录中的 换行符  \n， 默认删除
    
    isrmnum 是否删除 第二层中的 章节标号
    isrmt 是否删除 \t, 不删除，则会在原有章节的层次计数
    '''
    txt = readtoc(filetxt=filetxt, is_rmt = is_rmt, is_rmn = is_rmn)
    newtoc = txtTotoc(txt,offset = offset, isrmnum = isrmnum, isrmt = isrmt)
    # print("从目录txt中提取的目录结构：")
    # kk = 0;
    # for i in txt:
    #     print(i)
    #     kk = kk + 1
    #     if kk ==30:
    #         break;
    
    # newtoc = txtTotoc(txt,offset = offset, isrmnum = isrmnum, isrmt = isrmt)
    # ## 美化输出    
    # df = pd.DataFrame(newtoc, columns=['one', 'two', 'three'])
    # print('新的目录结构：')
    # print(df.head(30))

    kk = 30;
    ss_0 = "从目录txt中提取的目录结构："
    ss_1 = "新的目录结构:"
    max_txt_len = max([len(x) for x in txt[:kk]])
    max_newtoc_len = max([len(str(x)) for x in newtoc[:kk]])
    max_newtoc_len
    max_len = max(max_txt_len,max_newtoc_len)


    max_len2 = math.ceil(max_len/10)*10*2

    #print(os.get_terminal_size().columns) # 打印终端字符宽度
    #str_temp= "{:<"+ str(max_len2) + "}   |   {:<" + str(max_len2)+ "}"
    #print(str_temp) 

    hanzi_regex = re.compile(r'[？！：\u4E00-\u9FA5]')
    t_regex= re.compile(r'\t')

    for i in range(kk):
        #print("{:>40}   |   {:<40}".format(txt[i], str(newtoc[i]) ))

        txt_s = txt[i]
        newtoc_s = "    ".join(map(str,newtoc[i]))
        txt_hanzi = len(hanzi_regex.findall(txt_s))
        newtoc_hanzi = len(hanzi_regex.findall(newtoc_s))

        txt_t = len(t_regex.findall(txt_s))*7
        newtoc_t = len(t_regex.findall(newtoc_s))*7
        #print(len(txt[i])
        print(txt_s.ljust(max_len2 - txt_hanzi - txt_t," ") + "|        " + newtoc_s.ljust(max_len2 - newtoc_hanzi - newtoc_t," "))
    return newtoc



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
###########

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
# 读取文件

pdf_file_input = input("请输入pdf文件目录(输入数字选项 或 完整的文件名带后缀):")
try:
    xuan = int(pdf_file_input)
    pdf_file_input = files[xuan]
    pdf_file_output  = re.sub('.pdf$', '_含目录py.pdf', pdf_file_input, count=0, flags=0)
    pdf_rawtoc_file_output = re.sub('.pdf$', '_自带目录.txt', pdf_file_input, count=0, flags=0)
except:
    pdf_file_output = re.sub('.pdf$', '_含目录py.pdf', pdf_file_input, count=0, flags=0)
    pdf_rawtoc_file_output = re.sub('.pdf$', '_自带目录.txt', pdf_file_input, count=0, flags=0)

pdf_pianyiliang = input("请输入偏移量(正整数, 推荐使用: 当前页码 - 1):")
n = int(pdf_pianyiliang) #偏移量 --  一定要使得页码大于等于1,是第一章的页码 - 1


doc = fitz.open(pdf_file_input)
toctext = doc.get_toc(simple=True) # 原始pdf的目录

# 存储原始文件的目录结构 --- 以缩进为主
file = open(pdf_rawtoc_file_output,'w');
for x in toctext:
    s = '\t'* (int(x[0])-1) + x[1] +" "+ str(x[2]) +'\n'
    file.write(s);
file.close();


## 读取目录txt文件
filetxt = input("读取目录txt文件:")
try:
    xuan = int(filetxt)
    filetxt = files[xuan]
except:
    filetxt = filetxt
newtoc = readtocToNewtoc(filetxt,offset=n, is_rmt = False,is_rmn = True, isrmnum = True, isrmt = False)


doc.setToC(newtoc)
doc.save(pdf_file_output)
print('输出含目录的文件名：' + pdf_file_output)