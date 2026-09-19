import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT/"online_food_delivery_cleaned.csv", parse_dates=["Order_Date"])

print(f"Rows: {len(df):,} | Columns: {df.shape[1]}")
print("\nTop spending customers")
print(df.groupby("Customer_ID")["Final_Amount"].sum().nlargest(10))

print("\nWeekend vs weekday")
print(df["Order_Day_Type"].value_counts())

print("\nMonthly revenue")
print(df.groupby("Month")["Final_Amount"].sum())

print("\nRevenue by city")
print(df.groupby("City")["Final_Amount"].sum().sort_values(ascending=False))

print("\nRevenue by cuisine")
print(df.groupby("Cuisine_Type")["Final_Amount"].sum().sort_values(ascending=False))

print("\nAverage delivery time by city")
print(df.groupby("City")["Delivery_Time_Min"].mean().sort_values())

print("\nCancellation reasons")
print(df.loc[df["Order_Status"].eq("Cancelled"), "Cancellation_Reason"].value_counts())

print("\nPayment mode preferences")
print(df["Payment_Mode"].value_counts())
