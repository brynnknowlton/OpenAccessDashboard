import streamlit as st
from streamlit import connections
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import numpy as np


st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# .streamlit/secrets.toml
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

df = conn.read()

# Print results.
for row in df.itertuples():
    st.write(f"{row.Title} has a :{row.Author}:")