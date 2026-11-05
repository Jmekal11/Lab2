# This creates the page for displaying data visualizations.

import streamlit as st
import pandas as pd
import json
import plotly.express as px
import os

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
JSON_PATH = os.path.join(BASE_DIR, "data.json")
CSV_PATH = os.path.join(BASE_DIR, "data.csv")

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Visuals",
    page_icon="📈",
)

# PAGE TITLE
st.title("Data Visualizations 📈")

def show_metrics(key, values, selection):
    mean_now = values.mean()
    median_now = values.median()
    if key not in st.session_state:
        st.session_state[key] = {
            "selection": selection,
            "mean": mean_now,
            "median": median_now,
            "prev_mean": mean_now,
            "prev_median": median_now,
        }

    s= st.session_state[key]
    if s["selection"] != selection:
        s["prev_mean"], s["prev_median"] = s["mean"], s["median"]
        s["mean"], s["median"], s["selection"] = mean_now, median_now, selection
    col1, col2 = st.columns(2)
    col1.metric("Mean", f"{s['mean']:.2f}", delta=round(s["mean"] - s["prev_mean"], 2))
    col2.metric("Median", f"{s['median']:.1f}", delta=round(s["median"] - s["prev_median"], 1))


# PART 1: GRAPHS FROM data.json
# --- YOUR CODE GOES HERE ---
infile = open(JSON_PATH)
lines = infile.readlines()
infile.close()

data = {}
for line in lines:
    line = line.strip()
    if line == "{" or line == "}":
        continue
    line = line.rstrip(",")
    parts = line.split(": ", 1)
    key = parts[0].strip('"')
    items = parts[1].strip("[]").split(", ")
    cleaned = []
    for item in items:
        if key == "year" or key == "my_rating":
            cleaned.append(int(item))
        else:
            cleaned.append(item.strip('"'))
    data[key] = cleaned

df = pd.DataFrame(data)
st.write(df)

#static chart
st.subheader("My Album Ratings")
st.bar_chart(data=df, x="album", y="my_rating")

#dynamic chart
st.subheader("Rating Share by Album")
if "limit" not in st.session_state:
    st.session_state.limit = 4
st.slider("Number of albums to show", 1, 4, key = "limit")
pie = px.pie(
    names = df["album"][:st.session_state.limit],
    values = df["my_rating"][:st.session_state.limit],
    title = "Share of Total Rating"
)
st.plotly_chart(pie)
shown_ratings = df["my_rating"][:st.session_state.limit]
show_metrics("stats_json", shown_ratings, st.session_state.limit)

# PART 2: GRAPHS FROM data.csv
st.divider()
st.header("Survey Results")
if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0:
    csv_df = pd.read_csv(CSV_PATH)
    csv_df["rating"] = pd.to_numeric(csv_df["rating"], errors="coerce")
    csv_df = csv_df.dropna(subset=["rating"])
    st.subheader("Average Rating by Genre")
    avg_by_genre = csv_df.groupby("genre")["rating"].mean()
    st.bar_chart(avg_by_genre)
    st.subheader("Rating Distribution")
    genre_options = ["All"] + sorted(csv_df["genre"].unique())
    if "genre_choice" not in st.session_state:
        st.session_state.genre_choice = "All"
    st.selectbox("Filter by genre", genre_options, key="genre_choice")
    choice = st.session_state.genre_choice
    if choice == "All":
        filtered = csv_df
    else:
        filtered = csv_df[csv_df["genre"] == choice]
    hist = px.histogram(
        filtered,
        x="rating",
        nbins=10,
        title=f"Distribution of Ratings ({choice})",
        labels={"rating": "Rating"},
    )
    hist.update_layout(yaxis_title="Number of albums")
    st.plotly_chart(hist)
    show_metrics("stats.csv", filtered["rating"], choice)
else:
    st.warning("No survey data yet. Fill out the survey to see these charts.")

