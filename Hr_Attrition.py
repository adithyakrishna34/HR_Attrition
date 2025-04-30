import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import base64

# === Add Background Image ===
def add_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# === Page Config ===
st.set_page_config(page_title="HR Attrition Risk Analyzer", layout="wide")
add_background("GEC_BG.jpeg")  # Replace with your background image

# === HEADER WITH LOGO ===
col1, col2 = st.columns([1, 6])
with col1:
    logo = Image.open("GEC_Logo.jpeg")
    st.image(logo, width=100)
with col2:
    st.title("HR Attrition Risk Analyzer")
    st.markdown("Designed for proactive HR decision-making and individual risk analysis.")

st.markdown("---")

# === File Upload ===
uploaded_file = st.file_uploader("hr_attrition_dataset", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    # Dataset preview
    with st.expander("🔍 Preview Uploaded Dataset"):
        st.dataframe(df.head())

    # Employee selector
    st.subheader("🔎 Select an Employee")
    search_option = st.selectbox("Search by:", ["Employee_ID", "Employee_Name"])
    selected_value = st.selectbox(f"Select {search_option}:", df[search_option].unique())

    emp_data = df[df[search_option] == selected_value].iloc[0]

    # === CANDIDATE INFO SECTION ===
    st.markdown("## 🧑 Candidate Details")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**👤 Name:** {emp_data['Employee_Name']}")
        st.markdown(f"**🆔 ID:** {emp_data['Employee_ID']}")
        st.markdown(f"**🏢 Department:** {emp_data['Department']}")
        st.markdown(f"**🕒 Years at Company:** {emp_data['Years_at_Company']}")

    with col2:
        risk = emp_data['Attrition_Risk']
        if risk == 'High':
            st.error(f"🔴 Attrition Risk: **{risk}**")
        elif risk == 'Medium':
            st.warning(f"🟡 Attrition Risk: **{risk}**")
        else:
            st.success(f"🟢 Attrition Risk: **{risk}**")

    st.markdown("---")

    # === METRIC BAR CHART ===
    st.subheader("📊 HR Profile Metrics (Bar Chart)")

    bar_metrics = {
        "Engagement Score": emp_data["Engagement_Score"],
        "Attraction Score": emp_data["Attraction_Score"],
        "Job Satisfaction": emp_data["Job_Satisfaction"] * 20,
        "Work-Life Balance": emp_data["Work_Life_Balance_Score"] * 20,
        "Performance Rating": emp_data["Performance_Rating"] * 20
    }

    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.bar(bar_metrics.keys(), bar_metrics.values(), color='#4E79A7', edgecolor='black')

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 1, f'{height:.1f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

    ax.set_ylim(0, 120)
    ax.set_ylabel("Score", fontsize=12)
    ax.set_title("Employee’s HR Score Metrics", fontsize=14, fontweight='bold')
    ax.tick_params(axis='x', rotation=30)
    ax.grid(axis='y', linestyle='--', alpha=0.5)

    st.pyplot(fig)

    # === Summary Message ===
    st.markdown("### 📌 Summary & Suggestion")
    if risk == 'High':
        st.error("⚠️ Immediate attention needed. High attrition risk due to poor engagement or other red flags.")
    elif risk == 'Medium':
        st.warning("⚠️ Medium risk. Monitor and take actions to improve satisfaction and retention.")
    else:
        st.success("✅ Low attrition risk. Employee appears stable and positively engaged.")

else:
    st.info("📤 Upload an Excel file to begin the analysis.")
