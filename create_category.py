import json
from bs4 import BeautifulSoup


def find_book_categories_and_link(parsed_doc):
# find title
    title_class = "_cDEzb_card-title_2sYgw"
    page_title = parsed_doc.find_all('div',{'class':title_class})

    all_titles_class = "_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8"
    all_titles = parsed_doc.find_all('div',{'class':all_titles_class})
    all_tiltes_anchor_tags = []
    all_titles_records = []
    for item in all_titles:
        topics = item.find_all('a')
        all_tiltes_anchor_tags.append(topics)
    all_tiltes_anchor_tags.pop(0)
    count = 1
    for data in all_tiltes_anchor_tags:
        link_string = str(data[0])
        x = link_string.replace('&amp;',"&")
        # for title name
        y = x.split('>')
        z = y[1]

        #for link
        a = x.split('"')
        a = a[1]
        full_link = "https://www.amazon.in/"+a

        final_name = z.replace('</a',"")
        final_link = full_link
        final_value = [final_name,final_link]
        json_data = {}
        json_data['Category_number']=count
        json_data['Category']=final_name
        json_data['Link'] = final_link
        json_data["Books"]=[]
        all_titles_records.append(final_value)


        with open('category_records.json','r',encoding='utf8') as f:
            dic = json.load(f)
            if 'Data' not in dic.keys():
                dic['Data']=[]
            if json_data not in dic['Data']:
                dic['Data'].append(json_data)
            

        with open('category_records.json','w',encoding='utf8') as f:
            json.dump(dic,f)
            f.close()
        with open('category.json','w',encoding='utf8') as g:
            json.dump(dic,g)
            f.close()
        count+=1



    return f