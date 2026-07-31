"""
MovieIQ - Predictive Analytics on Film Success
Streamlit Dashboard

Run with:
    streamlit run streamlit_app.py

Place `movies_iq.csv` in the same folder as this script (or upload it
via the sidebar uploader when the app starts).
"""

import ast

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

# ----------------------------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="MovieIQ | Film Success Analytics",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------------------------------------------------
# CUSTOM CSS — pulsing "blood reddish" theme
# ----------------------------------------------------------------------
st.markdown("""
<style>

/* ---------- MAIN APP ---------- */

.stApp{
    background-color:white !important;
}

[data-testid="stAppViewContainer"]{
    background:white !important;
}

[data-testid="stHeader"]{
    background:white !important;
}

/* ---------- SIDEBAR ---------- */

section[data-testid="stSidebar"]{
    background:#F5F5F5 !important;
}

section[data-testid="stSidebar"] *{
    color:black !important;
}

/* ---------- FILE UPLOADER ---------- */

[data-testid="stFileUploader"]{
    background:white !important;
    border:1px solid #DDDDDD;
    border-radius:12px;
    padding:10px;
}

[data-testid="stFileUploaderDropzone"]{
    background:white !important;
    border:2px dashed #CCCCCC;
}

[data-testid="stFileUploader"] *{
    color:black !important;
}

/* ---------- METRICS ---------- */

div[data-testid="stMetric"]{
    background:white;
    border:1px solid #E5E5E5;
    border-radius:10px;
    padding:15px;
}

div[data-testid="stMetricLabel"]{
    color:#444 !important;
}

div[data-testid="stMetricValue"]{
    color:#111 !important;
}

/* ---------- RADIO ---------- */

div[role="radiogroup"]{
    gap:18px;
}

div[role="radiogroup"] label{
    color:black !important;
    font-weight:600;
    opacity:1 !important;
}

/* ---------- HEADINGS ---------- */

h1,h2,h3,h4{
    color:#111827 !important;
}

</style>
""", unsafe_allow_html=True)

# Make matplotlib/seaborn plots blend with the dark theme
plt.style.use("default")
sns.set_theme(style="whitegrid")

# ----------------------------------------------------------------------
# DATA LOADING
# ----------------------------------------------------------------------
@st.cache_data(show_spinner="Loading and preparing dataset...")
def load_data(file) -> pd.DataFrame:
    df = pd.read_csv(file)

    # genres column stores a list-of-dicts as a string -> parse it
    if df["genres"].dtype == object:
        try:
            df["genres"] = df["genres"].apply(ast.literal_eval)
        except (ValueError, SyntaxError):
            pass  # already parsed / not in that format

    if df["genres"].apply(lambda x: isinstance(x, list)).any():
        df["movie_id"] = df["genres"].apply(
            lambda i: i[0]["id"] if isinstance(i, list) and len(i) > 0 else None
        )
        df["genres"] = df["genres"].apply(
            lambda x: x[0]["name"] if isinstance(x, list) and len(x) > 0 else None
        )

    df["genres"] = df["genres"].fillna("N/A")
    if "movie_id" in df.columns:
        df["movie_id"] = df["movie_id"].fillna("N/A")

    # revenue-to-budget ("perfect") ratio, guarding against div-by-zero
    df["perfect_ratio"] = df["revenue"] / df["budget"].replace(0, np.nan)

    return df


with st.sidebar:
    st.markdown("## 🎬 MovieIQ")
    st.caption("Predictive Analytics on Film Success")
    st.divider()

    uploaded = st.file_uploader("Upload movies_iq.csv", type="csv")
    data_path = uploaded if uploaded is not None else "movies_iq.csv"

try:
    df = load_data(data_path)
except FileNotFoundError:
    st.error(
        "Couldn't find `movies_iq.csv`. Upload it using the sidebar uploader "
        "to load the dashboard."
    )
    st.stop()

