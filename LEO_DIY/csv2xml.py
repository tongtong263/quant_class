import pandas as pd

pd.set_option('expand_frame_repr', False)

file_path = r'C:\Users\sgwat\Desktop\quant_class\LEO_DIY\data\homework4.csv'

df = pd.read_csv(file_path,
                 skiprows=1,
                 encoding='gbk'
                 )

# 将title生成xml的tag
def get_xml_template():
    template = ''
    for i in df.columns:
        xml_element = '<%s></%s>' % (i, i)
        template += xml_element + '\n'
    template = '<CSFA>' + '\n' + template + '</CSFA>'
    return template


df = get_xml_template()
print(df)
exit()


print(df.iloc[1:3,:])