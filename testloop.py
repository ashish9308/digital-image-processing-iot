a =['ashish', 'alok']



list1 =['kumar','kumar1','kumar2']
list2= ['sinha','tiwari']


print(type(list1))


for x in a:
    for c in list1:
        for i in range(3):
            print(x,c)
    for c2 in list2:
        for j in range(3):
            print(x,c2)
            
            
            
import pandas as pd

df = pd.read_excel('Financial_Sample.xlsx') # can also index sheet by name or fetch all sheets
mylist = df['Country'].tolist()
print(type(mylist))


import xml.etree.ElementTree as ET

tree = ET.parse('test.xml')
for node in tree.getiterator():
    if node.attrib.get('Name', 0) == 'Recipient Name':
        node.attrib['Value'] = 'Ashish'
root = tree.getroot()
#ET.register_namespace("", "XY")
#print(ET.tostring(root))
tree.write('output.xml')