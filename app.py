import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IPL Analytics Dashboard", page_icon="🏏", layout="wide")

st.title("🏏 IPL Analytics Dashboard (2008–2020)")
st.markdown("Interactive analysis of IPL matches, teams, and players")

# Load data
@st.cache_data
def load_data():
    matches = pd.read_csv("matches.csv")
    deliveries = pd.read_csv("deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# Sidebar
st.sidebar.header("Filters")
seasons = sorted(matches["season"].unique())
selected_season = st.sidebar.selectbox("Select Season", ["All"] + list(seasons))

if selected_season != "All":
    matches = matches[matches["season"] == selected_season]

# KPI Cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Matches", len(matches))
col2.metric("Total Seasons", matches["season"].nunique())
col3.metric("Total Teams", matches["team1"].nunique())
col4.metric("Venues", matches["venue"].nunique())

st.markdown("---")

# Most Successful Teams
st.subheader("🏆 Most Successful Teams (by Wins)")
wins = matches["winner"].value_counts().reset_index()
wins.columns = ["Team", "Wins"]
fig1 = px.bar(wins.head(10), x="Team", y="Wins", color="Wins",
              color_continuous_scale="sunset", title="Top 10 Teams by Wins")
st.plotly_chart(fig1, use_container_width=True)

# Toss Decision Analysis
st.subheader("🪙 Toss Decision Analysis")
col1, col2 = st.columns(2)
toss = matches["toss_decision"].value_counts().reset_index()
toss.columns = ["Decision", "Count"]
fig2 = px.pie(toss, names="Decision", values="Count", title="Bat vs Field after Toss")
col1.plotly_chart(fig2, use_container_width=True)

toss_winner = matches[matches["toss_winner"] == matches["winner"]].shape[0]
toss_loser = len(matches) - toss_winner
fig3 = px.pie(names=["Toss Winner Won", "Toss Winner Lost"],
              values=[toss_winner, toss_loser],
              title="Does Winning Toss Help?")
col2.plotly_chart(fig3, use_container_width=True)

# Matches per Season
st.subheader("📅 Matches Per Season")
per_season = matches.groupby("season").size().reset_index(name="Matches")
fig4 = px.line(per_season, x="season", y="Matches", markers=True,
               title="Number of Matches Each Season")
st.plotly_chart(fig4, use_container_width=True)

# Top Venues
st.subheader("🏟️ Top Venues by Matches Hosted")
venues = matches["venue"].value_counts().reset_index().head(10)
venues.columns = ["Venue", "Matches"]
fig5 = px.bar(venues, x="Matches", y="Venue", orientation="h",
              color="Matches", color_continuous_scale="teal")
st.plotly_chart(fig5, use_container_width=True)

# Top Run Scorers
st.subheader("🏏 Top 10 Run Scorers (All Time)")
runs = deliveries.groupby("batter")["batsman_runs"].sum().reset_index()
runs.columns = ["Batter", "Total Runs"]
runs = runs.sort_values("Total Runs", ascending=False).head(10)
fig6 = px.bar(runs, x="Batter", y="Total Runs", color="Total Runs",
              color_continuous_scale="reds", title="Top 10 Run Scorers")
st.plotly_chart(fig6, use_container_width=True)

# Top Wicket Takers
st.subheader("🎯 Top 10 Wicket Takers")
wickets = deliveries[deliveries["dismissal_kind"].notna()]
wickets = wickets[~wickets["dismissal_kind"].isin(["run out", "retired hurt", "obstructing the field"])]
wickets = wickets.groupby("bowler").size().reset_index(name="Wickets")
wickets = wickets.sort_values("Wickets", ascending=False).head(10)
fig7 = px.bar(wickets, x="Bowler" if "Bowler" in wickets.columns else "bowler",
              y="Wickets", color="Wickets", color_continuous_scale="blues")
fig7.update_xaxes(title="Bowler")
st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.caption("Data Source: Kaggle IPL Complete Dataset 2008-2020 | Built with Streamlit & Plotly")