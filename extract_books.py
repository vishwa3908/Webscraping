#-------------Importing Libraries----------------------------
import requests
import html5lib
from bs4 import BeautifulSoup
import json
import re

#---------------------------------------------------------------

#--------------------Function to extract all book details---------------
def extract_all_books(json_file):
    f= open(json_file)
    category_records_json = json.load(f)  # loading existing json file containing all categories
    

    for record in range(len(category_records_json['Data'])):  # looping over all categories

        cat = category_records_json['Data'][record]['Category']  # fetching specifice categoriy at record index
        link = category_records_json['Data'][record]['Link']   # fetching category link

        project_url = link
        response = requests.get(project_url)  # requesting at link at record index   
        
        while response.status_code !=200:
            response = requests.get(project_url)   # looping till succesfully data is fetched

        if response.status_code==200:  # if data is fetched proceed further then only
            page_contents = response.text

            with open ('books.html','w',encoding='utf8') as f:
                f.write(page_contents)  # writing page contents in html format

            parsed_doc = BeautifulSoup(page_contents,'html.parser')

            cc = "p13n-sc-uncoverable-faceout"   # class that contain all details of books
            dd = parsed_doc.find_all('div',{'class':cc})

            count=1   # variable to keep track of number of books

            for index in range(len(dd)):   # to iterate over all data present in the class cc
               
    # -------------------finding ratings of the book -----------------------
                d = str(dd[index])
                h = d.split("><")

                for k in h:
                    if "out of 5 stars" in k and 'span' in k:
                        q = k.split(">")[1].replace("</span","")
                        rating = q

            
            

    #------------------------------------------------------------
    # ------------------------finding cost of the book-------------------------------

                cost_str = str(dd[index])
                qq = cost_str.split(">")

                for p in qq:
                    if "₹" in p:
                        zz = p.replace("</span","")
                        zz = zz.replace("₹","Rs ")
                        price = zz

                

    #-----------------------------------------------------------------------------------------------

    #--------------------------------finding number of reviews-----------------

                review_str = str(dd[index])
                qw = review_str.split("</span>")

                for we in qw:
                    if 'class="a-size-small"' in we:
                        reviews = we.split(">")[-1]

    #-----------------finding author and book title-------------------------------

                gf = review_str.split("</div>")

                for find_title in gf:
                    if 'class="_cDEzb_p13n-sc-css-line-clamp-2_EWgCb"' in find_title:   # handling some exception class of book title
                        title = find_title.split(">")[-1]
                        
                    elif 'class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"' in find_title:  # finding author
                        df = find_title.split('class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"')
                        author = df[-1].replace(">","")

                ggf = str(gf)
                # ggf = ggf.split('class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"')
                ff = ggf.split("<span><div ")
                
                for x in ff:
                    if 'class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"' in x and 'class="_cDEzb_p13n-sc-css-line-clamp-2_EWgCb"' not in x:  # finding book title
                        y = x.split("</span")
                        z=y[0].split('class="_cDEzb_p13n-sc-css-line-clamp-1_1Fn1y"')
                        if len(z)==2:
                            xx=z[1].replace("', '","")
                            xx = xx.replace(">","")
                        else:
                            xx = z
                        
                        title = xx

#----------------------finding book image link-------------------------------------------
# ---------------------image  is of 900X600 size-------------------

                image_process_str = str(dd[index].a)
                image_process = image_process_str.split("</a>")

                for r in image_process:
                    if "[900,600]" in r:
                        f = r.split("[600,400]")
                        image_link = f[1].split(":[900,600]")[0].replace(",","")
                        image_link = image_link[:-1]

#-----------------appending all details inside a dictionary-----------------------------
                book_records = {}
              
                book_records["Number"]=count
                book_records['Book_name'] = title
                # book_records['Book_link']=""
                book_records["Book_image_link"] = image_link
                book_records["Author"] = author
                # book_records['Author_link']=""
                book_records['Rating']=rating
                book_records['Views']=reviews
                book_records["Price"]=price


                count+=1 #  increasing to increase the book number
                
#------------------saving all details inside the category_records.json file-----------------------------------

                with open('category_records.json','r',encoding='utf8') as f:
                    dic = json.load(f)
                    if book_records not in dic['Data'][record]['Books']:
                        dic['Data'][record]['Books'].append(book_records)
                

                with open('category_records.json','w',encoding='utf8') as f:
                    json.dump(dic,f)
                    f.close()
            
                


    return json_file