# ----------------------------------------------------------------------
# PRE-COMPUTED SUMMARY STATS
# ----------------------------------------------------------------------
total_rows = len(df)
top_revenue_row = df.loc[df["revenue"].idxmax()]
popular_genre = df["genres"].value_counts().idxmax()
popular_genre_count = df["genres"].value_counts().max()
max_perfect_ratio = df["perfect_ratio"].max()
max_perfect_ratio_movie = df.loc[df["perfect_ratio"].idxmax(), "title"]

# ----------------------------------------------------------------------
# SIDEBAR NAVIGATION
# ----------------------------------------------------------------------
with st.sidebar:
    st.divider()
    page = st.radio(
        "Navigate",
        ["🏠 Overview", "🗂️ Dataset Description", "📊 EDA Charts"],
        label_visibility="collapsed",
    )
    st.divider()
    st.caption("Built with Streamlit • MovieIQ Project")


# ========================================================================
# PAGE 1 — OVERVIEW
# ========================================================================
if page == "🏠 Overview":
    st.title("🎬 MovieIQ — Predictive Analytics on Film Success")
    st.subheader("Project Overview")

    st.markdown(
        """
        **MovieIQ** explores what actually drives a movie's commercial success,
        using a dataset of financial, popularity, and rating attributes for
        thousands of films. The project moves through **data wrangling**
        (parsing nested genre data, handling missing values, engineering a
        revenue-to-budget *"perfect ratio"* feature) and then an **exploratory
        data analysis (EDA)** built around 11 core questions.
        """
    )

    st.markdown("#### Key Questions Explored")
    st.markdown(
        """
        1. Does a higher budget lead to higher revenue?
        2. Which genres are most **common** vs. most **successful**?
        3. Do popularity, runtime, or ratings correlate with success?
        4. Are any numerical features basically duplicates of each other (correlation heatmap)?
        5. What does the distribution of movie budgets look like?
        6. What does the distribution of movie revenues look like?
        7. Which genres generate the highest average revenue?
        8. Which genres require the highest average budget?
        9. Do successful movies have higher budgets than unsuccessful ones?
        10. Do successful movies earn a higher revenue-to-budget ratio?
        11. Which movies achieved the highest return on investment (ROI)?
        """
    )

    st.markdown("#### Headline Findings")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            """
            - Budget and revenue show a **strong positive correlation** (r ≈ 0.75) —
              budget sets a *ceiling* on revenue rather than guaranteeing it.
            - **Romance** is the most common genre, but **Drama** has the highest
              success rate (~82%).
            - Popularity, runtime, and vote average show **near-zero correlation**
              with success.
            """
        )
    with c2:
        st.markdown(
            """
            - The dataset shows **low multicollinearity** — most numeric features
              are safe to keep for modeling.
            - Successful movies earn a markedly **higher revenue-to-budget ratio**
              than unsuccessful ones (median ~2×).
            - Revenue-to-budget ratio (perfect ratio) is a **strong indicator**
              of commercial success — more so than raw budget.
            """
        )

    st.info(
        "Use the navigation on the left to explore the raw dataset "
        "statistics or dive into the full set of EDA visualizations.",
        icon="🎬",
    )


