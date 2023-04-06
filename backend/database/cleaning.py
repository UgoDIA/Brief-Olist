import pandas as pd
from runnamegen import generate

from database import engine




# --------------LOCATIONS----------------------------------------------------------------------------------------
def locationsTable():
    df = pd.read_csv('../datacsv/olist_geolocation_dataset.csv')
    df.drop(['geolocation_zip_code_prefix','geolocation_lat','geolocation_lng','geolocation_city'], inplace=True, axis=1)
    df=df.drop_duplicates(subset=['geolocation_state'],keep="first")
    df.rename(columns = {'geolocation_state':'state'}, inplace = True)
    df.reset_index(inplace=True, drop=True)
    # df.to_sql('locations',engine, if_exists='append',index= False)
    return df

locationsDf=locationsTable()


# --------------CATEGORIES----------------------------------------------------------------------------------------
def categoriesTable():
    df = pd.read_csv('../datacsv/olist_products_dataset.csv')   
    df['product_category_name']=df['product_category_name'].fillna('unknown')
    df.drop_duplicates(subset=["product_category_name"],keep='first',inplace=True)
    df.reset_index(inplace=True,drop=True)
    df['id'] = df.index
    df.drop(["product_id","product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"], inplace=True, axis=1)
    df.rename(columns={'product_category_name':'name'}, inplace = True)
    return df

categoriesDf=categoriesTable()


# --------------SELLERS----------------------------------------------------------------------------------------
def sellersTable():
    df = pd.read_csv('../datacsv/olist_sellers_dataset.csv')     
    ###  drop colonnes +random name + rename
    df.drop(['seller_zip_code_prefix','seller_city'], inplace=True, axis=1)
    df['name'] = df.apply(lambda x: generate(), axis=1)
    df.rename(columns = {'seller_id':'id', 'seller_state':'state'}, inplace = True)
    return df

sellersDf=sellersTable()



# --------------PRODUCTS----------------------------------------------------------------------------------------
def productsTable():
    df1=pd.read_csv('../datacsv/olist_products_dataset.csv') #32951  
    # remplis les cat nulls par unknown
    df1['product_category_name']=df1['product_category_name'].fillna('unknown')
    df2=pd.read_csv('../datacsv/olist_order_items_dataset.csv')
    df3=df1.copy() 
    # même traitemet que pour liste catégories
    df3.drop(["product_id","product_name_lenght","product_description_lenght","product_photos_qty","product_weight_g","product_length_cm","product_height_cm","product_width_cm"], inplace=True, axis=1)
    df3.drop_duplicates(subset=["product_category_name"],  keep='first',inplace=True)
    df3.reset_index(inplace=True,drop=True)
    df3['category'] = df3.index
    ## Merge des 2 df sur 'product_id' puis 3eme df sur category name
    merged_df = pd.merge(df1, df2[['product_id', 'seller_id']], on='product_id', how='left')
    merged_df.drop(["product_weight_g","product_length_cm","product_height_cm","product_width_cm"], inplace=True, axis=1)
    merged_df.drop_duplicates(subset=["product_id"],  keep='first',inplace=True)
    merged_df.reset_index(inplace=True,drop=True)
    # 2ème merge
    merged_df = pd.merge(merged_df, df3[['category', 'product_category_name']], on='product_category_name', how='left')
    merged_df.drop_duplicates(subset=["product_id"],  keep='first',inplace=True)
    merged_df.drop(["product_category_name"], inplace=True, axis=1)
    merged_df.rename(columns={"product_id":'id',"seller_id":"seller","product_name_lenght":'name_length',"product_description_lenght":'description_length',"product_photos_qty":"photos_qty"}, inplace = True)
    return merged_df

productsDf=productsTable()



# --------------CUSTOMERS----------------------------------------------------------------------------------------
def customersTable():
    df = pd.read_csv('../datacsv/olist_customers_dataset.csv')

    # Dataframe à merge avec orders
    customerIdMergeDf = df.copy()
    customerIdMergeDf = customerIdMergeDf.iloc[:,[0,1]]

    # Ne garder que les colonnes "customer_unique_id" et "state"
    df = df.iloc[:, [1,4]]

    # Suppression des doublons
    df = df.drop_duplicates(subset=['customer_unique_id'], keep='first')
    df.rename(columns={"customer_unique_id":'id',"customer_state":"state"},inplace = True)
    return df, customerIdMergeDf

