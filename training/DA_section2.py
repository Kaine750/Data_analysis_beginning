# -*- coding: utf-8 -*-
"""
Created on Sat Mar 12 21:10:07 2022

@author: Micro
"""


import pandas as pd
uriage_data = pd.read_csv("uriage.csv")
#print(uriage_data.head())

kokyaku_data = pd.read_excel("kokyaku_daicho.xlsx")
#print(kokyaku_data.head())

#print(uriage_data["item_name"].head())
#print(uriage_data["item_price"].head())

uriage_data["purchase_date"] = pd.to_datetime(uriage_data["purchase_date"])
uriage_data["purchase_month"] = uriage_data["purchase_date"].dt.strftime("%Y%m")
res = uriage_data.pivot_table(index="purchase_month", columns="item_name", aggfunc="size", fill_value=0)
res = uriage_data.pivot_table(index="purchase_month", columns="item_name", values="item_price", aggfunc="sum", fill_value=0)
#print(res)

#print(len(pd.unique(uriage_data.item_name)))

uriage_data["item_name"] = uriage_data["item_name"].str.upper()
uriage_data["item_name"] = uriage_data["item_name"].str.replace(" ", "")
uriage_data["item_name"] = uriage_data["item_name"].str.replace("  ", "")
#print(uriage_data)
uriage_data.sort_values(by=["item_name"], ascending=True)
#print(pd.unique(uriage_data["item_name"]))
#print(len(pd.unique(uriage_data["item_name"])))
#print(uriage_data.isnull().any(axis=0))

#欠損値の補完
print(type(uriage_data))
flg_is_null = uriage_data["item_price"].isnull()
for trg in list(uriage_data.loc[flg_is_null, "item_name"].unique()):
    price = uriage_data.loc[(~flg_is_null) & (uriage_data["item_name"] == trg), "item_price"].max()
    uriage_data["item_price"].loc[(flg_is_null) & (uriage_data["item_name"] == trg)] = price

#print(uriage_data.head())
#print(uriage_data.isnull().any(axis=0))
    
#for trg in list(uriage_data["item_name"].sort_values().unique()):
    #print(trg + "の最大額：" + str(uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].max()) 
         # + "の最少額：" + str(uriage_data.loc[uriage_data["item_name"]==trg]["item_price"].min(skipna=False)))
    
kokyaku_data["顧客名"].head()
#print(uriage_data["customer_name"].head())

kokyaku_data["顧客名"] = kokyaku_data["顧客名"].str.replace(" ", "")
kokyaku_data["顧客名"] = kokyaku_data["顧客名"].str.replace("  ", "")

flg_is_serial = kokyaku_data["登録日"].astype("str").str.isdigit()
flg_is_serial.sum()

fromSerial = pd.to_timedelta(kokyaku_data.loc[flg_is_serial, "登録日"].astype("float"), unit="D") + pd.to_datetime("1900/01/01")
#print(fromSerial)

fromString = pd.to_datetime(kokyaku_data.loc[~flg_is_serial, "登録日"])
#print(fromString)

kokyaku_data["登録日"] = pd.concat([fromSerial, fromString])
#print(kokyaku_data)

kokyaku_data["登録年月"] = kokyaku_data["登録日"].dt.strftime("%Y%m")
rslt = kokyaku_data.groupby("登録年月").count()["顧客名"]
#print(rslt)
#print(len(kokyaku_data))

flg_is_serial = kokyaku_data["登録日"].astype("str").str.isdigit()
#print(flg_is_serial.sum())
join_data = pd.merge(uriage_data, kokyaku_data, left_on="customer_name", right_on="顧客名", how="left")
join_data = join_data.drop("customer_name", axis=1)
#print(join_data)

dump_data = join_data[["purchase_date", "purchase_month", "item_name", "item_price", "顧客名"
                       , "かな", "地域", "メールアドレス", "登録日"]]
#print(dump_data)
dump_data.to_csv("dump_data.csv", index=False)















