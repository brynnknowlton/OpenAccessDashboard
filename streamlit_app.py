import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd



st.title("Open Access Dashboard of CSUSB Authors")

st.write(
   "Reviewing the open access status of CSUSB authors, this dashboard provides insights into the number of publications and their accessibility. The data is sourced from OpenAlex, which tracks the open access status of various publications by CSUSB authors."
)

conn = st.connection(
    "gsheets",
    type=GSheetsConnection
)


@st.cache_data(ttl=3600)
def load_data():
    return conn.read(
        spreadsheet="https://docs.google.com/spreadsheets/d/1sy7PdahgXAdMpimSvbH-Qb2A3c47ERnuRqxYauW9M4s/edit",
        worksheet="1488710283"
    )

df = load_data()

# Initialize dictionaries to store open access, non-open access, and total counts per topic, as well as a percent open access dictionary
open_access_dict = {} 
not_oa_dict = {}
total_dict = {}
percent_open_access_dict = {"Topic": [], "Percent Open Access": []}
 
# Iterate through the dataframe to populate the dictionaries with open access, non-open access, and total counts per topic
for i in range(len(df)):
    if df.iloc[i]["Topic"] in total_dict:
        total_dict[df.iloc[i]["Topic"]] = total_dict[df.iloc[i]["Topic"]] + 1
    else:
        total_dict[df.iloc[i]["Topic"]] = 1
    if df.iloc[i]["Open access"] == "Open Access":
        if df.iloc[i]["Topic"] in open_access_dict:
            open_access_dict[df.iloc[i]["Topic"]] = open_access_dict[df.iloc[i]["Topic"]] + 1
        else: 
            open_access_dict[df.iloc[i]["Topic"]] = 1.0
    else:
        if df.iloc[i]["Topic"] in not_oa_dict:
            not_oa_dict[df.iloc[i]["Topic"]] = not_oa_dict[df.iloc[i]["Topic"]] + 1
        else:
            not_oa_dict[df.iloc[i]["Topic"]] = 1.0

# Calculate the percent open access for each topic based on the populated dictionariese
for topic in total_dict:
    if topic in open_access_dict:
        percent_open_access_dict["Topic"].append(topic)
        percent_open_access_dict["Percent Open Access"].append(round(float((open_access_dict[topic] / total_dict[topic]) * 100.0), 2))
    else:
        percent_open_access_dict["Topic"].append(topic)
        percent_open_access_dict["Percent Open Access"].append(0.0)


# Allow the user to select topics from the available list of topics
selected_topics = st.multiselect("Select Topics", options=list(total_dict.keys()))
st.subheader("Percent Open Access Topics")
# Create the filtered dictionary
selected_data = {
    topic: float(percent_open_access_dict["Percent Open Access"][percent_open_access_dict["Topic"].index(topic)])
    for topic in selected_topics
}

# Display each one as a crisp metric component
if selected_topics:
    # Optional: Display them side-by-side using columns
    cols = st.columns(len(selected_topics))
    for col, (topic, val) in zip(cols, selected_data.items()):
        col.write(label=topic, value=f"{val:.2f}%")



# Display a line chart of the percent open access for the selected topics
st.subheader("Line Chart from Dictionary")
st.bar_chart(pd.DataFrame({
    "Topic": [topic for topic in selected_topics],
    "Percent Open Access": [percent_open_access_dict["Percent Open Access"][percent_open_access_dict["Topic"].index(topic)] for topic in selected_topics]
}), x="Topic", y="Percent Open Access")

