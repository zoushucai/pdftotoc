#  使用说明

首先建议安装conda环境（以下全部在conda环境中实现）

### 环境准备:

- 前提要准备一个目录的txt,(建议配合 pdf-toc 来用,主要是用于提取pdf的书签目录):
    - pdf-toc: https://github.com/HareInWeed/pdf-toc
- python3环境  + 并且要安装 `fitz` ,它属于pymupdf包, 
    - 安装: `pip3 install pymupdf `
    - 在使用时,可能会遇到 `AttributeError("module 'fitz' has no attribute 'open'") `,
        - 参考: https://github.com/pymupdf/PyMuPDF/issues/660

### 环境的快速搭建

```python
# 环境的快读搭建
conda create -n mypdftoc python=3.9 
# 然后进入环境,再输入安装软件包命令
conda activate mypdftoc
pip3 install  -i https://pypi.mirrors.ustc.edu.cn/simple -U pandas
pip3 install  -i https://pypi.mirrors.ustc.edu.cn/simple -U pymupdf
## 如果不使用 jupyterlab 则不需要安装
# pip3 install -i https://pypi.mirrors.ustc.edu.cn/simple -U jupyterlab==3
```

### 使用: 

```python
# 前提是进入虚拟环境: 
# conda activate mypdftoc 

# 在命令行终端,输入如下命令, 
python3 pdfsettoc.py
```



### 目录文件格式:  

- 缩进有无都行,按照标题前面的数字和小数点 以及 缩进`\t` 个个数 来判断层级, 选最大的那个
- 空格不要随便打, 按照空格分割
- 可以设置偏移量: 如果偏移量是20, 则第21页算第一页,即第三列为1 ,  第20页为-1, 第19页为-2, …., 第一页为-20

```
......
.......
第2章 双变量回归分析：一些基本思想 35
	2.1 一个假设的例子  35
	2.2 总体回归函数的概念 38
	2.3 “线性”一词的含义 39
	2.4 PRF的随机设定 41
	2.5 随机干扰项的意义 42
	2.6 样本回归函数 43
	2.7 说明性例子 46
	要点与结论 48
	习题 49
第3章 双变量回归分析：估计问题  56
	3.1 普通最小二乘法 56
	3.2 经典线性回归模型:最小二乘法的基本假定 62
	3.3 最小二乘估计的精度或标准误 70
	3.4 最小二乘估计量的性质:高斯-马尔可夫定理 73
	3.5 判定系数2: “拟合优度”的一个度量 75
	3.6 一个数值例子 81
	3.7 说明性例子 83
	3.8 关于蒙特卡罗实验的一一个注记 86
	要点与结论 87
	习题 88
	附录3A  94
......
.......
```

###  返回文件

- 原有pdf的目录文件
- 带目录的pdf文件

### 实例:

![image-20211114234709819](https://i0.hdslb.com/bfs/album/81aa639a607c2e5d355f8418d4fa89e3087d5aa4.png)


![image-20211114234745294](https://i0.hdslb.com/bfs/album/401ae60e6350228d93e44caff0223cd12233026e.png)

![image-20211114234729881](https://i0.hdslb.com/bfs/album/2e99333487e944baa7e074d6770b145ed9458881.png)

