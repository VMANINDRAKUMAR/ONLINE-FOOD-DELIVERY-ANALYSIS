import pandas as pd
import numpy as np
from pathlib import Path


import os

print(os.path.exists("C:/Users/V MANINDRA KUMAR/Desktop/ONLINE FOOD DELIVERY/ONINE_FOOD_DELIVERY_ANALYSIS.csv"))

food_del = pd.read_csv("C:/Users/V MANINDRA KUMAR/Desktop/ONLINE FOOD DELIVERY/ONINE_FOOD_DELIVERY_ANALYSIS.csv")

df = pd.DataFrame(food_del)

df.info()

print(df.isnull().sum())

for c in df.select_dtypes(include="object").columns:
    df[c] = df[c].astype("string").str.strip().replace({"": pd.NA, "nan": pd.NA, "None": pd.NA})

df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", format="mixed")

num = ["Customer_Age","Delivery_Time_Min","Distance_km","Order_Value",
       "Discount_Applied","Final_Amount","Delivery_Rating","Restaurant_Rating","Profit_Margin"]
for c in num:
    df[c] = pd.to_numeric(df[c], errors="coerce")

df["Customer_Age"] = df["Customer_Age"].clip(18,60)
df["Delivery_Time_Min"] = df["Delivery_Time_Min"].clip(0,300)
df["Distance_km"] = df["Distance_km"].clip(0,40)
df["Order_Value"] = df["Order_Value"].clip(0,5000)
df["Discount_Applied"] = df["Discount_Applied"].clip(0,300)
df["Delivery_Rating"] = df["Delivery_Rating"].clip(1,5)
df["Restaurant_Rating"] = df["Restaurant_Rating"].clip(1,5)
df["Profit_Margin"] = df["Profit_Margin"].clip(0,0.50)

for c in ["Customer_Gender","City","Area","Cuisine_Type","Payment_Mode"]:
    mode = df[c].mode(dropna=True)
    df[c] = df[c].fillna(mode.iloc[0] if len(mode) else "Unknown")

for c in ["Customer_Age","Delivery_Time_Min","Distance_km","Order_Value","Discount_Applied","Delivery_Rating"]:
    df[c] = df[c].fillna(df[c].median())

df["Discount_Applied"] = np.minimum(df["Discount_Applied"], df["Order_Value"])
df["Final_Amount"] = df["Final_Amount"].fillna(df["Order_Value"] - df["Discount_Applied"])
df["Final_Amount"] = df["Final_Amount"].clip(lower=0)
df["Final_Amount"] = np.minimum(df["Final_Amount"], df["Order_Value"])

df.loc[df["Order_Status"].eq("Delivered"), "Cancellation_Reason"] = "Not Applicable"
df.loc[df["Order_Status"].eq("Cancelled") & df["Cancellation_Reason"].isna(), "Cancellation_Reason"] = "Unknown"

peak = df["Peak_Hour"].astype("string").str.lower().str.strip()
df["Peak_Hour"] = peak.map({"true":True,"false":False,"1":True,"0":False,"yes":True,"no":False}).fillna(False)

df["Order_Hour"] = pd.to_datetime(df["Order_Time"], format="%H:%M", errors="coerce").dt.hour.fillna(0).astype(int)
df["Order_Day_Type"] = np.where(df["Order_Date"].dt.dayofweek >= 5, "Weekend", "Weekday")
df["Age_Group"] = pd.cut(df["Customer_Age"], [17,25,35,45,55,60],
                         labels=["18-25","26-35","36-45","46-55","56-60"], include_lowest=True).astype(str)
df["Profit_Amount"] = df["Final_Amount"] * df["Profit_Margin"]
df["Delivery_Performance"] = pd.cut(df["Delivery_Time_Min"], [-1,30,60,120,180,300],
                                    labels=["Excellent","Good","Average","Slow","Very Slow"]).astype(str)
df["Discount_Pct"] = np.where(df["Order_Value"]>0, df["Discount_Applied"]/df["Order_Value"]*100, 0).round(2)
df["Month"] = df["Order_Date"].dt.to_period("M").astype(str)


