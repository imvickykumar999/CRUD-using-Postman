
from bs4 import BeautifulSoup
import xml.etree.ElementTree as obj
import random, string

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

with open('task 2 XSLT initial.xml', 'r') as f:
    data = f.read()

bs_data = BeautifulSoup(data, 'xml')
print('\n----> task 2 XSLT initial.xml\n')
print(bs_data.prettify())
root = obj.Element("header")

for tag in bs_data.find_all('cd'):
    m1 = obj.Element("cd")
    root.append (m1)

    b1 = obj.SubElement(m1, "username")
    b1.text = tag.username.text

    b2 = obj.SubElement(m1, "password")
    b2.text = get_random_string(8)
    tree = obj.ElementTree(root)

fileName = 'task 2 XSLT final.xml'
with open (fileName, "wb") as files :
    tree.write(files)

with open('task 2 XSLT final.xml', 'r') as f:
    data = f.read()

bs_data = BeautifulSoup(data, 'xml')
print()
print('\n----> task 2 XSLT final.xml\n')
print(bs_data.prettify())
