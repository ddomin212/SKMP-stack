import altair as alt
import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils import get_dataframe

st.set_page_config(page_title="Weather Dashboard", page_icon=":sunny:")
st.title("Weather Dashboard")

st_autorefresh(interval=15 * 1000, key="count")

# Read in the data
df = get_dataframe()
df["CreationTime"] = pd.to_datetime(df["CreationTime"])
units = st.selectbox(
    "Temperature Units", ["Celsius", "Fahrenheit"], key="temp_units"
)
if units == "Fahrenheit":
    df["Temperature"] = df["Temperature"] * 9 / 5 - 459.67
else:
    df["Temperature"] = df["Temperature"] - 273.15
# Streamlit app
st.title("Temperature by City")

# Bar chart
bchart = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("CityName", title=None),
        y=alt.Y("Temperature", title="Temperature"),
        color="CityName",
    )
)
# Bar chart
bchart2 = (
    alt.Chart(df)
    .mark_bar()
    .encode(
        x=alt.X("CityName", title=None),
        y=alt.Y("Humidity", title="Humidity"),
        color="CityName",
    )
)
# Bar chart
lchart = (
    alt.Chart(df)
    .mark_line()
    .encode(
        x="CreationTime",
        y="Temperature",
        color="CityName",
    )
)

c1, c2, c3 = st.columns(3)
with c1:
    st.metric(label="Item Count", value=df["Temperature"].count())
with c2:
    st.metric(label="Max Temperature", value=int(df["Temperature"].max()))
with c3:
    st.metric(label="Min Temperature", value=int(df["Temperature"].min()))
st.altair_chart(bchart, use_container_width=True)
st.altair_chart(lchart, use_container_width=True)
st.altair_chart(bchart2, use_container_width=True)
