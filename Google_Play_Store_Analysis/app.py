
import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Google Play Store Analysis",
    page_icon="📱",
    layout="wide"
)

# Load cleaned dataset
@st.cache_data
def load_data():
    return pd.read_csv("googleplaystore_cleaned.csv")

df = load_data()

# Dashboard title
st.title("📱 Google Play Store Data Analysis")
st.markdown("Interactive dashboard to explore Play Store applications.")

# Sidebar filters
st.sidebar.header("Dashboard Filters")

categories = sorted(df["Category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Categories",
    categories,
    default=categories
)

types = sorted(df["Type"].dropna().unique())

selected_types = st.sidebar.multiselect(
    "Select App Type",
    types,
    default=types
)

min_rating = st.sidebar.slider(
    "Minimum Rating",
    min_value=0.0,
    max_value=5.0,
    value=0.0,
    step=0.1
)

search_app = st.sidebar.text_input("Search App Name")

# Apply filters
filtered_df = df[
    (df["Category"].isin(selected_categories)) &
    (df["Type"].isin(selected_types)) &
    (df["Rating"] >= min_rating)
]

if search_app:
    filtered_df = filtered_df[
        filtered_df["App"].str.contains(
            search_app,
            case=False,
            na=False
        )
    ]

# KPI cards
st.subheader("📊 Dashboard Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Apps", f"{len(filtered_df):,}")

avg_rating = filtered_df["Rating"].mean()
col2.metric(
    "Average Rating",
    f"{avg_rating:.2f}" if pd.notna(avg_rating) else "N/A"
)

total_installs = filtered_df["Installs"].sum()
col3.metric("Total Installs", f"{total_installs:,.0f}")

paid_apps = (filtered_df["Type"] == "Paid").sum()
col4.metric("Paid Apps", f"{paid_apps:,}")

st.divider()

if filtered_df.empty:
    st.warning("No apps found. Please change your filters.")
else:
    # Category chart
    st.subheader("Top 10 App Categories")

    category_data = (
        filtered_df["Category"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    category_data.columns = ["Category", "Apps"]

    fig1 = px.bar(
        category_data,
        x="Apps",
        y="Category",
        orientation="h",
        color="Apps",
        title="Number of Apps by Category"
    )
    st.plotly_chart(fig1, width="stretch")

    # Rating distribution
    st.subheader("App Rating Distribution")

    fig2 = px.histogram(
        filtered_df,
        x="Rating",
        nbins=20,
        title="Distribution of App Ratings",
        color_discrete_sequence=["#636EFA"]
    )
    st.plotly_chart(fig2, width="stretch")

    # Free vs Paid chart
    st.subheader("Free vs Paid Apps")

    type_data = (
        filtered_df["Type"]
        .value_counts()
        .reset_index()
    )
    type_data.columns = ["Type", "Count"]

    fig3 = px.pie(
        type_data,
        names="Type",
        values="Count",
        hole=0.4,
        title="Free and Paid App Distribution"
    )
    st.plotly_chart(fig3, width="stretch")
    # Top installed apps
    st.subheader("Top 10 Apps by Installs")

    top_apps = (
        filtered_df
        .sort_values("Installs", ascending=False)
        .drop_duplicates(subset=["App"])
        .head(10)
    )

    fig4 = px.bar(
        top_apps,
        x="Installs",
        y="App",
        orientation="h",
        title="Top Installed Apps"
    )
    st.plotly_chart(fig4, width="stretch")


    # Data preview
    st.subheader("📋 App Data Preview")
    st.dataframe(filtered_df, width="stretch")

    # Download filtered data
    csv_data = filtered_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download Filtered Data",
        data=csv_data,
        file_name="filtered_play_store_data.csv",
        mime="text/csv"
    )

st.success("Dashboard loaded successfully!")
