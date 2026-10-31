import streamlit as st
from streamlit_gsheets import GSheetsConnection



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

open_access_dict = {
    
}
for i in range(len(df)):
    if df.iloc[i]["Open access"] == "Open Access":
        if df.iloc[i]["Topic"] in open_access_dict:
            open_access_dict[df.iloc[i]["Topic"]] = open_access_dict[df.iloc[i]["Topic"]] + 1
        else: 
            open_access_dict[df.iloc[i]["Topic"]] = 1
st.metric("Total rows read", df.shape[0])
st.write(open_access_dict)

st.subheader("Last 5 Rows of Data")
st.dataframe(df.tail())