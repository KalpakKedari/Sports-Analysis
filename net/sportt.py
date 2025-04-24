import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Page Configuration
st.set_page_config(layout="wide")

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    .stApp {
        background-color: black;
        color: white;
    }
    [data-testid="stSidebar"] {
        background-color: #1e1e1e;
    }
    .css-1cpxqw2, .st-bx {
        background-color: #333 !important;
        color: white !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏆 Sports Performance Analysis Dashboard")

# Load Data Directly
file_path = "sport_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(file_path)

df = load_data()

st.write("### Data Preview")
st.dataframe(df.head())

# Convert date columns
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

palette_colors = ['red', 'blue', 'orange', 'green', 'purple', 'magenta', 'cyan']

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Score Distribution")
    if 'score' in df.columns:
        fig, ax = plt.subplots()
        sns.histplot(df['score'].dropna(), bins=20, kde=True, color=palette_colors[0], ax=ax)
        ax.set_xlabel("Score")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)
    else:
        st.warning("No 'score' column found.")

with col2:
    st.subheader("📅 Performance Over Time")
    if 'date' in df.columns and 'score' in df.columns:
        fig, ax = plt.subplots()
        sns.lineplot(x=df['date'], y=df['score'], marker='o', color=palette_colors[1], ax=ax)
        ax.set_xlabel("Date")
        ax.set_ylabel("Score")
        st.pyplot(fig)
    else:
        st.warning("Ensure columns 'date' and 'score' exist.")

col3, col4 = st.columns(2)

with col3:
    st.subheader("🏅 Top 10 Players")
    if 'player' in df.columns and 'goals' in df.columns:
        top_players = df.groupby('player')['goals'].sum().nlargest(10)
        fig, ax = plt.subplots()
        sns.barplot(y=top_players.index, x=top_players.values, palette=palette_colors, ax=ax)
        ax.set_xlabel("Total Goals")
        st.pyplot(fig)
    else:
        st.warning("Ensure 'player' and 'goals' columns exist.")

with col4:
    st.subheader("⚽ Team Performance")
    if 'team' in df.columns and 'score' in df.columns:
        team_performance = df.groupby('team')['score'].mean()
        fig, ax = plt.subplots()
        sns.barplot(x=team_performance.index, y=team_performance.values, palette=palette_colors, ax=ax)
        ax.set_xlabel("Teams")
        ax.set_ylabel("Total Goals Scored")
        plt.xticks(rotation=45)
        st.pyplot(fig)
    else:
        st.warning("Ensure 'team' and 'score' columns exist.")

# Dropdown for selecting a team
st.title("Team Players Performance Analysis")
teams = df['team'].unique()
selected_team = st.selectbox("Select a Team", teams)

# Filter data for selected team
team_df = df[df['team'] == selected_team]

# Bar chart for scores
fig1 = px.bar(team_df, x='player', y='score', title=f"Scores of {selected_team} Players", color='player')
st.plotly_chart(fig1)

# Bar chart for goals
fig2 = px.bar(team_df, x='player', y='goals', title=f"Goals of {selected_team} Players", color='player')
st.plotly_chart(fig2)

st.write("This analysis helps visualize the performance of players in the selected team.")
