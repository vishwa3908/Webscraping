import json
import requests
import html5lib
from bs4 import BeautifulSoup
import re
from random import randint
from abc import ABC, abstractmethod
import os
class Extraction(ABC):

    @abstractmethod
    def create_password():
        pass

    @abstractmethod
    def create_connection(self):
        pass
    
    @abstractmethod
    def extract_all_categories(self):
        pass

    @abstractmethod
    def extract_all_book_details(self):
        pass

class Extract_all_books(Extraction):

    def __init__(self):
        self.__password = "samuel186"
        self.create_password()

    def create_password(self):
        rand_lst = [randint(1,126) for _ in range(12)]
        rand_str_list = list(map(chr,rand_lst))
        password = "".join(rand_str_list)
        # print(password)

    def create_connection(self,password):
        if password == self.__password:

            project_url = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_unv_books_1_1318158031_2"
            response = requests.get(project_url)
            while response.status_code!=200:
                response = requests.get(project_url)
            if response.status_code==200:
                return response
        else:
            return False

    def extract_all_categories(self,parsed_doc):
        # title_class = "_cDEzb_card-title_2sYgw" for further use
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


            with open('books_category_records.json','r',encoding='utf8') as f:
                dic = json.load(f)
                if 'Data' not in dic.keys():
                    dic['Data']=[]
                if json_data not in dic['Data']:
                    dic['Data'].append(json_data)
                

            with open('books_category_records.json','w',encoding='utf8') as f:
                json.dump(dic,f)
                f.close()
            with open('books_category.json','w',encoding='utf8') as g:
                json.dump(dic,g)
                f.close()
            count+=1



        return f

    def extract_all_book_details(self,json_file):
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

                    with open('books_category_records.json','r',encoding='utf8') as f:
                        dic = json.load(f)
                        if book_records not in dic['Data'][record]['Books']:
                            dic['Data'][record]['Books'].append(book_records)
                    

                    with open('books_category_records.json','w',encoding='utf8') as f:
                        json.dump(dic,f)
                        f.close()
                
                    


        return json_file

