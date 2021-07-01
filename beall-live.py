#!/usr/bin/env python
# coding: utf-8
import streamlit as st
import pandas as pd
import datetime
from pathlib import Path
import altair as alt

# Main
st.set_page_config(page_title="Beall Live", page_icon=":bulb:")

# hiding the hamburger menu and footer
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.markdown("## :bulb: Beall Live")
st.markdown("---")

st.write(
    "This application provides weekly updates on how much of the [Beall's list](https://beallslist.net/) of predatory scholarly open‑access publishers is alive."
)

# Sidebar
st.sidebar.markdown("## :bulb: Beall Live")
st.sidebar.markdown("---")

navigate_sidebar = st.sidebar.radio(
    "Go to",
    [
        "Publishers",
        "Standalone Journals"
    ],
    0,
)
st.sidebar.markdown("---")

st.sidebar.markdown("**🐧 Contribute**")
st.sidebar.info(
    "Contributions welcome through comments, issues, and pull requests to the open-source [code base](https://github.com/saurabh-khanna/beall-live)."
)

st.sidebar.markdown("**:octopus: Maitainer**")
st.sidebar.info("[Saurabh Khanna](https://saurabh-khanna.github.io/)")

st.sidebar.markdown("**:scroll: License**")
st.sidebar.info(
    "[GNU Affero General Public License v3.0](https://github.com/saurabh-khanna/beall-live/blob/main/LICENSE)"
)

if navigate_sidebar == "Publishers":
    df = pd.read_csv(Path("data/df_weekly_publishers.csv"))

if navigate_sidebar == "Standalone Journals":
    df = pd.read_csv(Path("data/df_weekly_standalone.csv"))

alive_count = len(df[df["status"] == 200])
alive_perc = round((alive_count / len(df)) * 100, 2)

st.markdown("&nbsp;")
st.write("_Updated: " + df["date"].iloc[0] + "_")

st.info(
    "__"
    + str(alive_perc)
    + "%__ domains on Beall's list are alive this week."
)
st.write("\n")

df_eco = pd.DataFrame(
    [alive_perc, 100 - alive_perc],
    columns=["value"],
)

df_eco["Status"] = ["Alive", "Not alive"]
df_eco["Domains"] = ["Domains", "Domains"]  # dummy column for plot
plot_eco = (
    alt.Chart(df_eco)
    .mark_bar(opacity=0.75)
    .encode(
        x=alt.X("sum(value)", title="Results (%)"),
        y=alt.Y("Domains", title="", sort="x"),
        tooltip=["value"],
        color=alt.Color(
            "Status",
            scale=alt.Scale(
                domain=["Alive", "Not alive"],
                range=["#0ec956", "#ff1717"],
            ),
        ),
    )
    .properties(
        height=125,
    )
    .configure_title(fontSize=18)
    .configure_axis(labelFontSize=15, titleFontSize=15)
)
st.altair_chart(plot_eco, use_container_width=True)
st.markdown("&nbsp;")

navigate = st.radio("View", ["Alive domains", "Dead domains"], 0)

if navigate == "Alive domains":
    df = (
        df[df["status"] == 200][["source", "url"]]
        .sort_values(by=["source"])
        .reset_index(drop=True)
    )
    st.table(df.assign(hack="").set_index("hack"))

if navigate == "Dead domains":
    df = (
        df[df["status"] != 200][["source", "url"]]
        .sort_values(by=["source"])
        .reset_index(drop=True)
    )
    df = df[df["source"] != "DOAJ"]
    st.table(df.assign(hack="").set_index("hack"))
