import re
import pandas as pd
customer = pd.read_csv("customer_join.csv")
uselog_months = pd.read_csv("use_log_months.csv")
year_months = list(uselog_months["年月"].unique())
uselog = pd.DataFrame()
for i in range(1,len(year_months)):
    tmp = uselog_months.loc[uselog_months["年月"]==year_months[i]]
    tmp.rename(columns={"count":"count_0"},inplace=True)
    tmp_before = uselog_months.loc[uselog_months["年月"]==year_months[i-1]]
    del tmp_before["年月"]
    tmp_before.rename(columns={"count":"count_1"},inplace=True)
    tmp = pd.merge(tmp, tmp_before, on="customer_id", how="left")
    uselog = pd.concat([uselog,tmp], ignore_index=True)
#print(uselog.head()) 
from dateutil.relativedelta import relativedelta
exit_customer = customer.loc[customer["is_deleted"]==1]
exit_customer["exit_date"] = None
exit_customer["end_date"] = pd.to_datetime(exit_customer["end_date"])
for i in range(len(exit_customer)):
    exit_customer["exit_date"].iloc[i] = exit_customer["end_date"].iloc[i] - relativedelta(months=1)
exit_customer["exit_date"] = pd.to_datetime(exit_customer["exit_date"])
exit_customer["年月"] = exit_customer["exit_date"].dt.strftime("%Y%m")
uselog["年月"] = uselog["年月"].astype(str)
exit_uselog = pd.merge(uselog, exit_customer, on=["customer_id", "年月"], how="left")
#print(len(uselog))
exit_uselog = exit_uselog.dropna(subset=["name"])
#print(len(exit_uselog))
#print(len(exit_uselog["customer_id"].unique()))
conti_customer = customer.loc[customer["is_deleted"]==0]
conti_uselog = pd.merge(uselog, conti_customer, on=["customer_id"], how="left")
conti_uselog = conti_uselog.dropna(subset=["name"])
#データをシャッフルして重複削除
conti_uselog = conti_uselog.sample(frac=1).reset_index(drop=True)
conti_uselog = conti_uselog.drop_duplicates(subset="customer_id")
#print(len(conti_uselog))
predict_data = pd.concat([conti_uselog, exit_uselog], ignore_index=True)
#print(len(predict_data))
predict_data["period"] = 0
predict_data["now_date"] = pd.to_datetime(predict_data["年月"],format="%Y%m")
predict_data["start_date"] = pd.to_datetime(predict_data["start_date"])
for i in range(len(predict_data)):
    delta = relativedelta(predict_data["now_date"][i], predict_data["start_date"][i])
    predict_data["period"][i] = int(delta.years*12 + delta.months)
#print(predict_data.isna().sum())
#print(predict_data.isnull().sum())
predict_data = predict_data.dropna(subset=["count_1"])
#print(predict_data.isna().sum())
target_col = ["campaign_name", "class_name", "gender", "count_1", "routine_flg", "period", "is_deleted"]
predict_data = predict_data[target_col]
predict_data = pd.get_dummies(predict_data) #ダミー変数生成
#print(predict_data.head())
del predict_data["campaign_name_通常"]
del predict_data["class_name_ナイト"]
del predict_data["gender_M"]
#print(predict_data.head())

from sklearn.tree import DecisionTreeClassifier
import sklearn.model_selection

exit = predict_data.loc[predict_data["is_deleted"]==1]
conti = predict_data.loc[predict_data["is_deleted"]==0].sample(len(exit)) 

X = pd.concat([exit, conti], ignore_index=True)
y = X["is_deleted"]
del X["is_deleted"]
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X,y)

model = DecisionTreeClassifier(random_state=0)
model.fit(X_train,y_train)
y_test_pred = model.predict(X_test)
#print(y_test_pred)
results_test = pd.DataFrame({"y_test":y_test, "y_pred":y_test_pred})
#print(results_test.head())
correct = len(results_test.loc[results_test["y_test"]==results_test["y_pred"]])
data_count = len(results_test)
score_test = correct / data_count
#print(score_test)
#print(model.score(X_test, y_test))
#print(model.score(X_train, y_train))
X = pd.concat([exit, conti], ignore_index=True)
y = X["is_deleted"]
del X["is_deleted"]
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X,y)

model = DecisionTreeClassifier(random_state=0, max_depth=4)
model.fit(X_train, y_train)
#print(model.score(X_test, y_test))
#print(model.score(X_train, y_train))

importance = pd.DataFrame({"feature_names":X.columns, "coefficient":model.feature_importances_ })
#print(importance)

count_1 = 3
routine_flg = 1
period = 30
campaign_name = "入会費無料"
class_name = "オールタイム"
gender = "M"

if campaign_name == "入会費半額":
    campaign_name_list = [1, 0]
elif campaign_name == "入会費無料":
    campaign_name_list = [0, 1]
elif campaign_name == "通常":
    campaign_name_list = [0, 0]
if class_name == "オールタイム":
    class_name_list = [1, 0]
elif class_name == "デイタイム":
    class_name_list = [0, 1]
elif class_name == "ナイト":
    class_name_list = [0, 0]
if gender == "F":
    gender_list = [1]
elif gender == "M":
    gender_list = [0]
input_data = [count_1, routine_flg, period]
input_data.extend(campaign_name_list)
input_data.extend(class_name_list)
input_data.extend(gender_list)
#print(model.predict([input_data]))
#print(model.predict_proba([input_data]))    