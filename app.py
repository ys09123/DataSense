import os
import streamlit as st
import pandas as pd
from google import genai
from dotenv import load_dotenv

# ── Setup & Config ────────────────────────────────────────────────────────────
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.5-flash"

st.set_page_config(page_title="DataSense", layout="wide", page_icon="⚡")

# ── Modern Dark SaaS UI Styling ───────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

/* Base Colors & Typography */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #0B0F19; /* Deep space navy */
    color: #94A3B8; /* Slate gray text */
}
.stApp {
    background-color: #0B0F19;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111827 !important; /* Slightly lighter navy */
    border-right: 1px solid #1E293B !important;
}
section[data-testid="stSidebar"] > div {
    padding: 2rem 1.5rem !important;
}
section[data-testid="stSidebar"] label {
    font-family: 'Inter', sans-serif !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #64748B !important;
}

/* Fix Streamlit File Uploader for Dark Mode */
[data-testid="stFileUploadDropzone"] {
    background-color: #1E293B !important;
    border: 1px dashed #334155 !important;
    border-radius: 8px !important;
    color: #E2E8F0 !important;
    transition: all 0.2s ease;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: #6366F1 !important; /* Indigo hover */
    background-color: #232d42 !important;
}
[data-testid="stFileUploadDropzone"] section { padding: 1.2rem !important; }
[data-testid="stFileUploadDropzone"] button {
    background-color: #3B82F6 !important;
    color: white !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}
/* Hide default glitchy text */
[data-testid="stFileUploadDropzone"] div div span { display: none !important; }
[data-testid="stFileUploadDropzone"] div div small { display: none !important; }

/* Main Content Wrapper */
.block-container {
    padding: 3rem 4rem !important;
    max-width: 1200px !important;
}

