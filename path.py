
with open('path.txt',encoding='utf-8') as f:
    a = f.readlines()
    itempath = a[0].replace('\n','')
    defaultpath = a[1].replace('\n','')
    datapath = a[2].replace('\n','')
    keyword = a[3].replace('\n','')

print(itempath)
print(defaultpath)
print(datapath)
print(keyword)