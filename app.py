import streamlit as st
import google.generativeai as genai
from fpdf import FPDF
import datetime

# 1. Page Configuration
st.set_page_config(page_title="Enterprise InsurTech AI", page_icon="🛡️", layout="wide")

# 2. Language Selection
language = st.sidebar.selectbox("🌐 Language / اللغة", ["English", "العربية"])

# Dictionary for localized text
if language == "العربية":
    t = {
        "sidebar_title": "نظام الذكاء الاصطناعي المؤسسي",
        "workflow_label": "اختر مسار العمل:",
        "wf_life_med": "اكتتاب الحياة والطبي",
        "wf_med_claim": "تدقيق المطالبات الطبية",
        "wf_motor_claim": "تدقيق مطالبات السيارات",
        "wf_life_claim": "تدقيق مطالبات الحياة (وفاة/عجز)",
        "main_title": "🛡️ نظام الذكاء الاصطناعي لاكتتاب التأمين والمطالبات",
        "main_sub": "### 📊 مدعوم بمعايير Gen-Re و Swiss Re العالمية",
        "sec_client": "#### 👤 بيانات العميل والبوليصة",
        "policy_no": "رقم البوليصة",
        "client_name": "اسم العميل",
        "age": "العمر",
        "coverage": "مبلغ التغطية ($)",
        "occupation": "المهنة",
        "income": "الدخل السنوي ($)",
        "sec_med": "#### 🏥 التقارير الطبية",
        "med_issuer": "الجهة المصدرة للتقارير",
        "med_history": "التاريخ الطبي (الوزن، الضغط، السكر، الخ)",
        "med_files": "تحميل التقارير الطبية",
        "sec_legal": "#### ⚖️ الثبوتيات القانونية",
        "id_source": "مصدر الثبوتيات (مثل: وزارة الداخلية)",
        "id_numbers": "أرقام الثبوتيات",
        "legal_files": "تحميل الأوراق القانونية",
        "btn_analyze": "تحليل وإصدار تقرير أكاديمي 🚀",
        "loading": "الذكاء الاصطناعي يقوم بتحليل السجلات وإصدار التقرير الرسمي...",
        "success": "✅ اكتمل التحليل وتم توثيق التقرير بنجاح!",
        "report_title": "### 📑 التقرير التنفيذي (بوليصة:",
        "error": "❌ لم يتمكن النظام من الاتصال بالخوادم.",
        "med_claim_sec": "🏥 بيانات المطالبة الطبية",
        "diagnosis": "التشخيص الطبي (ICD-10)",
        "procedures": "الإجراءات الطبية المفوترة وتفاصيل الإقامة",
        "motor_claim_sec": "🚗 بيانات مطالبة السيارات",
        "accident_rep": "تقرير الشرطة / وصف الحادث",
        "surveyor_rep": "تقرير الخبير والأضرار المطالب بها",
        "life_claim_sec": "⚖️ بيانات مطالبة الحياة",
        "claim_type": "نوع المطالبة",
        "claim_details": "تفاصيل المطالبة والتقارير المرفقة"
    }
else:
    t = {
        "sidebar_title": "Enterprise InsurTech AI",
        "workflow_label": "Select Operation Workflow:",
        "wf_life_med": "Life & Medical Underwriting",
        "wf_med_claim": "Medical Claims Auditing",
        "wf_motor_claim": "Motor Claims Auditing",
        "wf_life_claim": "Life Claims Auditing (Death/TPD/ADB)",
        "main_title": "🛡️ Enterprise AI Insurance Underwriting & Claims",
        "main_sub": "### 📊 Powered by Advanced Gen-Re & Swiss Re Guidelines",
        "sec_client": "#### 👤 Applicant & Policy Data",
        "policy_no": "Policy Number",
        "client_name": "Client Name",
        "age": "Age",
        "coverage": "Coverage Amount ($)",
        "occupation": "Occupation",
        "income": "Annual Income ($)",
        "sec_med": "#### 🏥 Medical Documentation",
        "med_issuer": "Medical Report Issuer",
        "med_history": "Medical History (BMI, BP, etc.)",
        "med_files": "Upload Medical Files",
        "sec_legal": "#### ⚖️ Legal Documentation",
        "id_source": "ID Source (e.g. Ministry of Interior)",
        "id_numbers": "ID Numbers",
        "legal_files": "Upload Legal Documents",
        "btn_analyze": "Analyze & Generate Academic Report 🚀",
        "loading": "AI is analyzing records and generating the official executive report...",
        "success": "✅ Analysis Complete & Officially Documented!",
        "report_title": "### 📑 AI Executive Report (Policy:",
        "error": "❌ Could not connect to servers.",
        "med_claim_sec": "🏥 Medical Claim Data",
        "diagnosis": "Diagnosis (ICD-10)",
        "procedures": "Billed Procedures & Hospital Stay Details",
        "motor_claim_sec": "🚗 Motor Claim Data",
        "accident_rep": "Police / Accident Report Narrative",
        "surveyor_rep": "Surveyor Repair Request & Damages",
        "life_claim_sec": "⚖️ Life Claim Data",
        "claim_type": "Claim Type",
        "claim_details": "Claim Details & Medical/Police Reports"
    }

