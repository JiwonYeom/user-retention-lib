import pandas as pd
from datetime import datetime, timedelta
from collections import OrderedDict
import numpy as np

# import data
df = pd.read_csv('user-list.csv')

# add monthly column
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d %H:%M')
df['date_month'] = df['date'].dt.strftime('%Y-%m')
df['userId'] = df.userId.apply(str)
monthList = df.date_month.unique()
userList = []
for month in monthList:
    if(len(userList) == 0):
        userList.append(list(df.userId.where(df['date_month'] == month).unique()))
    else:
        toAppend = set(df.userId.where(df['date_month'] == month).unique())
        # remove all the previous months' users
        toRemove = set().union(*userList)
        userList.append(list(toAppend - toRemove))
# userList will now contain lists of first users from each month.
userObj = {}
count = 0
for month in monthList:
    userObj[month] = userList[count]
    count+=1

userList = {}  # change userList from array to dictionary
for month in monthList:
    userList[month] = df.userId.where(df['date_month'] == month).unique()  # << unique user of each month

def match_all(rangeArr, subRangeArr):
    arr = {}
    for month in rangeArr:
        arr[month] = []
        for sub_month in subRangeArr:  
            # figure out if each month unique user existed in the first charger user group
            arr[month].append(np.isin(userList[sub_month],userObj[month]).sum())
    return arr

dates = ["2017-03-01", "2018-05-30"]
start, end = [datetime.strptime(_, "%Y-%m-%d") for _ in dates]
result = list(OrderedDict(((start + timedelta(_)).strftime(r"%Y-%m"), None) for _ in range((end - start).days)).keys())
real_result = match_all(result, result) # use same time range for both compare-ref and compare-ee

df2 = df.groupby('date_month')[['userId']].nunique()
for month, month_list in real_result.items():
    df2[month] = month_list

print(df2)
#writer = pd.ExcelWriter('pollet_ok3.xlsx', engine='xlsxwriter')
#df2.to_excel(writer, sheet_name='Sheet1')
#writer.save()
