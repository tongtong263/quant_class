import pandas as pd
import os

pd.set_option('expand_frame_repr', False)

file_location = r'C:\Users\sgwat\Desktop\quant_class\量化初阶教程\data\basic-trading-data\stock_data'

file_list = []
#get file list
for root,dir,file in os.walk(file_location):
    for file_name in file:
        if file_name.endswith('csv'):
            file_path = os.path.join(root, file_name)
            file_path = os.path.abspath(file_path)
            file_list.append([file_name, file_path])
            print(file_list)

h5_store = pd.HDFStore('hdf_test.h5', mode='w')

# 导入所有csv文件
for file_name, file_path in sorted(file_list):
    stock_code = file_name.split('.')[0]
    df = pd.read_csv(file_path, encoding='gbk',skiprows=1, parse_dates=['交易日期'])
    h5_store[stock_code] = df.iloc[:100]

h5_store.close()
exit()