class Extract_all_categories():

    def __init__(self):
        # self.__password = "samuel186"
        # self.create_password()
        pass
    # def create_password(self):
    #     rand_lst = [randint(1,126) for _ in range(12)]
    #     rand_str_list = list(map(chr,rand_lst))
    #     password = "".join(rand_str_list)
    #     print(password)

    def create_connection(self,password):
        if password == 'samuel186':

            self.project_url = "https://www.amazon.in/gp/bestsellers/ref=zg_bs_unv_books_0_1"
            response = requests.get(self.project_url)
            while response.status_code!=200:
                response = requests.get(self.project_url)
            if response.status_code==200:
                return response
        else:
            return False

    def extract_all_amazon_categories(self):
        project_url = self.project_url
        response = requests.get(project_url)
        while response.status_code !=200:
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
            category_json["Category_Number"] = count_category
            category_json["Category"] = categories
            category_json["Category_link"] = final_link
            category_json['Subcategory'] = []
            count_category+=1
            with open('all_categories.json','r',encoding='utf8') as f:
                dic = json.load(f)
                if 'All_categories' not in dic.keys():
                    dic['All_categories']=[]
                if category_json not in dic['All_categories']:
                    dic['All_categories'].append(category_json)
                

            with open('all_categories.json','w',encoding='utf8') as f:
                json.dump(dic,f)
                f.close()
            with open(f'All_Files/{categories}.json','w',encoding='utf8') as f:
                json.dump(category_json,f)
                f.close()

    def extract_all_amazon_subcategories(self):
        # with open('all_categories.json','r',encoding='utf8') as f:
        #     data =json.load(f)
        directory = "All_Files"
        for filename in os.listdir(directory):
            fil = os.path.join(directory, filename)
        # checking if it is a file
            if os.path.isfile(fil):
                with open(fil,'r',encoding='utf8') as f:
                    data =json.load(f)
                    print("Filling Sub categories in  {} File".format(fil))
            url = data['Category_link']
            without_escape_url = url.replace("\\","")
            project_url = without_escape_url.replace('"',"")
            response = requests.get(project_url)
            while response.status_code!=200:
                response = requests.get(project_url)
            if response.status_code ==200:
                page_contents = response.text
                parsed_doc = BeautifulSoup(page_contents,'html.parser')
                clas ="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8"
                ddd = parsed_doc.find_all('div',{'class':clas})
                sub_count = 1
                for i in range(1,len(ddd)):
                    s = str(ddd[i].a)
                    f = s.split("</a>")
                    categories = f[0].split(">")
                    subcategory = categories[-1]
                    c = s
                    z = c.split(">")
                    final_sub_link = '"https://www.amazon.in'+z[0].split('="')[-1]



                    sub_data = {}
                    sub_data['Index'] = sub_count
                    sub_data['Name'] = subcategory
                    sub_data['Link']=final_sub_link
                    sub_data['All_sub_data'] = []
                    sub_data['All_sub_Category'] = []
                    with open(fil,'r',encoding='utf8') as file:
                        dic = json.load(file)
                    
                    if sub_data not in dic['Subcategory']:
                        dic['Subcategory'].append(sub_data)
                    

                    with open(fil,'w',encoding='utf8') as file:
                        json.dump(dic,file)
                        file.close()
                    sub_count+=1

    def pass_sub_cat_url(self):
        directory = "All_Files"
        for filename in os.listdir(directory):
            fil = os.path.join(directory, filename)
        # checking if it is a file
            if os.path.isfile(fil):
                with open(fil,'r',encoding='utf8') as f:
                    data =json.load(f)
                    print("Extracting Sub Sub-Category of {} file".format(fil))
                len_sub_cat = len(data['Subcategory'])
                for index in range(len_sub_cat):
                    url = data['Subcategory'][index]['Link']
                    sub_data = self.extract_all_amazon_sub_sub_category(url)
                    if sub_data not in data['Subcategory'][index]['All_sub_Category']:
                        data['Subcategory'][index]['All_sub_Category']= sub_data
                    with open(fil,'w',encoding='utf8') as f:
                        json.dump(data,f)
                


    def extract_all_amazon_sub_sub_category(self,url):
        
        url =url
        without_escape_url = url.replace("\\","")
        project_url = without_escape_url.replace('"',"")
        response = requests.get(project_url)
        while response.status_code!=200:
            response = requests.get(project_url)
        if response.status_code ==200:
            page_contents = response.text
            parsed_doc = BeautifulSoup(page_contents,'html.parser')
            clas ="_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-large__1z5B8"
            ddd = parsed_doc.find_all('div',{'class':clas})
            sub_count = 1
            final_sub_data = []
            for i in range(1,len(ddd)):
                s = str(ddd[i].a)
                f = s.split("</a>")
                categories = f[0].split(">")
                subcategory = categories[-1]
                c = s
                z = c.split(">")
                final_sub_link = '"https://www.amazon.in'+z[0].split('="')[-1]



                sub_data = {}
                sub_data['Index'] = sub_count
                sub_data['Name'] = subcategory
                sub_data['Link']=final_sub_link
                sub_data['All_sub_records']=[]
                final_sub_data.append(sub_data)
                sub_count+=1
            return final_sub_data


    def extract_all_amazon_subcategories_data(self):
        directory = "All_Files"
        for filename in os.listdir(directory):
            fil = os.path.join(directory, filename)
        # checking if it is a file
            if os.path.isfile(fil):
                with open(fil,'r',encoding='utf8') as f:
                    data =json.load(f)
                len_sub_category = len(data['Subcategory'])
            for dat in range(len_sub_category):
                sub_link = data['Subcategory'][dat]['Link']
                without_escape_url = sub_link.replace("\\","")
                project_url = without_escape_url.replace('"',"")
                self.fill_all_values(fil,dat,project_url)

    def fill_all_values(self,fil,second_index,project_url):
        response = requests.get(project_url)  # requesting at link at record index   
        price = None
        rating = None
        reviews = None
        title=None
        author=None
        while response.status_code !=200:
            response = requests.get(project_url)   # looping till succesfully data is fetched

        if response.status_code==200:  # if data is fetched proceed further then only
            page_contents = response.text

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
                            title = xx
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
                sub_records = {}
            
                sub_records["Number"]=count
                # book_records['Book_link']=""
                sub_records['Title'] = title
                sub_records["image_link"] = image_link
                if "Books" in fil:
                    sub_records["Author"] =author
                # book_records['Author_link']=""
                sub_records['Rating']=rating
                sub_records['Views']=reviews
                sub_records["Price"]=price
                if "Books" in fil:
                    sub_records["Author"] =author
                
                with open(fil,'r',encoding='utf8') as f:
                    data =json.load(f)
                    
                if sub_records not in data['Subcategory'][second_index]['All_sub_data']:
                    data['Subcategory'][second_index]['All_sub_data'].append(sub_records)
        

                with open(fil,'w',encoding='utf8') as file:
                    json.dump(data,file)
                    file.close()

                count+=1 #  increasing to increase the book number

    def fill_other_titles(self):
        directory = "All_Files"
        for filename in os.listdir(directory):
            fil = os.path.join(directory, filename)
            
            if "Books" not in fil:
        # checking if it is a file
                if os.path.isfile(fil):
                    with open(fil,'r',encoding='utf8') as f:
                        data =json.load(f)
                    sub_cat_len = len(data['Subcategory'])
                    
                    for index in range(sub_cat_len):
                        sub_cat_url = data["Subcategory"][index]['Link']
                        without_escape_url = sub_cat_url.replace("\\","")
                        project_url = without_escape_url.replace('"',"")
                        sub_cat_url = project_url
                        len_sub_subcat = len(data['Subcategory'][index]['All_sub_data'])
                        
                        for i in range(len_sub_subcat):
                            response = requests.get(sub_cat_url)
                            while response.status_code !=200:
                                response = requests.get(sub_cat_url)
                            page_contents = response.text
                            parsed_doc = BeautifulSoup(page_contents,'html.parser')
                            clas = "_cDEzb_p13n-sc-css-line-clamp-3_g3dy1"
                            ddd = parsed_doc.find_all('div',{'class':clas})
                           
                            
                            for ix in ddd:
                                t = str(ix)
                                s = t.split("</div>")
                                sd = s[0]
                                title = sd.split(">")[-1]
                                data['Subcategory'][index]['All_sub_data'][i]['Title'] = title
                                i=i+1
                                with open(fil,'w',encoding='utf8') as file:
                                    json.dump(data,file)
                                    file.close()
                                if i==len_sub_subcat:
                                    break
                            
                            break




