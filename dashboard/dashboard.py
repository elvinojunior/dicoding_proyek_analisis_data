import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import date


day_df = pd.read_csv('day_df.csv')
day_df['dteday'] = pd.to_datetime(day_df['dteday'])

st.sidebar.header("Select Date Range")
min_date = date(2011, 1, 1)
max_date = date(2012, 12, 31)
start_date = st.sidebar.date_input("Start Date", min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("End Date", min_value=min_date, max_value=max_date)
filtered_df = day_df[(day_df['dteday'].dt.date >= start_date) & (day_df['dteday'].dt.date <= end_date)]


avg_usage_by_month = filtered_df.groupby('month')[['casual', 'registered']].mean()
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(avg_usage_by_month.index, avg_usage_by_month['casual'], label='Casual Users', marker='o')
ax.plot(avg_usage_by_month.index, avg_usage_by_month['registered'], label='Registered Users', marker='o')
ax.set_title('Average Bike Usage by Month (Casual vs Registered Users)')
ax.set_xlabel('Month')
ax.set_ylabel('Average Number of Users')
ax.set_xticks(range(1, 13))
ax.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax.legend()
ax.grid(True)

avg_usage_by_holiday = filtered_df.groupby('holiday')[['casual', 'registered']].mean().reset_index()
avg_usage_by_holiday['holiday'] = avg_usage_by_holiday['holiday'].map({0: 'Workday', 1: 'Holiday'})
avg_usage_by_holiday_melted = avg_usage_by_holiday.melt(id_vars='holiday', value_vars=['casual', 'registered'], var_name='User  Type', value_name='Average Users')
fig2, ax2 = plt.subplots(figsize=(8, 6))
sns.barplot(x='holiday', y='Average Users', hue='User  Type', data=avg_usage_by_holiday_melted, palette='Set2', ax=ax2)
ax2.set_title('Average Bike Usage on Workdays vs Holidays')
ax2.set_xlabel('Day Type')
ax2.set_ylabel('Average Number of Users')
ax2.grid(True)

st.header("Bike Usage Analysis")
st.pyplot(fig, use_container_width=True)
st.pyplot(fig2, use_container_width=True)

url = "http://elvinojr75-streamlit-app-url"  # Replace with your actual URL

with open("url.txt", "w") as f:
    f.write(url)

st.write("URL has been saved to url.txt")