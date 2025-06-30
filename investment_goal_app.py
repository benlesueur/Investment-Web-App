import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Investment Goal Tracker", layout="wide")

st.title("📈 Investment Goal Tracker")

# Sidebar inputs
st.sidebar.header("Adjustable Inputs")
target_net_worth = st.sidebar.number_input("Target Net Worth (£)", value=1_500_000, step=10000)
years = st.sidebar.slider("Investment Horizon (Years)", 1, 50, 30)
annual_return = st.sidebar.slider("Average Annual Return (%)", 0.0, 15.0, 7.0, 0.1) / 100
starting_monthly = st.sidebar.number_input("Starting Monthly Contribution (£)", value=500, step=50)

# Annual manual inputs
st.subheader("Annual Contribution Planner")
manual_monthlies = []
lump_sums = []

for year in range(1, years + 1):
    cols = st.columns([1, 1])
    with cols[0]:
        monthly = st.number_input(f"Year {year} - Monthly (£)", value=int(starting_monthly + (year - 1) * 50), key=f"m{year}")
    with cols[1]:
        lump = st.number_input(f"Year {year} - Lump Sum (£)", value=0, key=f"l{year}")
    manual_monthlies.append(monthly)
    lump_sums.append(lump)

# Simulation
portfolio_value = 0
portfolio_values = []
total_contributions = []

for year in range(years):
    monthly_contrib = manual_monthlies[year]
    lump_sum = lump_sums[year]
    annual_contrib = monthly_contrib * 12 + lump_sum
    monthly_rate = (1 + annual_return) ** (1/12) - 1

    for _ in range(12):
        portfolio_value = portfolio_value * (1 + monthly_rate) + monthly_contrib
    portfolio_value += lump_sum

    portfolio_values.append(portfolio_value)
    total_contributions.append(monthly_contrib * 12 + lump_sum)

# Display Results
st.subheader("Results")
df = pd.DataFrame({
    "Year": list(range(1, years + 1)),
    "Portfolio Value": portfolio_values,
    "Total Contributions": total_contributions
})

st.dataframe(df.style.format({"Portfolio Value": "£{:,.0f}", "Total Contributions": "£{:,.0f}"}))

# Charts
st.subheader("Visualisations")
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
ax1.plot(df["Year"], df["Portfolio Value"], marker='o', color='green')
ax1.set_title("Portfolio Value Over Time")
ax1.set_ylabel("£")
ax1.grid(True)

ax2.bar(df["Year"], df["Total Contributions"], color='blue')
ax2.set_title("Annual Contributions")
ax2.set_ylabel("£")
ax2.set_xlabel("Year")
ax2.grid(True)

st.pyplot(fig)

# Summary
st.subheader("Summary")
st.metric(label="Final Portfolio Value", value=f"£{portfolio_value:,.0f}")
st.metric(label="Target Net Worth", value=f"£{target_net_worth:,.0f}")
st.metric(label="Progress", value=f"{(portfolio_value / target_net_worth * 100):.1f}%")
