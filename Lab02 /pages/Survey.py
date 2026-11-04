# This creates the page for users to input data.
# The collected data should be appended to the 'data.csv' file.

import streamlit as st
import pandas as pd
import os # The 'os' module is used for file system operations (e.g. checking if a file exists).
import csv

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Survey",
    page_icon="📝",
)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data.csv")

# PAGE TITLE AND USER DIRECTIONS
st.title("Data Collection Survey 📝")
st.write("Please fill out the form below to add your data to the dataset.")

# DATA INPUT FORM
# 'st.form' creates a container that groups input widgets.
# The form is submitted only when the user clicks the 'st.form_submit_button'.
# This is useful for preventing the app from re-running every time a widget is changed.
with st.form("survey_form"):
    # Create text input widgets for the user to enter data.
    # The first argument is the label that appears above the input box.
    album_input = st.text_input("What's an album you love?")
    genre_input = st.selectbox(
        "What genre is it?",
        ["Pop", "Rock", "Hip-Hop", "R&B", "Country", "Electronic", "Indie", "Other"],
        )
    rating_input = st.slider("How would you rate it?", 1, 10, 5)
    submitted = st.form_submit_button("Submit Data")

    # The submit button for the form.

    # This block of code runs ONLY when the submit button is clicked.
    if submitted:
        if album_input.strip():
            needs_header = not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0
            with open(CSV_PATH, "a", newline="") as f:
                writer = csv.writer(f)
                if needs_header:
                    writer.writerow(["album", "genre", "rating"])
                writer.writerow([album_input.strip(), genre_input, rating_input])
            st.success("Your data has been submitted!")
            st.write(f"You entered: **Album:** {album_input}, **Genre:** {genre_input}, **Rating:** {rating_input}")
        else:
            st.warning("Please enter an album name.")
        # --- YOUR LOGIC GOES HERE ---
        # TO DO:
        # 1. Create a new row of data from 'category_input' and 'value_input'.
        # 2. Append this new row to the 'data.csv' file.
        #    - You can use pandas or Python's built-in 'csv' module.
        #    - Make sure to open the file in 'append' mode ('a').
        #    - Don't forget to add a newline character '\n' at the end.

# DATA DISPLAY
# This section shows the current contents of the CSV file, which helps in debugging.
st.divider() # Adds a horizontal line for visual separation.
st.header("Current Data in CSV")

# Check if the CSV file exists and is not empty before trying to read it.
if os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0:
    # Read the CSV file into a pandas DataFrame.
    current_data_df = pd.read_csv(CSV_PATH)
    # Display the DataFrame as a table.
    st.dataframe(
        current_data_df,
        use_container_width=True,
        column_config={
            "album": st.column_config.TextColumn("Album", width="large"),
            }
        )
else:
    st.warning("The 'data.csv' file is empty or does not exist yet.")