# ========================================================================
# PAGE 2 — DATASET DESCRIPTION
# ========================================================================
elif page == "🗂️ Dataset Description":
    st.title("🗂️ Dataset Description")
    st.caption("A quick statistical snapshot of the MovieIQ dataset")

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Rows", f"{total_rows:,}")
    m2.metric("Highest Revenue Movie", str(top_revenue_row["title"])[:22])
    m3.metric("Most Popular Genre", f"{popular_genre} ({popular_genre_count})")
    m4.metric("Max Perfect Ratio", f"{max_perfect_ratio:,.2f}x")

    st.divider()

    col1, col2 = st.columns([1, 1])
    with col1:
        st.markdown("##### 🏆 Highest Revenue Movie")
        st.write(
            f"**{top_revenue_row['title']}** generated "
            f"**${top_revenue_row['revenue']:,.0f}** in revenue "
            f"on a budget of **${top_revenue_row['budget']:,.0f}**."
        )
        st.markdown("##### 💰 Max Perfect Ratio (Revenue ÷ Budget)")
        st.write(
            f"**{max_perfect_ratio_movie}** achieved the highest ratio at "
            f"**{max_perfect_ratio:,.2f}x** — meaning it earned about "
            f"{max_perfect_ratio:,.0f} times its production budget."
        )

    with col2:
        st.markdown("##### 🎭 Genre Breakdown (Top 10)")
        st.bar_chart(df["genres"].value_counts().head(10))

    st.divider()
    st.markdown("##### 📋 Raw Data Preview")
    st.dataframe(df.head(20), use_container_width=True)

    st.markdown("##### 📈 Statistical Summary")
    st.dataframe(df.describe(), use_container_width=True)


