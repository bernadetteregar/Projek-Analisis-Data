import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency


st.header('Bike Rentals Dashboard')

days_df = pd.read_csv('days_df.csv')
daily_rentals = pd.read_csv('daily_rentals.csv')
monthly_data = pd.read_csv('monthly_data.csv')
years_sum = pd.read_csv('years_sum.csv')
yearly_counts = pd.read_csv('yearly_counts.csv')
season_sum = pd.read_csv('season_sum.csv')
season_contribution = pd.read_csv('season_contribution.csv')

daily_rentals['dteday'] = pd.to_datetime(days_df['dteday'])
daily_rentals.sort_values(by='dteday', inplace=True)
daily_rentals.reset_index(drop=True, inplace=True)

min_date = daily_rentals["dteday"].min()
max_date = daily_rentals["dteday"].max()

# membuat sidebar untuk filter
with st.sidebar:
    start_date, end_date = st.date_input(
        label='Pick Date',
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = daily_rentals[(daily_rentals["dteday"] >= pd.to_datetime(start_date)) & 
                         (daily_rentals["dteday"] <= pd.to_datetime(end_date))]


st.subheader(f'Daily Rentals ({start_date} to {end_date})')

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(main_df["dteday"], main_df["cnt"], marker='o', color="#FF7043", linestyle='-', linewidth=2)

ax.set_title("Daily Bike Rentals in Selected Date Range")
ax.set_xlabel("Date")
ax.set_ylabel("Rental Count")
ax.grid(True)  
ax.tick_params(axis='x', rotation=45)  

st.pyplot(fig)
col1, col2 = st.columns(2)

with col1:
    # Menghitung total pesanan (rental_count) dari main_df
    total_orders = main_df["cnt"].sum()  
    st.metric("Total Rentals", value=total_orders)


# Grafik 1
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(main_df["dteday"], main_df["cnt"], marker='o', color="#FF7043", linestyle='-', linewidth=2)

ax.set_title("Daily Bike Rentals in Selected Date Range")
ax.set_xlabel("Date")
ax.set_ylabel("Rental Count")
ax.grid(True)  


# Grafik 2
st.subheader("Monthly Bike Rental Trends (2011 vs 2012)")
month_names = ["Jan", "Feb", "March", "April", "May", "June",
               "July", "Aug", "Sept", "Oct", "Nov", "Dec"]

fig, ax = plt.subplots(figsize=(10, 6))

for yr in days_df['yr'].unique():
    monthly_data = days_df[days_df['yr'] == yr].groupby('mnth')['cnt'].sum()
    ax.plot(monthly_data.index, monthly_data.values, marker='o', label=f'Year {yr + 2011}')

ax.set_xticks(range(1, 13))  
ax.set_xticklabels(month_names)  

# label and title
ax.set_title("Monthly Bike Rental Trends (2011 vs 2012)")
ax.set_xlabel("Month")
ax.set_ylabel("Total Rentals")
ax.legend()

plt.grid()
st.pyplot(fig)

# Grafik 3
st.subheader("Percentage Contribution of Bycycle Rentals by Season (2012)")

# menghitung total penyewaan di tahun 2012
total_2012 = days_df[days_df['yr'] == 1]['cnt'].sum()

season_contribution_2012 = days_df[days_df['yr'] == 1].groupby("season").agg({"cnt": "sum"})

# menghitung persentase kontribusi per season
season_contribution_2012['percentage'] = (season_contribution_2012['cnt'] / total_2012) * 100

# dictionary untuk mengubah season number menjadi nama musim
season_labels = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
season_contribution_2012['season_name'] = season_contribution_2012.index.map(season_labels)

fig, ax = plt.subplots(figsize=(8, 6))  # Mengatur ukuran figure
labels = season_contribution_2012['season_name'] 
explode = [0.1 if i == season_contribution_2012['percentage'].idxmax() else 0 for i in season_contribution_2012.index]

# Membuat pie chart
ax.pie(
    season_contribution_2012['percentage'],  
    labels=labels, 
    autopct='%1.1f%%',  
    explode=explode,  
    startangle=140, 
    colors=['#ff9999','#66b3ff','#99ff99','#ffcc99']  
)
ax.set_title("Percentage Contribution of Bike Rentals by Season in 2012")
st.pyplot(fig)


# Grafik 4 
st.subheader("Total Bike Rentals by Weather Condition")

weather_group = days_df.groupby('weathersit').agg({'cnt': 'sum'}).reset_index()
weather_labels = {1: 'Clear', 2: 'Cloudy/Mist', 3: 'Snow/Rain'}
weather_group['weathersit'] = weather_group['weathersit'].map(weather_labels)

# Membuat bar chart
plt.figure(figsize=(10, 6))
sns.barplot(x='weathersit', y='cnt', data=weather_group, dodge=False)

plt.title("Total Bike Rentals by Weather Conditions")
plt.xlabel("Weather Condition")
plt.ylabel("Total of Rentals")

for index, value in enumerate(weather_group['cnt']):
    plt.text(index, value + 1000, str(value), ha='center', va='bottom', fontsize=12)

plt.ylim(10000, weather_group['cnt'].max() + 50000)  
plt.yticks(range(10000, int(weather_group['cnt'].max()) + 200000, 200000))  

st.pyplot(plt)
plt.clf()

