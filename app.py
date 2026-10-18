import streamlit as st
import google.generativeai as genai

st.title("🛠️ نظام الفحص الآلي (Diagnostic Mode)")

try:
    # جلب المفتاح
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    st.success("✅ تم قراءة المفتاح بنجاح من إعدادات Streamlit.")
    
    st.markdown("### أسماء النماذج المصرحة لهذا المفتاح (انسخ أحدها):")
    
    # جلب النماذج المتاحة
    models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    for m in models:
        st.code(m)
        
except Exception as e:
    st.error(f"❌ تفاصيل الخطأ: {e}")
