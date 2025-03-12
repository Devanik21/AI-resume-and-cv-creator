import streamlit as st
import google.generativeai as genai

# Configure the Streamlit page
st.set_page_config(
    page_title="AI Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #eef2f3;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div {
            background-color: #ffffff;
            border-radius: 10px;
            padding: 8px;
            font-weight: bold;
        }
        .stButton>button {
            background: linear-gradient(to right, #4facfe, #00f2fe);
            color: white;
            font-weight: bold;
            border-radius: 10px;
            padding: 10px 20px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar for API Key
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")

# Page Header
st.title("📄 AI Resume & Cover Letter Generator")
st.write("Generate a professional resume and tailored cover letter based on job descriptions!")

# Input fields
st.markdown("## 📝 Enter Your Details")
name = st.text_input("👤 Full Name:")
email = st.text_input("✉️ Email Address:")
phone = st.text_input("📞 Phone Number:")
experience = st.text_area("💼 Work Experience (Summarized):")
skills = st.text_area("🛠️ Key Skills:")
education = st.text_area("🎓 Education:")
certifications = st.text_area("📜 Certifications (Optional):")

# Job Description Input
st.markdown("## 🏢 Job Description")
job_title = st.text_input("🔍 Job Title:")
company = st.text_input("🏢 Company Name:")
job_description = st.text_area("📋 Paste Job Description Here:")

# Generate button
if st.button("🚀 Generate Resume & Cover Letter"):
    if not api_key:
        st.warning("⚠️ Please enter a valid Google Gemini API Key in the sidebar.")
    else:
        try:
            # Configure API
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash")

            # Create prompts for resume and cover letter
            resume_prompt = (f"Generate a professional resume for {name} with the following details:\n"
                             f"Email: {email}\nPhone: {phone}\nExperience: {experience}\n"
                             f"Skills: {skills}\nEducation: {education}\nCertifications: {certifications}")

            cover_letter_prompt = (f"Generate a cover letter for {name} applying for the position of {job_title} at {company}.\n"
                                   f"Include details about experience: {experience}, skills: {skills}, and align it with the job description:\n"
                                   f"{job_description}")

            # Generate responses
            with st.spinner("🔄 Creating your resume and cover letter..."):
                resume_response = model.generate_content(resume_prompt)
                cover_letter_response = model.generate_content(cover_letter_prompt)

            # Display results
            st.success("✅ Generated Resume:")
            st.write(resume_response.text)
            
            st.success("✅ Generated Cover Letter:")
            st.write(cover_letter_response.text)

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.info("If you're having issues, try using a different model like 'gemini-1.5-pro'.")
