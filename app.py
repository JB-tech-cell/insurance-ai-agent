import streamlit as st
import google.generativeai as genai

# 1. Page Configuration
st.set_page_config(page_title="Insurance Operations AI", page_icon="🛡️", layout="wide")

# 2. Sidebar Design
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2621/2621011.png", width=100)
st.sidebar.title("Jihad's InsurTech AI")
st.sidebar.markdown("---")
workflow = st.sidebar.radio(
    "Select Operation Workflow:",
    ("Life & Medical Underwriting", 
     "Medical Claims Auditing", 
     "Motor Claims Auditing", 
     "Life Claims Auditing (Death/TPD/ADB)")
)

# 3. Secure API Key Setup
API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('models/gemini-1.5-flash')

# 4. Main Interface
st.title("🛡️ AI Insurance Operations Assistant")
st.markdown("### Powered by Advanced Gen-Re & Swiss Re Guidelines")

with st.form("input_form"):
    if workflow == "Life & Medical Underwriting":
        st.subheader("📝 Applicant Data")
        col1, col2 = st.columns(2)
        age = col1.number_input("Age", min_value=18, max_value=80)
        coverage = col1.number_input("Coverage Amount ($)", min_value=10000)
        occupation = col2.text_input("Occupation")
        income = col2.number_input("Annual Income ($)", min_value=1000)
        medical_history = st.text_area("Medical History (BMI, BP, Blood Sugar, Family History)")
        
        prompt_data = f"Underwriting Request: Age {age}, Coverage ${coverage}, Occupation: {occupation}, Income ${income}. Medical: {medical_history}"

    elif workflow == "Medical Claims Auditing":
        st.subheader("🏥 Medical Claim Data")
        diagnosis = st.text_input("Diagnosis (ICD-10)")
        procedures = st.text_area("Billed Procedures & Hospital Stay Details")
        
        prompt_data = f"Medical Claim Audit: Diagnosis: {diagnosis}. Billed Items: {procedures}"

    elif workflow == "Motor Claims Auditing":
        st.subheader("🚗 Motor Claim Data")
        accident_report = st.text_area("Police / Accident Report Narrative")
        surveyor_report = st.text_area("Surveyor Repair Request & Damages")
        
        prompt_data = f"Motor Claim Audit: Accident Narrative: {accident_report}. Claimed Damages: {surveyor_report}"

    else:
        st.subheader("⚖️ Life Claim Data (Death/TPD/ADB)")
        claim_type = st.selectbox("Claim Type", ["Death", "TPD", "PPD", "ADB", "Passive War Risk"])
        claim_details = st.text_area("Claim Details & Medical/Police Reports")
        
        prompt_data = f"Life Claim Audit ({claim_type}): Details: {claim_details}"

    submitted = st.form_submit_button("Analyze & Generate Report 🚀")

# 5. Process & Generate Report
if submitted:
    with st.spinner("Analyzing data based on global reinsurance guidelines..."):
        system_instruction = """
        Act as an Expert Insurance Operations Assistant following Swiss Re/Gen-Re guidelines.
        Analyze the provided data based on the requested workflow. Highlight RED FLAGS clearly.
        Format the output as a professional executive report.
        """
        
        response = model.generate_content(system_instruction + "\n\nData:\n" + prompt_data)
        
        st.success("✅ Analysis Complete!")
        st.markdown("---")
        st.markdown("### 📊 Executive AI Report")
        st.write(response.text)
        
        st.download_button(
            label="Download Report as TXT",
            data=response.text,
            file_name="AI_Insurance_Report.txt",
            mime="text/plain"
        )