if __name__ == "__main__":
    obj1 = Extract_all_books()
    password = input("Enter Password => ")
    obj1_response = obj1.create_connection(password)
    empty_data = {}
    print("Creating All Categories Json file")
    with open ('all_categories.json','w',encoding='utf8') as file:
            json.dump(empty_data,file)
    
    obj2 = Extract_all_categories()
    obj2_response = obj2.create_connection(password)
    if obj2_response:
        print("Filling up the All Amazon Categories")
        obj2.extract_all_amazon_categories()
        print("Filled all Amazon Categories")
        print("Filling up the All Amazon Sub-Categories")
        obj2.extract_all_amazon_subcategories()
        print("Filled all Amazon Sub-Categories")
        print("Filling all sub_sub_categories_data")
        obj2.pass_sub_cat_url()
        
        obj2.extract_all_amazon_subcategories_data()
        print("filled done")
        obj2.fill_other_titles()
        print("title filled")


    if obj1_response:
        print(obj1_response.status_code)
        page_contents = obj1_response.text
        parsed_doc = BeautifulSoup(page_contents,'html.parser')
        print("Succesfully Made the Connection")
        print("Creating all Categories of Books")
        
    #-------------cretaing category_records.json file for further process
        with open ('books_category_records.json','w',encoding='utf8') as file:
            json.dump(empty_data,file)
        obj1.extract_all_categories(parsed_doc)
        print("All categories Created")
        print("Putting Books inside all Categories")
        obj1.extract_all_book_details('books_category_records.json')
    else:
        print("Oops Wrong Password")

