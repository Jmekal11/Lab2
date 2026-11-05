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

# PART 2: GRAPHS FROM data.csv
# --- YOUR CODE GOES HERE ---
