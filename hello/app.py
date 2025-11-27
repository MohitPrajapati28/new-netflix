import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_js_eval import streamlit_js_eval

st.set_page_config(page_title="Netflix Dashboard", layout="wide")
st.title("🎬 Netflix Recommendation System")

# Local Storage
st.sidebar.header("User Info")
username = streamlit_js_eval(js_expressions="localStorage.getItem('username')")
if username is None:
    username = "Guest"

st.sidebar.write(f"👋 Welcome, {username}")

new_name = st.sidebar.text_input("Enter Name to Save")
if st.sidebar.button("Save"):
    streamlit_js_eval(js_expressions=f"localStorage.setItem('username','{new_name}')")
    st.sidebar.success("Saved to Local Storage")

uploaded_file = st.file_uploader("Upload Netflix CSV Dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    df.columns = df.columns.str.strip().str.replace(" ", "_").str.title()
    df["Genre"] = df["Genre"].str.title()
    df["Title"] = df["Title"].str.title()
    df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")
    df.dropna(inplace=True)

    st.success("Data Cleaned Successfully!")
    st.dataframe(df.head())

    st.subheader("📈 KPI Dashboard")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Movies", len(df))
    c2.metric("Unique Genres", df["Genre"].nunique())
    c3.metric("Average Rating", round(df["Rating"].mean(),2))
    c4.metric("Max Views", df["Views"].max())

    st.subheader("📊 Visualizations")
    st.plotly_chart(px.bar(df["Genre"].value_counts(), title="Movies by Genre"), use_container_width=True)
    st.plotly_chart(px.histogram(df, x="Rating", title="Rating Distribution"), use_container_width=True)
    st.plotly_chart(px.box(df, x="Genre", y="Views", title="Views by Genre"), use_container_width=True)

    top10 = df.nlargest(10,"Views")
    st.plotly_chart(px.bar(top10, x="Title", y="Views", title="Top 10 Movies"), use_container_width=True)
else:
    st.info("Upload CSV file to start.")
