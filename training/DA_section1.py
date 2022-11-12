# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 16:54:40 2022

@author: Micro
"""

import numpy as np
import pandas as pd
customer_master = pd.read_csv("customer_master.csv")
#print(customer_master.head())
#custom = np.array(customer_master)
#print(custom.shape)

item_master = pd.read_csv("item_master.csv")
#print(item_master.head())

transaction_1 = pd.read_csv("transaction_1.csv")
#print(transaction_1.head())

transaction_detail_1 = pd.read_csv("transaction_detail_1.csv")
#print(transaction_detail_1.head())

transaction_2 = pd.read_csv("transaction_2.csv")
transaction = pd.concat([transaction_1, transaction_2], ignore_index=True)
#print(transaction.head())

transaction_detail_2 = pd.read_csv("transaction_detail_2.csv")
transaction_detail = pd.concat([transaction_detail_1, transaction_detail_2], ignore_index=True)

#print(len(transaction_1))
#print(len(transaction_2))
#print(len(transaction))

join_data = pd.merge(transaction_detail, transaction[["transaction_id", "payment_date", "customer_id"]], on="transaction_id", how="left")
#print(join_data.head())

join_data = pd.merge(join_data, customer_master, on="customer_id", how="left")
join_data = pd.merge(join_data, item_master, on="item_id", how="left")
#print(join_data.head())

join_data["price"] = join_data["quantity"] * join_data["item_price"]
#print(join_data[["quantity", "item_price", "price"]].head()) 

#print(join_data["price"].sum())
#print(transaction["price"].sum())
#print(join_data["price"].sum()==transaction["price"].sum())

#print(join_data.isnull().sum())
#print(join_data.describe())

#print(join_data["payment_date"].min())
#print(join_data["payment_date"].max())

#print(join_data.dtypes)

join_data["payment_date"] = pd.to_datetime(join_data["payment_date"])
join_data["payment_month"] = join_data["payment_date"].dt.strftime("%Y%m")
#print(join_data[["payment_date", "payment_month"]].head())
#print(join_data.groupby("payment_month").sum()["price"])

#print(join_data.groupby(["payment_month","item_name"]).sum()[["price", "quantity"]])

#print(pd.pivot_table(join_data, index="item_name", columns="payment_month", values=["price", "quantity"], aggfunc="sum"))

graph_data = pd.pivot_table(join_data, index="payment_month", columns="item_name", values="price", aggfunc="sum")
#print(graph_data.head())

import matplotlib.pyplot as plt
#%matplotlib inline
plt.plot(list(graph_data.index), graph_data["PC-A"], label="PC-A", color="red")
plt.plot(list(graph_data.index), graph_data["PC-B"], label="PC-B", color="blue")
plt.plot(list(graph_data.index), graph_data["PC-C"], label="PC-C", color="green")
plt.plot(list(graph_data.index), graph_data["PC-D"], label="PC-D", color="yellow")
plt.plot(list(graph_data.index), graph_data["PC-E"], label="PC-E", color="pink")
plt.legend()
plt.show()