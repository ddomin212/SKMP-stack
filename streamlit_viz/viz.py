import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from utils import sql_to_dataframe, select_temperature, get_charts, render_metrics

st.set_page_config(page_title="Weather Dashboard", page_icon=":sunny:")
st.title("Weather Dashboard")

st_autorefresh(interval=15 * 1000, key="count")

temperatures = sql_to_dataframe()
select_temperature(temperatures)

temp_bar, humid_bar, temp_line = get_charts(temperatures)

render_metrics(temperatures)

st.altair_chart(temp_bar, use_container_width=True)
st.altair_chart(humid_bar, use_container_width=True)
st.altair_chart(temp_line, use_container_width=True)
