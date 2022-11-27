import requests
import html5lib
from bs4 import BeautifulSoup
import json
from create_category import find_book_categories_and_link
from extract_books import extract_all_books
import re

project_url = "https://www.amazon.in/gp/bestsellers/books/ref=zg_bs_unv_books_1_1318158031_2"
response = requests.get(project_url)
print(response.status_code)
page_contents = response.text
empty_data = {}
#-------------cretaing category_records.json file for further process
with open ('category_records.json','w',encoding='utf8') as file:
        json.dump(empty_data,file)


if response.status_code==200:
    with open ('project.html','w',encoding='utf8') as f:
        f.write(page_contents)

    parsed_doc = BeautifulSoup(page_contents,'html.parser')
    print("Succesfully Made the Connection")
    print("Creating all Categories of Books")
    a = find_book_categories_and_link(parsed_doc)
    with open('category_records.json', "r") as fr, open("category.json", "w") as to:
        to.write(fr.read())
    print("Now Putting all book details inside the book categories")
    b = extract_all_books('category_records.json')
    print("All done !! Enjoy")
else:
    print('bad response try again!!')