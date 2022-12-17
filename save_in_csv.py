import pandas as pd
import os

directory  = 'All_Files'
for filename in os.listdir(directory):
            fil = os.path.join(directory, filename)
            if os.path.isfile(fil) and 'json' in fil.split(".")[-1]:
                df = pd.read_json(fil)
                df = df.replace("&amp;","and",regex=True)
                sub_len = len(df)
                for i in range(1,sub_len+1):
                    category_number = df.iloc[i-1,0]
                    category_name = df.iloc[i-1,1]
                    category_link = df.iloc[i-1,2]
                    subcategory_name = df.iloc[i-1,3]['Name']
                    sub_cat_link = df.iloc[i-1,3]['Link']
                    sub_index = df.iloc[i-1,3]['Index']
                    len_all_sub_data = len(df.iloc[i-1,3]['All_sub_data'])
                    Title = []
                    image_link = []
                    Rating = []
                    Views = []
                    Price = []
                    Number = []
                    Data = []
                    for j in range(1,len_all_sub_data+1):
                        Number=df.iloc[i-1,3]['All_sub_data'][j-1]['Number']
                        Title=df.iloc[i-1,3]['All_sub_data'][j-1]['Title']
                        image_link=df.iloc[i-1,3]['All_sub_data'][j-1]['image_link']
                        Rating=df.iloc[i-1,3]['All_sub_data'][j-1]['Rating']
                        Views=df.iloc[i-1,3]['All_sub_data'][j-1]['Views']
                        Price = df.iloc[i-1,3]['All_sub_data'][j-1]['Price']
                        data = [category_number,category_name,category_link,sub_index,subcategory_name,sub_cat_link,Number,Title,image_link,Rating,Views,Price]
                        Data.append(data)
                    df_1 = pd.DataFrame(Data,columns=['Category_number','Category_name','Category_link','Sub_category_number','Sub_categoy_name','Sub_category_link','Index','Title','Image_link','Rating','Views','Price'])
                    df_1 = df_1.replace("&amp;","and",regex=True)
                    filename = category_name
                    df_1.to_csv(f'All_csv_files/{filename}.csv',index=False)
            