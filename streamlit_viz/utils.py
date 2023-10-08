import os
import streamlit as st
import mysql.connector
import pandas as pd
from dotenv import load_dotenv
import altair as alt
import pandas as pd

load_dotenv()

def select_temperature(temperatures: pd.DataFrame) -> None:
    """Get temperature units from user and convert temperature accordingly
    
    Args:
        temperatures (pd.DataFrame): Dataframe with temperature data
    """
    units = st.selectbox(
        "Temperature Units", ["Celsius", "Fahrenheit"], key="temp_units"
    )
    if units == "Fahrenheit":
        temperatures["ConvertedTemperature"] = temperatures["Temperature"] * 9 / 5 - 459.67
    else:
        temperatures["ConvertedTemperature"] = temperatures["Temperature"] - 273.15


def sql_to_dataframe() -> pd.DataFrame:
    """Get data from a MySQL database and return a dataframe
    
    Returns:
        pd.DataFrame: Dataframe with data from MySQL database
    """
    conn = mysql.connector.connect(
        host="host.docker.internal",
        port=os.getenv("MYSQL_PORT"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database="weather",
    )
    cursor = conn.cursor()

    query = "SELECT * FROM data"
    cursor.execute(query)
    rows = cursor.fetchall()
    column_names = [desc[0] for desc in cursor.description]

    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=column_names)
    df["CreationTime"] = pd.to_datetime(df["CreationTime"])

    return df

def get_charts(temperatures: pd.DataFrame) -> tuple[alt.Chart, alt.Chart, alt.Chart]:
    """Create altair charts

    Args:
        temperatures (pd.DataFrame): Dataframe with temperature data
    """
    temp_bar = (
        alt.Chart(temperatures)
        .mark_bar()
        .encode(
            x=alt.X("CityName", title=None),
            y=alt.Y("median(ConvertedTemperature)", title="Temperature"),
            color=alt.Color("median(Temperature)").scale(scheme="goldorange"),
        )
    )
    humid_bar = (
        alt.Chart(temperatures)
        .mark_bar()
        .encode(
            x=alt.X("CityName", title=None),
            y=alt.Y("median(Humidity)", title="Humidity"),
            color=alt.Color("median(Humidity)").scale(scheme="greenblue"),
        )
    )
    temp_line = (
        alt.Chart(temperatures)
        .mark_line()
        .encode(
            x=alt.X("CreationTime", title="Timeline"),
            y="ConvertedTemperature",
            color="CityName",
        )
    )
    return temp_bar, humid_bar, temp_line

def render_metrics(temperatures: pd.DataFrame) -> None:
    """Render metrics

    Args:
        temperatures (pd.DataFrame): Dataframe with temperature data
    """
    c1, c2, c3 = st.columns(3)
    with c1:
        st.metric(label="Item Count", value=temperatures["ConvertedTemperature"].count())
    with c2:
        st.metric(label="Max Temperature", value=int(temperatures["ConvertedTemperature"].max()))
    with c3:
        st.metric(label="Min Temperature", value=int(temperatures["ConvertedTemperature"].min()))