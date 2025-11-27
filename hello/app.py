import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit_js_eval

st.set_page_config(page_title="Netflix Data Dashboard", layout="wide")

st.title("🎬 Netflix Recommendation System Dashboard")

# ---------- Local Storage ----------
st.sidebar.header("Local Storage")

username = streamlit_js_eval.get_js(
    "localStorage.getItem('username')",
    default="Guest"
)

st.sidebar.write(f"👋 Welcome, {username}")

new_name = st.sidebar.text_input("Enter your name to save")

if st.sidebar.button("Save to Local Storage"):
    streamlit_js_eval.set_js(
        "localStorage.setItem('username', value)",
        value=new_name
    )
    st.sidebar.success("Saved to Local Storage!")

# ---------- File Upload Section ----------
uploaded_file = st.file_uploader("📂 Upload your Netflix CSV dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ------- DATA CLEANING -------
    df.columns = df.columns.str.strip().str.replace(" ", "_").str.title()

    if "Title" in df.columns:
        df["Title"] = df["Title"].str.title()

    if "Genre" in df.columns:
        df["Genre"] = df["Genre"].str.title()

    if "Rating" in df.columns:
        df["Rating"] = pd.to_numeric(df["Rating"], errors="coerce")

    df.dropna(inplace=True)

    st.success("✨ Data cleaned successfully!")

    st.write("### Cleaned Data Preview")
    st.dataframe(df.head())

    # ---------- KPI Dashboard ----------
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Movies", len(df))
    col2.metric("Unique Genres", df["Genre"].nunique())
    col3.metric("Average Rating", round(df["Rating"].mean(), 2))
    col4.metric("Max Views", df["Views"].max())

    st.markdown("---")

    # ---------- VISUALIZATIONS ----------
    st.subheader("📊 Visual Insights")

    # Movies by Genre
    fig1 = px.bar(df["Genre"].value_counts(), title="Movies per Genre")
    st.plotly_chart(fig1, use_container_width=True)

    # Rating Distribution
    fig2 = px.histogram(df, x="Rating", nbins=20, title="Rating Distribution")
    st.plotly_chart(fig2, use_container_width=True)

    # Views Boxplot
    fig3 = px.box(df, x="Genre", y="Views", title="Views by Genre")
    st.plotly_chart(fig3, use_container_width=True)

    # Top 10 Movies by View Count
    top10 = df.nlargest(10, "Views")
    fig4 = px.bar(top10, x="Title", y="Views", title="Top 10 Most Watched Movies")
    st.plotly_chart(fig4, use_container_width=True)

    # Simple Recommendation Engine
    st.subheader("🎯 Movie Recommendation Engine")
    selected_genre = st.selectbox("Choose Genre", df["Genre"].unique())
    recommended = df[(df["Genre"] == selected_genre) & (df["Rating"] > 4)]
    st.write("Recommended Movies")
    st.dataframe(recommended)

else:
    st.info("Please upload a CSV file to view the dashboard.")
