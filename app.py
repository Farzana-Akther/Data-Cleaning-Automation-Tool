import streamlit as st
import pandas as pd
from cleaner import auto_clean

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Data Cleaning Automation Tool",
    layout="wide",
    page_icon="🧹",
)

# -------------------- DARK/LIGHT THEME TOGGLE --------------------
if "theme" not in st.session_state:
    st.session_state.theme = "light"

toggle = st.toggle("🌗 Toggle Dark/Light Mode", value=(st.session_state.theme == "dark"))
st.session_state.theme = "dark" if toggle else "light"

# -------------------- CUSTOM STYLING --------------------
if st.session_state.theme == "dark":
    bg_color = "#0f172a"
    text_color = "#e2e8f0"
    card_color = "#1e293b"
else:
    bg_color = "#f8fafc"
    text_color = "#1e293b"
    card_color = "#ffffff"

st.markdown(f"""
    <style>
        .main {{
            background-color: {bg_color};
            color: {text_color};
            font-family: 'Poppins', sans-serif;
        }}
        .title {{
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            color: #3b82f6;
        }}
        .subtitle {{
            text-align: center;
            color: #64748b;
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }}
        div.stDownloadButton > button {{
            background-color: #3b82f6 !important;
            color: white !important;
            border-radius: 10px;
            font-size: 1rem;
            padding: 0.6rem 1rem;
        }}
        .dataframe {{
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }}
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown('<h1 class="title">🧹 Data Cleaning Automation Tool</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload your messy data — let AI clean and summarize it automatically.</p>', unsafe_allow_html=True)

# -------------------- FILE UPLOAD --------------------
uploaded_file = st.file_uploader(
    "📂 Upload your data file (CSV, Excel, or JSON)",
    type=["csv", "xlsx", "xls", "json"]
)

if uploaded_file:
    # Read different formats
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith((".xlsx", ".xls")):
        df = pd.read_excel(uploaded_file)
    elif uploaded_file.name.endswith(".json"):
        df = pd.read_json(uploaded_file)
    else:
        st.error("Unsupported file format.")
        st.stop()

    st.markdown("### 📊 Raw Data Preview")
    st.dataframe(df.head(), use_container_width=True)

    # -------------------- SUMMARY STATS --------------------
    st.markdown("### 📈 Summary Statistics (Before Cleaning)")
    col1, col2, col3 = st.columns(3)
    col1.metric("🧾 Total Rows", f"{len(df)}")
    col2.metric("🔢 Columns", f"{len(df.columns)}")
    col3.metric("🧍 Missing Values", f"{df.isna().sum().sum()}")
    st.caption(f"Duplicate Rows: {df.duplicated().sum()} | Data Types: {', '.join(df.dtypes.unique().astype(str))}")



    # -------------------- CLEANING --------------------
    with st.spinner("⚙️ Cleaning data... Please wait ⏳"):
        cleaned_df = auto_clean(df)

    st.success("✅ Cleaning Complete! Your data is ready.", icon="🎉")

    # -------------------- AI EXPLANATION --------------------
    st.markdown("### 🧠 AI Cleaning Summary")
    removed_duplicates = df.duplicated().sum()
    filled_missing = df.isna().sum().sum() - cleaned_df.isna().sum().sum()
    st.info(
        f"""
        - Removed **{removed_duplicates}** duplicate rows  
        - Filled or handled **{filled_missing}** missing values  
        - Standardized column names and formats  
        - Ensured consistent data types across columns  
        """,
        icon="🤖"
    )


    # -------------------- DOWNLOAD SECTION --------------------
    st.markdown("---")
    st.markdown("### 📥 Download Cleaned File")
    st.download_button(
        label="Download Cleaned CSV",
        data=cleaned_df.to_csv(index=False).encode('utf-8'),
        file_name="cleaned_data.csv",
        mime='text/csv'
    )

else:
    st.info("👆 Upload your data to begin cleaning.", icon="📁")

# -------------------- FOOTER --------------------
st.markdown(f"""
<hr style="border:1px solid #e2e8f0; margin-top:2rem;">
<p style="text-align:center; color:{text_color};">
Built with ❤️ using Streamlit | © 2025 DataClean AI
</p>
""", unsafe_allow_html=True)
