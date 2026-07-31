# 🎬 MovieIQ: Predictive Analytics on Film Success

## 📌 Project Overview

MovieIQ is an Exploratory Data Analysis (EDA) and interactive dashboard project that investigates the factors influencing a movie's commercial success. Using Python, Pandas, Matplotlib, Seaborn, and Streamlit, this project analyzes relationships between production budget, revenue, genres, popularity, runtime, ratings, and return on investment (ROI).

The project aims to uncover meaningful business insights through data visualization and provide an interactive dashboard for exploring movie performance.

---

## 🎯 Objectives

- Analyze the relationship between production budget and revenue.
- Identify the most common and most successful movie genres.
- Study how popularity, runtime, and ratings relate to commercial success.
- Detect correlations among numerical features.
- Evaluate movie profitability using Revenue-to-Budget Ratio (ROI).
- Build an interactive Streamlit dashboard for data exploration.

---

## 📂 Dataset Information

The dataset contains information about movies, including:

- Movie Title
- Genre
- Budget
- Revenue
- Popularity
- Runtime
- Average Rating
- Success (Binary: 1 = Successful, 0 = Unsuccessful)
- Genre ID
- Revenue-to-Budget Ratio (Perfect Ratio)

---

## 🛠 Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit

---

## 📊 Exploratory Data Analysis (EDA)

The following analyses were performed:

1. Does a higher budget lead to higher revenue?
2. Which genres are the most common and the most successful?
3. Do popularity, runtime, and ratings correlate with success?
4. Correlation Heatmap to identify redundant features.
5. Distribution of Movie Budgets.
6. Distribution of Movie Revenues.
7. Average Revenue by Genre.
8. Average Budget by Genre.
9. Budget Distribution of Successful vs Unsuccessful Movies.
10. Revenue-to-Budget Ratio by Movie Success.
11. Top 10 Movies by Return on Investment (ROI).
12. Top 10 Highest Revenue Movies.

---

## 📈 Key Findings

- Budget and revenue exhibit a strong positive correlation.
- Most movie revenues are positively skewed, with a few blockbuster movies generating exceptionally high earnings.
- Revenue-to-Budget Ratio is a strong indicator of commercial success.
- Genre has only a modest influence on average revenue and budget.
- Successful movies generally achieve significantly higher ROI than unsuccessful movies.
- No severe multicollinearity was observed among the numerical features.

---

## 🖥 Streamlit Dashboard Features

The dashboard consists of:

### 🏠 Project Overview
- Project summary
- Objectives
- Key findings

### 📂 Dataset Description
- Total movies
- Highest revenue movie
- Most popular genre
- Maximum ROI
- Dataset preview
- Statistical summary

### 📊 EDA Visualizations
- Budget vs Revenue Scatter Plot
- Budget Distribution
- Revenue Distribution
- Genre Analysis
- Correlation Heatmap
- ROI Analysis
- Top Revenue Movies
- Interactive KPI Metrics

---

## 📁 Project Structure

```
MovieIQ/
│
├── movies_iq.csv
├── MovieIQ_EDA.ipynb
├── streamlit_app.py
├── requirements.txt
├── README.md
└── images/
```

---

## 🚀 How to Run

### Clone the repository

```bash
git clone https://github.com/your-username/MovieIQ.git
```

### Navigate to the project

```bash
cd MovieIQ
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the Streamlit application

```bash
streamlit run streamlit_app.py
```

---

## 📷 Dashboard Preview

You can include screenshots of:

- Project Overview
- Dataset Description
- EDA Dashboard
- KPI Cards

inside an `images/` folder and display them here.

Example:

```markdown
![Dashboard](images/dashboard.png)
```

---

## 📚 Skills Demonstrated

- Data Cleaning
- Feature Engineering
- Exploratory Data Analysis (EDA)
- Data Visualization
- Business Insight Generation
- Dashboard Development
- Python Programming
- Statistical Analysis

---

## 👨‍💻 Author

**Sahil Verma**

Aspiring Data Scientist

---

## ⭐ If you found this project useful

Please consider giving this repository a ⭐ on GitHub.