# ========================================================================
# PAGE 3 — EDA CHARTS
# ========================================================================
elif page == "📊 EDA Charts":
    st.title("📊 Exploratory Data Analysis")
    st.caption("All charts from the MovieIQ EDA, grouped for quick access")

    toggle = st.radio(
    "Choose Analysis",
    [
        "📈 Budget & Revenue",
        "🎬 Genre Analysis",
        "💰 ROI Analysis"
    ],
    horizontal=True
)
    st.divider()

    # ---------------- Total Rows: distributions & overall relationships -------
    if toggle=="📈 Budget & Revenue":
        st.subheader("Dataset-wide Distributions & Relationships")

        c1, c2 = st.columns(2)
        with c1:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ax.scatter(df["budget"], df["revenue"], color="green", alpha=0.6)
            ax.set_title("Budget vs Revenue")
            ax.set_xlabel("Budget")
            ax.set_ylabel("Revenue")
            st.pyplot(fig)
            st.caption(
                f"Correlation (budget vs revenue): "
                f"{df['budget'].corr(df['revenue']):.2f} — a strong positive relationship."
            )

        with c2:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            corr = df.drop(columns=["movie_id"], errors="ignore").select_dtypes(
                include="number"
            ).corr()
            sns.heatmap(corr, annot=True, cmap="rocket", fmt=".2f", ax=ax)
            ax.set_title("Correlation Heatmap")
            st.pyplot(fig)

        c3, c4 = st.columns(2)
        with c3:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ax.hist(df["budget"].dropna(), bins=30, color="#c0392b", edgecolor="black")
            ax.set_title("Distribution of Movie Budgets")
            ax.set_xlabel("Budget")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        with c4:
            fig, ax = plt.subplots(figsize=(6, 4.5))
            ax.hist(df["revenue"].dropna(), bins=30, color="#f1c40f", edgecolor="black")
            ax.set_title("Distribution of Movie Revenues")
            ax.set_xlabel("Revenue")
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

    # ---------------- Highest Revenue Movie: top revenue / ROI charts ---------
    elif toggle == "Highest Revenue Movie":
        st.subheader("Top-Performing Movies by Revenue")

        top10_rev = df[["title", "revenue"]].sort_values(
            "revenue", ascending=False
        ).head(10)
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.bar(top10_rev["title"], top10_rev["revenue"], color="#e74c3c", edgecolor="black")
        ax.set_title("Top 10 Highest Revenue Movies")
        ax.set_xlabel("Title")
        ax.set_ylabel("Revenue")
        plt.setp(ax.get_xticklabels(), rotation=75, ha="right")
        st.pyplot(fig)

        st.markdown(
            f"**{top_revenue_row['title']}** is the highest-grossing movie in "
            f"the dataset, earning **${top_revenue_row['revenue']:,.0f}**."
        )

    # ---------------- Popular Genre: genre-focused charts ----------------------
    elif toggle=="🎬 Genre Analysis":
        st.subheader("Genre Popularity vs. Success")

        summary = df.groupby("genres", observed=False).agg(
            count=("genres", "count"),
            success_rate=("success", "mean") if "success" in df.columns else ("genres", "count"),
        ).sort_values("count", ascending=False).reset_index()

        fig, ax1 = plt.subplots(figsize=(9, 5))
        ax1.bar(summary["genres"], summary["count"], color="#3498db", label="Count")
        ax1.set_ylabel("Count", color="#3498db")
        ax1.set_xlabel("Genre")
        plt.setp(ax1.get_xticklabels(), rotation=45, ha="right")

        if "success" in df.columns:
            ax2 = ax1.twinx()
            ax2.plot(
                summary["genres"], summary["success_rate"],
                color="#e74c3c", marker="o", label="Success Rate",
            )
            ax2.set_ylabel("Success Rate", color="#e74c3c")

        ax1.set_title("Genre: Count vs Success Rate")
        st.pyplot(fig)

        c1, c2 = st.columns(2)
        with c1:
            avg_revenue = df.groupby("genres", observed=False)["revenue"].mean().sort_values(
                ascending=False
            )
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(x=avg_revenue.index, y=avg_revenue.values, palette="rocket", ax=ax)
            ax.set_title("Average Revenue by Genre")
            ax.set_xlabel("Genre")
            ax.set_ylabel("Average Revenue")
            plt.setp(ax.get_xticklabels(), rotation=75, ha="right")
            st.pyplot(fig)

        with c2:
            avg_budget = df.groupby("genres", observed=False)["budget"].mean().sort_values(
                ascending=False
            )
            fig, ax = plt.subplots(figsize=(6, 5))
            sns.barplot(x=avg_budget.index, y=avg_budget.values, palette="flare", ax=ax)
            ax.set_title("Average Budget by Genre")
            ax.set_xlabel("Genre")
            ax.set_ylabel("Average Budget")
            plt.setp(ax.get_xticklabels(), rotation=75, ha="right")
            st.pyplot(fig)

        st.markdown(
            f"**{popular_genre}** is the most common genre with "
            f"**{popular_genre_count}** movies in the dataset."
        )

    # ---------------- Maximum Perfect Ratio: ROI / success charts -------------
    elif toggle=="💰 ROI Analysis":
        st.subheader("Return on Investment (Revenue ÷ Budget)")

        roi = df[["title", "perfect_ratio"]].dropna().sort_values(
            "perfect_ratio", ascending=False
        ).head(10)
        fig, ax = plt.subplots(figsize=(9, 5))
        sns.barplot(data=roi, x="title", y="perfect_ratio", palette="coolwarm", ax=ax, edgecolor="black")
        ax.set_title("Highest ROI Movies")
        ax.set_xlabel("Movie Title")
        ax.set_ylabel("Perfect Ratio")
        plt.setp(ax.get_xticklabels(), rotation=75, ha="right")
        st.pyplot(fig)

        if "success" in df.columns:
            c1, c2 = st.columns(2)
            with c1:
                fig, ax = plt.subplots(figsize=(6, 5))
                sns.boxplot(data=df, x="success", y="budget", hue="success", palette="viridis", legend=False, ax=ax)
                ax.set_title("Budget Distribution by Success")
                ax.set_xlabel("Success (0 = No, 1 = Yes)")
                ax.set_ylabel("Budget")
                st.pyplot(fig)

            with c2:
                fig, ax = plt.subplots(figsize=(6, 5))
                sns.boxplot(data=df, x="success", y="perfect_ratio", hue="success", palette="plasma", legend=False, ax=ax)
                ax.set_title("Revenue-to-Budget Ratio by Success")
                ax.set_xlabel("Success (0 = No, 1 = Yes)")
                ax.set_ylabel("Perfect Ratio")
                st.pyplot(fig)

        st.markdown(
            f"**{max_perfect_ratio_movie}** recorded the highest revenue-to-budget "
            f"ratio at **{max_perfect_ratio:,.2f}x**."
        )