customersDf, customerIdMergeDf = customersTable()
# print(customersDf)
# print(customerIdMergeDf)



# --------------ORDERS-ITEMS-------------------------------------------------------------------------------------
def ordersItemsTAble():
    df = pd.read_csv('../datacsv/olist_order_items_dataset.csv')

    # Dataframe à merge avec orders
    shippingMergeDf = df.copy()
    shippingMergeDf = shippingMergeDf.iloc[:,[0,4]]

    # Suppression des doublons
    df.drop_duplicates(subset=['order_id'], inplace=True, keep='last')

    # Remplissage de la colonne qty
    df.rename(columns={'order_item_id': 'qty'}, inplace=True)

    # Supression des colonnes : seller_id, shipping_limit_date
    df = df.iloc[:, [0,1,2,5,6]]
    df.rename(columns={"order_id":'order',"product_id":"product","freight_value":"freight"},inplace = True)

    return df, shippingMergeDf

ordersItemsDf, shippingMergeDf = ordersItemsTAble()
# print(ordersItemsDf)
# print(shippingMergeDf)

# --------------ORDERS-------------------------------------------------------------------------------------------

def ordersTable():
    df= pd.read_csv('../datacsv/olist_orders_dataset.csv')

    # Customer Id merge=>
    df = pd.merge(df, customerIdMergeDf, how='left', on='customer_id')

    # Shipping_limit_date merge
    df = pd.merge(df, shippingMergeDf, how="left", on='order_id')

    # Supprimer "customer_id" car emplacé par "customer_unique_id"
    df = df.iloc[:,[0,2,3,4,5,6,7,8,9]]
    df.rename(columns={"order_id":'id',"order_status":"status","order_purchase_timestamp":"purchase_timestamps","order_approved_at":"approved_at","order_delivered_carrier_date":"delivered_carrier_date","order_delivered_customer_date":"delivered_customer_date","order_estimated_delivery_date":"estimated_delivery_date","customer_unique_id":"customer"},inplace = True)
    df.drop_duplicates(subset=['id'],inplace=True)

    return df

ordersDf = ordersTable()
# print(ordersDf.info())

# --------------PAYMENTS------------------------------------------------------------------------------------------

def paymentTable():
    df = pd.read_csv('../datacsv/olist_order_payments_dataset.csv')
    df.rename(columns={"order_id":'order',"payment_sequential":"sequential","payment_type":"type","payment_installments":"installments"},inplace = True)

    return df

paymentDf = paymentTable()
# print(paymentDf)

# ------INFO------------------------------------------------------------------------------------
# Valeurs manquantes : certaines timestamp de orders 
# unavailable: 609 ; invoiced: 314 ; processing: 301 ; shipped: 1017; cancel: 625




#--------------------REVIEWS------------------------------------------------------------------------------------------
def reviewsTable():
    df = pd.read_csv('../datacsv/olist_order_reviews_dataset.csv')
    df.dropna(subset=['review_id'],inplace=True)
    df.drop_duplicates(subset=['review_id'],inplace=True,keep="first")
    df.rename(columns={"review_id":"id","order_id":"order","review_score":'score',"review_comment_title":"comment_title","review_comment_message":"comment_message","review_creation_date":"creation_date","review_answer_timestamp":"answer_timestamp"}, inplace = True)
    return df

reviewsDf=reviewsTable()
# print(reviewsDf.info())


###### Import vers BDD

locationsDf.to_sql('locations',engine, if_exists='append',index= False)
print("import locations terminé")
categoriesDf.to_sql('categories',engine, if_exists='append',index= False)
print("import categories terminé")
sellersDf.to_sql('sellers',engine, if_exists='append',index= False)
print("import sellers terminé")
customersDf.to_sql('customers',engine, if_exists='append',index= False)
print("import customers terminé")
productsDf.to_sql('products',engine, if_exists='append',index= False)
print("import products terminé")
ordersDf.to_sql('orders',engine, if_exists='append',index= False)
print("import orders terminé")
ordersItemsDf.to_sql('order_items',engine, if_exists='append',index= False)
print("import order_items terminé")
reviewsDf.to_sql('reviews',engine, if_exists='append',index= False)
print("import reviews terminé")
paymentDf.to_sql('payments',engine, if_exists='append',index= False)
print("import payments terminé")
print("import total terminé")
