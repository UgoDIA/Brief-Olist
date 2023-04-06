import pandas as pd

# --------------CUSTOMERS----------------------------------------------------------------------------------------
def customersTable():
    df = pd.read_csv('./datacsv/olist_customers_dataset.csv')

    # Dataframe à merge avec orders
    customerIdMergeDf = df.copy()
    customerIdMergeDf = customerIdMergeDf.iloc[:,[0,1]]

    # Ne garder que les colonnes "customer_unique_id" et "state"
    df = df.iloc[:, [1,4]]

    # Suppression des doublons
    df = df.drop_duplicates(subset=['customer_unique_id'], keep='first')

    return df, customerIdMergeDf

customersDf, customerIdMergeDf = customersTable()
# print(customersDf)
# print(customerIdMergeDf)

# --------------ORDERS-ITEMS-------------------------------------------------------------------------------------
def ordersItemsTAble():
    df = pd.read_csv('./datacsv/olist_order_items_dataset.csv')

    # Dataframe à merge avec orders
    shippingMergeDf = df.copy()
    shippingMergeDf = shippingMergeDf.iloc[:,[0,4]]

    # Suppression des doublons
    df.drop_duplicates(subset=['order_id'], inplace=True, keep='last')

    # Remplissage de la colonne qty
    df.rename(columns={'order_item_id': 'qty'}, inplace=True)

    # Supression des colonnes : seller_id, shipping_limit_date
    df = df.iloc[:, [0,1,2,5,6]]

    return df, shippingMergeDf

ordersItemsDf, shippingMergeDf = ordersItemsTAble()
# print(ordersItemsDf)
# print(shippingMergeDf)

# --------------ORDERS-------------------------------------------------------------------------------------------

def ordersTable():
    df= pd.read_csv('./datacsv/olist_orders_dataset.csv')

    # Customer Id merge=>
    df = pd.merge(df, customerIdMergeDf, how='left', on='customer_id')

    # Shipping_limit_date merge
    df = pd.merge(df, shippingMergeDf, how="left", on='order_id')

    # Supprimer "customer_id" car emplacé par "customer_unique_id"
    df = df.iloc[:,[0,2,3,4,5,6,7,8,9]]

    return df

ordersDf = ordersTable()
# print(ordersDf.info())

# --------------PAYMENTS------------------------------------------------------------------------------------------

def paymentTable():
    df = pd.read_csv('./datacsv/olist_order_payments_dataset.csv')
    return df

paymentDf = paymentTable()

# ------INFO------------------------------------------------------------------------------------
# Valeurs manquantes : certaines timestamp de orders 
# unavailable: 609 ; invoiced: 314 ; processing: 301 ; shipped: 1017; cancel: 625

print("test")



