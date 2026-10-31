import streamlit as st
from streamlit import connections
from streamlit_gsheets import GSheetsConnection



st.title("🎈 My new app")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
# .streamlit/secrets.toml
# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)

@st.cache_data(ttl=3600)  # one hour

df = conn.read()
st.dataframe(df)

print(f'Total rows read: {len(df)}')
st.metric(label="Total rows read", value=df.shape[0])
st.subheader("Last 5 Rows of Data")
st.dataframe(df.tail())