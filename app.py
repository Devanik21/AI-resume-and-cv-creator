import streamlit as st
import google.generativeai as genai
import pandas as pd
import json
import re
from datetime import datetime
import uuid

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
        .stTextInput>div>div>input, .stSelectbox>div>div {
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
            box-shadow: 0px 5px 15px rgba(0, 0, 139, 0.2);
        }
        .feedback-box {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .high-match { background-color: #d4edda; border: 1px solid #c3e6cb; }
        .medium-match { background-color: #fff3cd; border: 1px solid #ffeeba; }
        .low-match { background-color: #f8d7da; border: 1px solid #f5c6cb; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'saved_profiles' not in st.session_state:
    st.session_state.saved_profiles = {}
if 'current_id' not in st.session_state:
    st.session_state.current_id = None

# Sidebar for API Key and Navigation
with st.sidebar:
    st.markdown("### 🔑 API Configuration")
    api_key = st.text_input("Enter Google Gemini API Key:", type="password")
    
    st.markdown("---")
    st.markdown("### 📋 Navigation")
    nav_options = ["Create Resume & Cover Letter", "Profile Manager", "History", "ATS Optimizer"]
    nav_option = st.selectbox("", options=nav_options, index=0)
    
    st.markdown("---")
    st.markdown("### 💾 Saved Profiles")
    if st.session_state.saved_profiles:
        selected_profile = st.selectbox("Load Profile:", list(st.session_state.saved_profiles.keys()))
        if st.button("Load Selected Profile"):
            profile_data = st.session_state.saved_profiles[selected_profile]
            for key, value in profile_data.items():
                if key in st.session_state:
                    st.session_state[key] = value
            st.success(f"Loaded profile: {selected_profile}")

# Main content area
if nav_option == "Create Resume & Cover Letter":
    st.title("📄 AI Resume & Cover Letter Generator")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Personal Info", "Job Details", "Generate & Export"])
    
    with tab1:
        st.markdown("## 📝 Personal Information")
        
        # Two-column layout for personal info
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name:", key="name")
            email = st.text_input("✉️ Email:", key="email")
            phone = st.text_input("📞 Phone:", key="phone")
            linkedin = st.text_input("🔗 LinkedIn:", key="linkedin")
        
        with col2:
            location = st.text_input("📍 Location:", key="location")
            headline = st.text_input("💫 Professional Headline:", key="headline")
            portfolio = st.text_input("🌐 Portfolio (Optional):", key="portfolio")
            objective = st.text_area("🎯 Career Objective:", key="objective", height=100)
        
        st.markdown("## 💼 Professional Experience")
        experience = st.text_area("Describe your work experience:", key="experience", height=150)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("## 🛠️ Skills")
            skills = st.text_area("List your skills:", key="skills", height=100)
        
        with col2:
            st.markdown("## 🎓 Education")
            education = st.text_area("Education Details:", key="education", height=100)
            certifications = st.text_area("Certifications (Optional):", key="certifications", height=100)
            
        # Save profile option
        profile_name = st.text_input("Profile Name:", key="profile_name")
        if st.button("Save Profile") and profile_name:
            profile_data = {
                "name": name, "email": email, "phone": phone, "linkedin": linkedin,
                "portfolio": portfolio, "location": location, "headline": headline,
                "objective": objective, "experience": experience, "skills": skills,
                "education": education, "certifications": certifications
            }
            st.session_state.saved_profiles[profile_name] = profile_data
            st.success(f"Profile '{profile_name}' saved!")
            
    with tab2:
        st.markdown("## 🏢 Job Details")
        
        job_title = st.text_input("🔍 Job Title:", key="job_title")
        company = st.text_input("🏢 Company Name:", key="company")
        
        st.markdown("### 📋 Job Description")
        job_description = st.text_area("Paste the job description:", key="job_description", height=250)
        
        col1, col2 = st.columns(2)
        with col1:
            resume_format = st.selectbox("Resume Format:", 
                               ["Chronological", "Functional", "Combination", "Targeted"], key="resume_format")
        
        with col2:
            tone = st.selectbox("Cover Letter Tone:", 
                          options=["Formal", "Professional", "Balanced", "Conversational"], 
                          index=1, key="tone")
        
        st.markdown("### 📚 Additional Information (Optional)")
        company_research = st.text_area("Company Research:", key="company_research", height=100)
        
        uploaded_resume = st.file_uploader("Upload current resume (Optional):", type=['txt', 'pdf', 'docx'])
        
    with tab3:
        st.markdown("## 🚀 Generate Your Documents")
        
        generate_options = st.multiselect("Select what to generate:", 
                                    ["Resume", "Cover Letter", "ATS Analysis"], 
                                    default=["Resume", "Cover Letter"])
        
        if st.button("🚀 Generate Documents"):
            if not api_key:
                st.warning("⚠️ Please enter a valid Google Gemini API Key.")
            elif not name or not experience or not skills or not job_description:
                st.warning("⚠️ Please fill in all required fields.")
            else:
                try:
                    # Configure API
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.0-flash")
                    
                    # Create prompts
                    resume_prompt = (f"Generate a professional {resume_format} resume for {name} with the following details:\n"
                                    f"Headline: {headline}\nEmail: {email}\nPhone: {phone}\nLocation: {location}\n"
                                    f"LinkedIn: {linkedin}\nPortfolio: {portfolio}\nObjective: {objective}\n"
                                    f"Experience: {experience}\nSkills: {skills}\nEducation: {education}\n"
                                    f"Certifications: {certifications}\n\n"
                                    f"Optimize for this job description: {job_description}\n"
                                    f"Format in Markdown with clear sections and bullet points.")
                    
                    cover_letter_prompt = (f"Generate a {tone.lower()} tone cover letter for {name} applying for {job_title} at {company}.\n"
                                         f"Include details about:\nExperience: {experience}\nSkills: {skills}\nEducation: {education}\n"
                                         f"Tailor to this job description: {job_description}\n"
                                         f"Additional company context: {company_research}")
                    
                    ats_analysis_prompt = (f"Analyze how well this candidate's profile matches the job description:\n"
                                        f"Candidate Profile:\nName: {name}\nHeadline: {headline}\nExperience: {experience}\n"
                                        f"Skills: {skills}\nEducation: {education}\nCertifications: {certifications}\n\n"
                                        f"Job Description: {job_description}\n\n"
                                        f"Provide: 1) Match percentage, 2) Top 5 keywords missing from profile, "
                                        f"3) Specific suggestions to improve ATS compatibility, 4) Profile strengths")
                    
                    # Generate responses
                    with st.spinner("🔄 Creating documents..."):
                        results = {}
                        
                        if "Resume" in generate_options:
                            resume_response = model.generate_content(resume_prompt)
                            results["resume"] = resume_response.text
                            
                        if "Cover Letter" in generate_options:
                            cover_letter_response = model.generate_content(cover_letter_prompt)
                            results["cover_letter"] = cover_letter_response.text
                            
                        if "ATS Analysis" in generate_options:
                            ats_response = model.generate_content(ats_analysis_prompt)
                            results["ats_analysis"] = ats_response.text
                            
                        # Save to history
                        history_entry = {
                            "id": str(uuid.uuid4()),
                            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "job_title": job_title,
                            "company": company,
                            "results": results
                        }
                        st.session_state.history.append(history_entry)
                        st.session_state.current_id = history_entry["id"]
                    
                    # Display results
                    if "resume" in results:
                        st.markdown("### ✅ Generated Resume")
                        st.markdown(results["resume"])
                        
                    if "cover_letter" in results:
                        st.markdown("### ✅ Generated Cover Letter")
                        st.markdown(results["cover_letter"])
                        
                    if "ats_analysis" in results:
                        st.markdown("### 🔍 ATS Analysis")
                        
                        # Extract match percentage using regex
                        match_text = results["ats_analysis"]
                        match_percentage = re.search(r'(\d+)%', match_text)
                        if match_percentage:
                            match_value = int(match_percentage.group(1))
                            if match_value >= 80:
                                st.markdown(f'<div class="feedback-box high-match">Match: {match_value}% - Strong</div>', unsafe_allow_html=True)
                            elif match_value >= 60:
                                st.markdown(f'<div class="feedback-box medium-match">Match: {match_value}% - Good</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="feedback-box low-match">Match: {match_value}% - Needs Improvement</div>', unsafe_allow_html=True)
                        
                        st.markdown(results["ats_analysis"])
                    
                    # Export options
                    st.markdown("### 📥 Export Options")
                    export_format = st.selectbox("Export Format:", ["Text", "JSON", "Markdown"])
                    
                    if st.button("Export Documents"):
                        if export_format == "Text":
                            export_text = ""
                            for doc_type, content in results.items():
                                export_text += f"--- {doc_type.upper()} ---\n\n{content}\n\n"
                            st.download_button(
                                label="Download as Text",
                                data=export_text,
                                file_name=f"{name.replace(' ', '_')}_documents.txt",
                                mime="text/plain"
                            )
                        elif export_format == "JSON":
                            export_json = json.dumps(results, indent=2)
                            st.download_button(
                                label="Download as JSON",
                                data=export_json,
                                file_name=f"{name.replace(' ', '_')}_documents.json",
                                mime="application/json"
                            )
                        else:  # Markdown
                            export_md = ""
                            for doc_type, content in results.items():
                                export_md += f"# {doc_type.upper()}\n\n{content}\n\n"
                            st.download_button(
                                label="Download as Markdown",
                                data=export_md,
                                file_name=f"{name.replace(' ', '_')}_documents.md",
                                mime="text/markdown"
                            )
                
                except Exception as e:
                    st.error(f"❌ Error: {e}")
                    st.info("Try using a different model like 'gemini-1.5-pro'.")

elif nav_option == "Profile Manager":
    st.title("👤 Profile Manager")
    
    if not st.session_state.saved_profiles:
        st.info("No saved profiles yet. Create one in the Resume & Cover Letter tab.")
    else:
        profile_to_view = st.selectbox("Select profile to edit:", list(st.session_state.saved_profiles.keys()))
        
        if profile_to_view:
            profile_data = st.session_state.saved_profiles[profile_to_view]
            st.markdown(f"## Profile: {profile_to_view}")
            
            edited_profile = {}
            col1, col2 = st.columns(2)
            
            with col1:
                edited_profile["name"] = st.text_input("Full Name:", value=profile_data.get("name", ""))
                edited_profile["email"] = st.text_input("Email:", value=profile_data.get("email", ""))
                edited_profile["phone"] = st.text_input("Phone:", value=profile_data.get("phone", ""))
                edited_profile["linkedin"] = st.text_input("LinkedIn:", value=profile_data.get("linkedin", ""))
                
            with col2:
                edited_profile["location"] = st.text_input("Location:", value=profile_data.get("location", ""))
                edited_profile["headline"] = st.text_input("Headline:", value=profile_data.get("headline", ""))
                edited_profile["portfolio"] = st.text_input("Portfolio:", value=profile_data.get("portfolio", ""))
                
            edited_profile["objective"] = st.text_area("Objective:", value=profile_data.get("objective", ""), height=100)
            edited_profile["experience"] = st.text_area("Experience:", value=profile_data.get("experience", ""), height=150)
            edited_profile["skills"] = st.text_area("Skills:", value=profile_data.get("skills", ""), height=100)
            
            col1, col2 = st.columns(2)
            with col1:
                edited_profile["education"] = st.text_area("Education:", value=profile_data.get("education", ""), height=100)
            with col2:
                edited_profile["certifications"] = st.text_area("Certifications:", value=profile_data.get("certifications", ""), height=100)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("Update Profile"):
                    st.session_state.saved_profiles[profile_to_view] = edited_profile
                    st.success(f"Profile '{profile_to_view}' updated!")
            with col2:
                new_name = st.text_input("New Profile Name:")
                if st.button("Save As New") and new_name:
                    st.session_state.saved_profiles[new_name] = edited_profile
                    st.success(f"Profile saved as '{new_name}'!")
            with col3:
                if st.button("Delete Profile"):
                    del st.session_state.saved_profiles[profile_to_view]
                    st.success(f"Profile '{profile_to_view}' deleted!")
                    st.rerun()

elif nav_option == "History":
    st.title("📜 Generation History")
    
    if not st.session_state.history:
        st.info("No generation history available.")
    else:
        history_items = st.session_state.history.copy()
        history_items.reverse()  # Show most recent first
        
        for idx, item in enumerate(history_items):
            with st.expander(f"{item['timestamp']} - {item['job_title']} at {item['company']}"):
                results = item["results"]
                
                if results:
                    doc_tabs = st.tabs(["Resume", "Cover Letter", "ATS Analysis"])
                    
                    with doc_tabs[0]:
                        if "resume" in results:
                            st.markdown(results["resume"])
                        else:
                            st.info("No resume was generated.")
                            
                    with doc_tabs[1]:
                        if "cover_letter" in results:
                            st.markdown(results["cover_letter"])
                        else:
                            st.info("No cover letter was generated.")
                            
                    with doc_tabs[2]:
                        if "ats_analysis" in results:
                            st.markdown(results["ats_analysis"])
                        else:
                            st.info("No ATS analysis was generated.")
                
                if st.button(f"Delete Entry", key=f"del_{idx}"):
                    st.session_state.history.remove(item)
                    st.success("History entry deleted!")
                    st.rerun()

elif nav_option == "ATS Optimizer":  
    """
    ATS Optimizer Module for Resume Analysis and Optimization
    
    Enhanced file upload and parsing capabilities for multiple file types.
    """

    st.title("🎯 ATS Optimizer")  
      
    col1, col2 = st.columns(2)  
      
    with col1:  
        st.markdown("### 📄 Your Resume")  
        resume_text = st.text_area("Paste your current resume text:", height=300)  
        
        # Enhanced file uploader with more file types
        uploaded_resume = st.file_uploader("Or upload your resume:", 
            type=["txt", "pdf", "docx", "doc", "rtf", "odt", "md"],
            help="Supported formats: TXT, PDF, DOCX, DOC, RTF, ODT, Markdown"
        )
          
    with col2:  
        st.markdown("### 📋 Job Description")  
        job_desc = st.text_area("Paste the job description:", height=300)  
        uploaded_csv = st.file_uploader("Or upload a job description file:", 
            type=["csv", "txt", "xlsx", "xls", "ods"],
            help="Supported formats: CSV, TXT, XLSX, XLS, ODS"
        )
      
    def extract_text_from_file(uploaded_file):
        """
        Extract text from various file types with robust error handling.
        """
        try:
            # PDF extraction
            if uploaded_file.type == "application/pdf":
                import PyPDF2
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                return "\n".join([page.extract_text() for page in pdf_reader.pages if page.extract_text()])
            
            # DOCX extraction
            elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                import docx
                doc = docx.Document(uploaded_file)
                return "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            # DOC extraction (requires additional library)
            elif uploaded_file.type in ["application/msword", "application/doc", "application/ms-doc"]:
                import olefile
                import win32com.client
                word = win32com.client.Dispatch("Word.Application")
                doc = word.Documents.Open(uploaded_file)
                text = doc.Content.Text
                doc.Close()
                word.Quit()
                return text
            
            # RTF extraction
            elif uploaded_file.type == "application/rtf":
                import striprtf
                rtf_text = uploaded_file.getvalue().decode("utf-8")
                return striprtf.rtf_to_text(rtf_text)
            
            # ODT extraction
            elif uploaded_file.type == "application/vnd.oasis.opendocument.text":
                import zipfile
                import xml.etree.ElementTree as ET
                with zipfile.ZipFile(uploaded_file) as zf:
                    xml_content = zf.read('content.xml')
                    tree = ET.fromstring(xml_content)
                    return " ".join(tree.itertext())
            
            # Markdown and Text files
            elif uploaded_file.type in ["text/markdown", "text/plain"]:
                return uploaded_file.getvalue().decode("utf-8")
            
            # Spreadsheet file handling for job descriptions
            elif uploaded_file.type in ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                                        "application/vnd.ms-excel", 
                                        "application/vnd.oasis.opendocument.spreadsheet"]:
                import pandas as pd
                
                # Try multiple libraries for robust parsing
                try:
                    # First try pandas
                    df = pd.read_excel(uploaded_file)
                except ImportError:
                    # Fallback to openpyxl
                    import openpyxl
                    wb = openpyxl.load_workbook(uploaded_file)
                    sheet = wb.active
                    df = pd.DataFrame(sheet.values)
                
                # Combine all text from first few columns
                return " ".join(df.iloc[:, :3].astype(str).values.flatten())
            
            # CSV file
            elif uploaded_file.type == "text/csv":
                import pandas as pd
                df = pd.read_csv(uploaded_file)
                return " ".join(df.iloc[:, 0].astype(str).tolist())
            
            else:
                st.warning(f"Unsupported file type: {uploaded_file.type}")
                return ""
        
        except Exception as e:
            st.error(f"Error extracting text from file: {e}")
            return ""
    
    if st.button("🔍 Analyze ATS Compatibility") and api_key:  
        """
        Enhanced ATS compatibility analysis with robust file handling.
        """
        
        if not resume_text and not uploaded_resume:  
            st.warning("Please provide either a resume text or upload a resume file.")  
        elif not job_desc and not uploaded_csv:  
            st.warning("Please provide either a job description or upload a job description file.")  
        else:  
            try:  
                # Extract text from uploaded resume
                if uploaded_resume:  
                    resume_text = extract_text_from_file(uploaded_resume) or resume_text
                  
                # Extract job description from uploaded file
                if uploaded_csv:  
                    job_desc = extract_text_from_file(uploaded_csv) or job_desc
                
                # Rest of the existing ATS analysis logic remains the same...
                # (Previous AI analysis and optimization code)
                
            except Exception as e:  
                st.error(f"❌ Error: {e}")