# 3. Sidebar Design
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/2621/2621011.png", width=100)
st.sidebar.title(t["sidebar_title"])
st.sidebar.markdown("---")
workflow_selection = st.sidebar.radio(
    t["workflow_label"],
    (t["wf_life_med"], t["wf_med_claim"], t["wf_motor_claim"], t["wf_life_claim"])
)

API_KEY = st.secrets["GEMINI_API_KEY"] 
genai.configure(api_key=API_KEY)

def create_pdf(report_text, policy, client, workflow_type):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="AI Insurance Operations - Executive Report", ln=True, align='C')
    pdf.set_font("Arial", 'I', 11)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    pdf.cell(200, 8, txt=f"Date: {date_str} | Workflow: {workflow_type}", ln=True, align='C')
    
    # Safe encoding for PDF generator
    safe_client = client.encode('latin-1', 'replace').decode('latin-1')
    pdf.cell(200, 8, txt=f"Client: {safe_client} | Policy No: {policy}", ln=True, align='C')
    pdf.line(10, 35, 200, 35)
    pdf.ln(10)
    pdf.set_font("Arial", size=11)
    clean_text = report_text.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 7, txt=clean_text)
    return pdf.output(dest='S').encode('latin-1')

# 4. Main Interface
st.title(t["main_title"])
st.markdown(t["main_sub"])

policy_no = "N/A"
client_name = "N/A"
prompt_data = ""

with st.form("input_form"):
    if workflow_selection == t["wf_life_med"]:
        st.markdown(t["sec_client"])
        col1, col2 = st.columns(2)
        policy_no = col1.text_input(t["policy_no"])
        client_name = col2.text_input(t["client_name"])
        age = col1.number_input(t["age"], min_value=18, max_value=80)
        coverage = col2.number_input(t["coverage"], min_value=10000)
        occupation = col1.text_input(t["occupation"])
        income = col2.number_input(t["income"], min_value=1000)

        st.markdown("---")
        st.markdown(t["sec_med"])
        col3, col4 = st.columns(2)
        medical_issuer = col3.text_input(t["med_issuer"])
        medical_history = col4.text_area(t["med_history"])
        medical_files = st.file_uploader(t["med_files"], accept_multiple_files=True)

        st.markdown("---")
        st.markdown(t["sec_legal"])
        col5, col6 = st.columns(2)
        id_source = col5.text_input(t["id_source"])
        id_numbers = col6.text_input(t["id_numbers"])
        legal_files = st.file_uploader(t["legal_files"], accept_multiple_files=True)

        prompt_data = f"Underwriting Request. Policy: {policy_no}, Client: {client_name}, Age: {age}, Coverage: ${coverage}, Occupation: {occupation}, Income: ${income}. Medical Issuer: {medical_issuer}, History: {medical_history}. ID Source: {id_source}, ID Nos: {id_numbers}."

    elif workflow_selection == t["wf_med_claim"]:
        st.subheader(t["med_claim_sec"])
        diagnosis = st.text_input(t["diagnosis"])
        procedures = st.text_area(t["procedures"])
        prompt_data = f"Medical Claim Audit: Diagnosis: {diagnosis}. Billed Items: {procedures}"

    elif workflow_selection == t["wf_motor_claim"]:
        st.subheader(t["motor_claim_sec"])
        accident_report = st.text_area(t["accident_rep"])
        surveyor_report = st.text_area(t["surveyor_rep"])
        prompt_data = f"Motor Claim Audit: Accident Narrative: {accident_report}. Claimed Damages: {surveyor_report}"

    else:
        st.subheader(t["life_claim_sec"])
        claim_type = st.selectbox(t["claim_type"], ["Death", "TPD", "PPD", "ADB", "Passive War Risk"])
        claim_details = st.text_area(t["claim_details"])
        prompt_data = f"Life Claim Audit ({claim_type}): Details: {claim_details}"

    submitted = st.form_submit_button(t["btn_analyze"])

# 5. AI Engine
if submitted:
    with st.spinner(t["loading"]):
        lang_instruction = "Must output the report entirely in Arabic language." if language == "العربية" else "Must output the report entirely in English language."
        system_instruction = f"Act as an Expert Insurance Operations Assistant following Swiss Re/Gen-Re guidelines. Analyze the data. Highlight RED FLAGS clearly. Present the output in a highly structured, academic, professional, and easy-to-read format with bullet points. {lang_instruction}"
        full_prompt = system_instruction + "\n\nData:\n" + prompt_data
        
        try:
            models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            success = False
            report_text = ""
            
            for m_name in models:
                try:
                    model = genai.GenerativeModel(m_name)
                    response = model.generate_content(full_prompt)
                    report_text = response.text
                    success = True
                    break
                except Exception:
                    continue
            
            if success:
                st.success(t["success"])
                st.markdown("---")
                st.markdown(f"{t['report_title']} {policy_no})")
                st.write(report_text)
                
                col_dl1, col_dl2 = st.columns(2)
                
                col_dl1.download_button(
                    label="📄 Download Report (TXT)",
                    data=report_text,
                    file_name=f"Report_{policy_no}.txt",
                    mime="text/plain"
                )
                
                pdf_bytes = create_pdf(report_text, policy_no, client_name, workflow_selection)
                col_dl2.download_button(
                    label="📄 Download Report (PDF)",
                    data=pdf_bytes,
                    file_name=f"Report_{policy_no}.pdf",
                    mime="application/pdf"
                )
            else:
                st.error(t["error"])
        except Exception as e:
            st.error(f"Error: {e}")
