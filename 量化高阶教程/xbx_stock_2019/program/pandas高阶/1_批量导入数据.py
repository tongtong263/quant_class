"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 本节课程内容
- 如何遍历文件夹
- 批量获取文件名
- 批量读入csv文件
- HDF5文件简介
"""

import pandas as pd
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整

# =====导入浦发银行(sh600000)的历史日线数据
df = pd.read_csv(
    r'C:\Users\Simons\Desktop\xbx_stock_2019\data\basic-trading-data\stock_data\sh600004.csv',
    encoding='gbk',
    skiprows=1, parse_dates=['交易日期']
)

# =====批量导入A股所有股票的历史日线数据
# 系统自带函数os.walk，用于遍历文件夹中的所有文件，os是python自带的系统库
# 演示os.walk

# file location存储我们要读取的数据的文件夹绝对路径
file_location = r'C:\Users\Simons\Desktop\xbx_stock_2019\data\basic-trading-data\stock_data'

# for root, dirs, files in os.walk(file_location):
#     # root输出文件夹，dirs输出root下所有的文件夹，files输出root下的所有的文件
#     print('当前文件夹:', root)
#     print('包含的文件夹:', dirs)
#     print('包含的文件:', files)
#     print()

# 批量读取文件名称
# file_list = []
# for root, dirs, files in os.walk(file_location):
#     for filename in files:
#         if filename.endswith('.csv'):
#             file_path = os.path.join(root, filename)
#             file_path = os.path.abspath(file_path)
#             file_list.append(file_path)

# 遍历文件名，批量导入数据
# all_data = pd.DataFrame()
# for fp in sorted(file_list)[:300]:
#     print(fp)
#
#     # 导入数据
#     df = pd.read_csv(fp, skiprows=1, encoding='gbk')
#     #  合并数据
#     all_data = all_data.append(df, ignore_index=True)  # 注意此时若一下子导入很多文件，可能会内存溢出


# 对数据进行排序
# all_data.sort_values(by=['交易日期', '股票代码'], inplace=True)
# print(all_data)

# 将数据存入hdf文件中
# all_data.to_hdf(
#     r'C:\Users\Simons\Desktop\xbx_stock_2019\data\a_stock.h5',
#     key='all_data',
#     mode='w'
# )

# 从hdf中读取文件
# all_data = pd.read_hdf(
#     r'C:\Users\Simons\Desktop\xbx_stock_2019\data\a_stock.h5',
#     key='all_data')
# print(all_data)
