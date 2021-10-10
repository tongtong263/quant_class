"""
《邢不行-2019新版|Python股票量化投资课程》
author: 邢不行/西蒙斯
微信: xingbuxing0807

# 本节课程内容
- HDF5文件介绍
- 如何存储、读取HDF5
"""

import pandas as pd
import os

pd.set_option('expand_frame_repr', False)  # 当列太多时显示完整


# =====将数据存入hdf文件
# 批量读取文件名称
# file_list = []
# # 存储csv文件的文件夹路径
# file_location = r'C:\Users\Simons\Desktop\xbx_stock_2019\data\basic-trading-data\stock_data'
#
# for root, dirs, files in os.walk(file_location):
#     for filename in files:
#         if filename.endswith('.csv'):
#             file_path = os.path.join(root, filename)
#             file_path = os.path.abspath(file_path)
#             file_list.append([filename, file_path])
#
# # 创建hdf文件
# h5_store = pd.HDFStore('a_stock_100.h5', mode='w')
#
# # 批量导入并且存储数据
# for filename, file_path in sorted(file_list)[:300]:
#     stock_code = filename.split('.')[0]
#     print(stock_code, filename, file_path)
#     df = pd.read_csv(file_path, encoding='gbk', skiprows=1, parse_dates=['交易日期'])
#
#     # 存储数据到hdf
#     h5_store[stock_code] = df.iloc[:100]
#
# # 关闭hdf文件
# h5_store.close()
# exit()

# =====读取hdf数据
# 创建hdf文件
# h5_store = pd.HDFStore('a_stock_100.h5', mode='r')

# h5_store中的key
# print(h5_store.keys())

# 读取某个key指向的数据
# print(h5_store.get('sh600000'))
# print(h5_store['sh600000'])

# 关闭hdf文件
# h5_store.close()