/* Typography Overrides */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 700 !important;
    color: #F8FAFC !important; /* Off-white for headers */
    letter-spacing: -0.02em !important;
}
h2 { font-size: 1.4rem !important; padding-bottom: 0.5rem !important; margin-top: 2rem !important; border-bottom: 1px solid #1E293B !important; }

/* Custom Page Header */
.header-container {
    margin-bottom: 2.5rem;
}
.page-title {
    font-size: 2.5rem;
    color: #F8FAFC;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
    background: linear-gradient(to right, #60A5FA, #A78BFA);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.page-subtitle {
    font-size: 14px;
    color: #64748B;
    font-weight: 400;
}

/* Dataset Metric Cards */
.metrics-grid {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
}
.metric-card {
    background: #111827;
    border: 1px solid #1E293B;
    border-radius: 10px;
    padding: 1.2rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 0.3rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.metric-value {
    font-family: 'Fira Code', monospace;
    font-size: 1.5rem;
    color: #F8FAFC;
    font-weight: 600;
}
.metric-label {
    font-size: 11px;
    color: #64748B;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 600;
}

/* Buttons */
.stButton > button {
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    font-weight: 600 !important;
    background: linear-gradient(135deg, #4F46E5 0%, #3B82F6 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 2rem !important;
    box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3) !important;
    transition: all 0.2s ease !important;
}
.stButton > button:hover { transform: translateY(-1px) !important; box-shadow: 0 6px 16px rgba(59, 130, 246, 0.4) !important; }

/* Code Blocks & DataFrames */
div[data-testid="stCodeBlock"] {
    background: #111827 !important;
    border: 1px solid #1E293B !important;
    border-radius: 8px !important;
    font-family: 'Fira Code', monospace !important;
}
.stDataFrame {
    border: 1px solid #1E293B !important;
    border-radius: 8px !important;
}

/* AI Insights Box (Mapping to st.info) */
div[data-testid="stAlert"] {
    background: rgba(59, 130, 246, 0.1) !important; /* Translucent blue */
    border: 1px solid rgba(59, 130, 246, 0.2) !important;
    border-left: 4px solid #3B82F6 !important;
    border-radius: 8px !important;
    padding: 1.5rem !important;
    color: #E2E8F0 !important;
}
div[data-testid="stAlert"] p, div[data-testid="stAlert"] li {
    font-size: 14px !important;
    color: #CBD5E1 !important;
    line-height: 1.6 !important;
}
div[data-testid="stAlert"] strong {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

/* Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: #0B0F19; }
::-webkit-scrollbar-thumb { background: #334155; border-radius: 4px; }
::-webkit-scrollbar-thumb:hover { background: #475569; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div style="margin-bottom: 0.5rem; font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em;">Data Source</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader("", type=["csv"], label_visibility="collapsed")

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_client():
    return genai.Client(api_key=api_key)

def generate(client, prompt):
    response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
    return response.text.strip()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-container">
    <div class="page-title">DataSense - AI Data Analyst</div>
    <div class="page-subtitle">Upload your CSV payload. Gemini handles the EDA and statistical synthesis.</div>
</div>
""", unsafe_allow_html=True)

# ── Guards & Empty State ──────────────────────────────────────────────────────
if not api_key:
    st.error("GEMINI_API_KEY not found. Add it to a `.env` file: `GEMINI_API_KEY=your_key_here`")
    st.stop()

if uploaded_file is None:
    st.markdown("""
    <div style="margin-top: 2rem; padding: 4rem 2rem; border: 1px dashed #334155; border-radius: 12px; text-align: center; background: #111827;">
        <div style="font-size: 2.5rem; margin-bottom: 1rem;">📊</div>
        <div style="font-size: 1.2rem; color: #E2E8F0; font-weight: 600;">Awaiting Data Payload</div>
        <div style="font-size: 14px; color: #64748B; margin-top: 0.5rem;">Drop a CSV using the sidebar to start analysis.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ── Load Data & Display Metrics ───────────────────────────────────────────────
df = pd.read_csv(uploaded_file)
num_cols  = len(df.select_dtypes(include="number").columns)
null_cols = int((df.isnull().sum() > 0).sum())

# Render modern metric cards
st.markdown(f"""
<div class="metrics-grid">
    <div class="metric-card">
        <div class="metric-value">{df.shape[0]:,}</div>
        <div class="metric-label">Total Rows</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{df.shape[1]}</div>
        <div class="metric-label">Total Columns</div>
    </div>
    <div class="metric-card">
        <div class="metric-value">{num_cols}</div>
        <div class="metric-label">Numeric Features</div>
    </div>
    <div class="metric-card">
        <div class="metric-value" style="color: #F87171;">{null_cols}</div>
        <div class="metric-label">Columns w/ Nulls</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size: 12px; color: #64748B; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.5rem;">Dataset Preview</div>', unsafe_allow_html=True)
st.dataframe(df.head(), use_container_width=True, hide_index=True)

schema_info = {
    "columns":        df.columns.tolist(),
    "dtypes":         df.dtypes.astype(str).to_dict(),
    "missing_values": df.isnull().sum().to_dict(),
    "shape":          df.shape,
}

# ── Execution ─────────────────────────────────────────────────────────────────
st.markdown("<div style='margin-top:2rem'></div>", unsafe_allow_html=True)
if st.button("Start Exploration ⚡"):
    client = get_client()

    # 1. Generate EDA Code (Inside Dropdown/Expander)
    with st.expander("🛠️ View Generated Python Code", expanded=False):
        with st.spinner("Compiling EDA code..."):
            code_prompt = f"""
            You are a senior data engineer.
            Dataset metadata: {schema_info}
            
            Write pristine, executable Python using pandas, matplotlib, seaborn to:
            1. Print exact summary statistics
            2. Plot clean distributions for all numeric columns
            3. Plot a correlation heatmap
            4. Visualise missing value density
            
            Rules:
            - Output ONLY executable Python code. No markdown formatting or fences around it.
            - Assume `df` is already a loaded DataFrame.
            - Use `plt.tight_layout()` and `plt.show()` after plots.
            - *Optional: Use a dark theme for the plots (e.g., plt.style.use("dark_background")) to match the UI.*
            """
            try:
                code = generate(client, code_prompt)
                if code.startswith("```"):
                    code = "\n".join(
                        l for l in code.splitlines()
                        if not l.strip().startswith("```")
                    ).strip()
                
                st.code(code, language="python")
            except Exception as e:
                st.error(f"Error generating code: {e}")

    # 2. Generate and display Insights (Below the Expander)
    with st.spinner("Synthesizing metrics..."):
        summary = df.describe(include="all").to_string()
        insight_prompt = f"""
        You are an expert data scientist.
        Summary statistics: {summary}
        Schema info: {schema_info}
        
        Provide an analytical brief covering:
        - **Key observations** in the dataset
        - **Data health** (nulls, extreme outliers, distributions)
        - **Correlations & relationships** between variables
        - **Strategic recommendations** for modeling
        
        Format clearly in Markdown. Be extremely concise, insightful, and professional. Use headers and bullet points.
        """
        try:
            insights = generate(client, insight_prompt)
            st.markdown('<h2>Exploratory Insights</h2>', unsafe_allow_html=True)
            st.info(insights, icon="🧠") 
        except Exception as e:
            st.error(f"Error generating insights: {e}")