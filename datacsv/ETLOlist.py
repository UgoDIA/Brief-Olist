import pandas as pd 
from runnamegen import generate
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:0000@localhost:5432/testolist')




################### LOCATIONS
###################
# df = pd.read_csv('olist_geolocation_dataset.csv')
# df.drop(['geolocation_zip_code_prefix','geolocation_lat','geolocation_lng','geolocation_city'], inplace=True, axis=1)
# df=df.drop_duplicates(subset=['geolocation_state'],keep="first")
# df.rename(columns = {'geolocation_state':'state'}, inplace = True)
# df.reset_index(inplace=True)
# print(df)



################### SELLERS
###################
# df = pd.read_csv('olist_sellers_dataset.csv')     
# print(df.info( ))
# df['seller_id'] = "'" + df['seller_id'].astype(str) + "'"

####  drop colonnes +random name + rename
# df.drop(['seller_zip_code_prefix','seller_city'], inplace=True, axis=1)
# df['name'] = df.apply(lambda x: generate(), axis=1)
# df.rename(columns = {'seller_id':'id', 'seller_state':'state'}, inplace = True)
# df.to_csv('modified_file.csv', index=False)

##### import csv vers db
# df.to_sql('test2',engine, if_exists='replace',index= False)



# ################## CATEGORIES
# ##################
# df = pd.read_csv('olist_products_dataset.csv')   
# df.rename(columns={'product_category_name':'name'}, inplace = True)
# df.dropna(inplace=True)
# df.drop(["product_id","product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"], inplace=True, axis=1)
# df.reset_index(drop=True,inplace=True)

# # print(df)
# df.to_sql('test3',engine, if_exists='replace',index= True,index_label='id')



################### PRODUCTS
###################
# df = pd.read_csv('olist_products_dataset.csv')


df1=pd.read_csv('olist_products_dataset.csv') #32951      products


df1.dropna(inplace=True)        # --> 32340 
df3=df1.copy()                                         #categories
# df1.info()
df2=pd.read_csv('olist_order_items_dataset.csv') #112650       item order
# df2.info()

df3.reset_index(drop=True,inplace=True)
df3.drop(["product_id","product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"], inplace=True, axis=1)
df3['category_id'] = df3.index
# print(df3)

## Merge des 2 df sur 'product_id' puis 3eme df sur category name
merged_df = pd.merge(df1, df2[['product_id', 'seller_id']], on='product_id', how='left')

# merged_df = pd.merge(merged_df, df3[['category_id', 'product_category_name']], on='product_category_name', how='left')


# merged_df.rename(columns={"product_id":'id',"product_category_name":'name',"product_name_lenght":'name_length',"product_description_lenght":'description_length',"product_photos_qty":"photos_qty"}, inplace = True)
merged_df.drop(["product_weight_g","product_length_cm","product_height_cm","product_width_cm"], inplace=True, axis=1)
merged_df.drop_duplicates(subset=["product_id"],  keep='first',inplace=True)
merged_df.reset_index(inplace=True,drop=True)
merged_df = pd.merge(merged_df, df3[['category_id', 'product_category_name']], on='product_category_name', how='left')
merged_df.drop_duplicates(subset=["product_id"],  keep='first',inplace=True)
merged_df.drop(["product_category_name"], inplace=True, axis=1)
merged_df.rename(columns={"product_id":'id',"product_name_lenght":'name_length',"product_description_lenght":'description_length',"product_photos_qty":"photos_qty"}, inplace = True)




print(merged_df)


# ################### REVIEWS
# ###################

# df = pd.read_csv('olist_order_reviews_dataset.csv')
# df.dropna(subset=['review_id'],inplace=True)
# df.drop_duplicates(subset=['review_id'],keep="first")
# df.rename(columns={"review_id":"id","order_id":"order_id","review_score":'score',"review_comment_title":"comment_title","review_comment_message":"comment_message","review_creation_date":"creation_date","review_answer_timestamp":"answer_timestamp"}, inplace = True)

# df.info()