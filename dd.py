import json
from bs4 import BeautifulSoup

import requests
project_url = 'https://www.amazon.in/gp/bestsellers/books/1318158031/ref=zg_bs_nav_books_1'
response = requests.get(project_url)
page_contents = response.text
parsed_doc = BeautifulSoup(page_contents,'html.parser')
clas ='_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL'
ddd = parsed_doc.find_all('div',{'class':clas})
count_category = 1
for i in ddd:
    s = str(i.a)
    d = s
    f = s.split("</a>")
    
    z = d.split(">")
    final_link = '"https://www.amazon.in'+z[0].split('="')[1]
    
    categories = f[0].split(">")[1]
    category_json = {}
    category_json["Number"] = count_category
    category_json["Category"] = categories
    category_json["Category_link"] = final_link
    category_json['Subcategory'] = []
    count_category+=1
    print(category_json)