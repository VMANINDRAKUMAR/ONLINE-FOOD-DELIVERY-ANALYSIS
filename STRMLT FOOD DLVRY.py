import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Online Food Delivery Analysis", page_icon="🍔", layout="wide")
ROOT = Path(__file__).resolve().parent

@st.cache_data
def load_data():
    return pd.read_csv(ROOT/"online_food_delivery_cleaned.csv", parse_dates=["Order_Date"])

df = load_data()
st.title("🍔 Online Food Delivery Analysis")
st.caption("Data-Driven Business Insights | Python + SQL + Streamlit")

st.sidebar.header("Filters")
cities = st.sidebar.multiselect("City", sorted(df.City.unique()), default=sorted(df.City.unique()))
cuisines = st.sidebar.multiselect("Cuisine", sorted(df.Cuisine_Type.unique()), default=sorted(df.Cuisine_Type.unique()))
statuses = st.sidebar.multiselect("Order Status", sorted(df.Order_Status.unique()), default=sorted(df.Order_Status.unique()))

date_min, date_max = df.Order_Date.min().date(), df.Order_Date.max().date()
dates = st.sidebar.date_input("Date range", (date_min, date_max), min_value=date_min, max_value=date_max)

f = df[df.City.isin(cities) & df.Cuisine_Type.isin(cuisines) &
       df.Order_Status.isin(statuses) &
       df.Order_Date.dt.date.between(dates[0], dates[-1])].copy()

cancel_rate = f.Order_Status.eq("Cancelled").mean()*100 if len(f) else 0

a,b,c,d = st.columns(4)
a.metric("Total Orders", f"{len(f):,}")
b.metric("Total Revenue", f"₹{f.Final_Amount.sum():,.0f}")
c.metric("Average Order Value", f"₹{f.Final_Amount.mean():,.0f}")
d.metric("Average Delivery Time", f"{f.Delivery_Time_Min.mean():.1f} min")

a,b,c = st.columns(3)
a.metric("Cancellation Rate", f"{cancel_rate:.2f}%")
b.metric("Average Delivery Rating", f"{f.Delivery_Rating.mean():.2f}/5")
c.metric("Profit Margin", f"{f.Profit_Margin.mean()*100:.2f}%")

st.divider()
left,right = st.columns(2)

with left:
    st.subheader("Monthly Revenue Trend")
    monthly = f.groupby(f.Order_Date.dt.to_period("M").astype(str)).Final_Amount.sum()
    st.line_chart(monthly)

with right:
    st.subheader("Orders by City")
    st.bar_chart(f.City.value_counts())

left,right = st.columns(2)
with left:
    st.subheader("Cuisine Revenue")
    st.bar_chart(f.groupby("Cuisine_Type").Final_Amount.sum().sort_values(ascending=False))
with right:
    st.subheader("Average Delivery Time by City")
    st.bar_chart(f.groupby("City").Delivery_Time_Min.mean().sort_values())

st.subheader("Cancellation Reasons")
st.bar_chart(f.loc[f.Order_Status.eq("Cancelled"), "Cancellation_Reason"].value_counts())

st.subheader("Top 10 Restaurants by Revenue")
top = f.groupby("Restaurant_Name").agg(
    Orders=("Order_ID","count"),
    Revenue=("Final_Amount","sum"),
    Avg_Rating=("Restaurant_Rating","mean"),
    Avg_Delivery=("Delivery_Time_Min","mean")
).sort_values("Revenue", ascending=False).head(10)
st.dataframe(top.round(2), use_container_width=True)

st.download_button("Download filtered data", f.to_csv(index=False).encode(),
                   "online_food_delivery_filtered.csv", "text/csv")
