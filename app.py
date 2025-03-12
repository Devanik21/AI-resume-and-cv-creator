import streamlit as st
import google.generativeai as genai
import pandas as pd
from io import StringIO
import json
import re
from datetime import datetime
import uuid

# Configure the Streamlit page
st.set_page_config(
    page_title="Advanced AI Resume & Cover Letter Generator",
    page_icon="📄",
    layout="wide",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #074f61;
        }
        .stTextInput>div>div>input, .stSelectbox>div>div {
            background-color: #074f61;
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
        .custom-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 20px;
        }
        .feedback-box {
            padding: 10px;
            border-radius: 5px;
            margin: 10px 0;
        }
        .high-match {
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
        }
        .medium-match {
            background-color: #fff3cd;
            border: 1px solid #ffeeba;
        }
        .low-match {
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize session state for history tracking
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
    nav_option = st.radio("", ["Create Resume & Cover Letter", "Profile Manager", "History", "ATS Optimizer"])
    
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
    st.title("📄 Advanced AI Resume & Cover Letter Generator")
    st.write("Generate a professional resume and tailored cover letter with ATS optimization")
    
    # Create tabs for different sections
    tab1, tab2, tab3 = st.tabs(["Personal Info", "Job Details", "Generate & Export"])
    
    with tab1:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("## 📝 Personal Information")
        
        # Two-column layout for personal info
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("👤 Full Name:", key="name")
            email = st.text_input("✉️ Email Address:", key="email")
            phone = st.text_input("📞 Phone Number:", key="phone")
            linkedin = st.text_input("🔗 LinkedIn Profile:", key="linkedin")
            portfolio = st.text_input("🌐 Portfolio/Website (Optional):", key="portfolio")
        
        with col2:
            location = st.text_input("📍 Location:", key="location")
            headline = st.text_input("💫 Professional Headline:", key="headline", 
                              help="A brief statement summarizing your professional identity")
            objective = st.text_area("🎯 Career Objective:", key="objective", height=123)
        
        st.markdown("## 💼 Professional Experience")
        experience = st.text_area("Describe your work experience in detail:", key="experience", height=150,
                           help="Include company names, positions, dates, and key achievements")
        
        st.markdown("## 🛠️ Skills & Expertise")
        skills = st.text_area("List your technical and soft skills:", key="skills", height=100)
        
        st.markdown("## 🎓 Education & Certifications")
        col1, col2 = st.columns(2)
        with col1:
            education = st.text_area("Education Details:", key="education", height=100)
        with col2:
            certifications = st.text_area("Certifications (Optional):", key="certifications", height=100)
            
        # Save profile option
        st.markdown("## 💾 Save Your Profile")
        profile_name = st.text_input("Profile Name:", key="profile_name")
        if st.button("Save Current Profile") and profile_name:
            profile_data = {
                "name": name, "email": email, "phone": phone, "linkedin": linkedin,
                "portfolio": portfolio, "location": location, "headline": headline,
                "objective": objective, "experience": experience, "skills": skills,
                "education": education, "certifications": certifications
            }
            st.session_state.saved_profiles[profile_name] = profile_data
            st.success(f"Profile '{profile_name}' saved successfully!")
        st.markdown('</div>', unsafe_allow_html=True)
            
    with tab2:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("## 🏢 Job Details")
        
        job_title = st.text_input("🔍 Job Title:", key="job_title")
        company = st.text_input("🏢 Company Name:", key="company")
        
        st.markdown("### 📋 Job Description")
        job_description = st.text_area("Paste the complete job description here:", key="job_description", height=250)
        
        st.markdown("### 🎛️ Advanced Options")
        resume_format = st.selectbox("Resume Format:", 
                               ["Chronological", "Functional", "Combination", "Targeted"], key="resume_format")
        
        tone = st.select_slider("Cover Letter Tone:", 
                          options=["Formal", "Professional", "Balanced", "Conversational"], 
                          value="Professional", key="tone")
        
        # Option to upload company research or additional info
        st.markdown("### 📚 Additional Information (Optional)")
        company_research = st.text_area("Company Research or Additional Context:", key="company_research", height=100,
                                 help="Add any research about the company culture, values, or specific projects")
        
        # Option to upload resume for improvement
        st.markdown("### 📤 Upload Existing Resume (Optional)")
        uploaded_resume = st.file_uploader("Upload your current resume for improvement:", type=['txt', 'pdf', 'docx'])
        st.markdown('</div>', unsafe_allow_html=True)
        
    with tab3:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown("## 🚀 Generate Your Documents")
        
        generate_options = st.multiselect("Select what to generate:", 
                                    ["Resume", "Cover Letter", "ATS Optimization Analysis"], 
                                    default=["Resume", "Cover Letter"])
        
        if st.button("🚀 Generate Selected Documents"):
            if not api_key:
                st.warning("⚠️ Please enter a valid Google Gemini API Key in the sidebar.")
            elif not name or not experience or not skills or not job_description:
                st.warning("⚠️ Please fill in all required fields in the Personal Info and Job Details tabs.")
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
                                    f"Optimize this resume specifically for the following job description: {job_description}\n"
                                    f"Format the resume in Markdown with clear sections and bullet points. Ensure it highlights relevant skills and experience for the job.")
                    
                    cover_letter_prompt = (f"Generate a {tone.lower()} tone cover letter for {name} applying for the position of {job_title} at {company}.\n"
                                         f"Include details about:\nExperience: {experience}\nSkills: {skills}\nEducation: {education}\n"
                                         f"Tailor this cover letter specifically to match this job description: {job_description}\n"
                                         f"Additional company context: {company_research}\n"
                                         f"Make the cover letter compelling, concise, and highlight the candidate's value proposition.")
                    
                    ats_analysis_prompt = (f"Analyze how well this candidate's profile matches the job description and provide an ATS optimization analysis:\n"
                                        f"Candidate Profile:\nName: {name}\nHeadline: {headline}\nExperience: {experience}\n"
                                        f"Skills: {skills}\nEducation: {education}\nCertifications: {certifications}\n\n"
                                        f"Job Description: {job_description}\n\n"
                                        f"Provide: 1) A match percentage, 2) Top 5 keywords missing from the profile, "
                                        f"3) Specific suggestions to improve ATS compatibility, 4) Strengths in the current profile")
                    
                    # Generate responses
                    with st.spinner("🔄 Creating your documents..."):
                        results = {}
                        
                        if "Resume" in generate_options:
                            resume_response = model.generate_content(resume_prompt)
                            results["resume"] = resume_response.text
                            
                        if "Cover Letter" in generate_options:
                            cover_letter_response = model.generate_content(cover_letter_prompt)
                            results["cover_letter"] = cover_letter_response.text
                            
                        if "ATS Optimization Analysis" in generate_options:
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
                        st.markdown("### 🔍 ATS Optimization Analysis")
                        
                        # Extract match percentage using regex
                        match_text = results["ats_analysis"]
                        match_percentage = re.search(r'(\d+)%', match_text)
                        if match_percentage:
                            match_value = int(match_percentage.group(1))
                            # Create a visual indicator of match strength
                            if match_value >= 80:
                                st.markdown(f'<div class="feedback-box high-match">Match Score: {match_value}% - Strong Match</div>', unsafe_allow_html=True)
                            elif match_value >= 60:
                                st.markdown(f'<div class="feedback-box medium-match">Match Score: {match_value}% - Good Match</div>', unsafe_allow_html=True)
                            else:
                                st.markdown(f'<div class="feedback-box low-match">Match Score: {match_value}% - Needs Improvement</div>', unsafe_allow_html=True)
                        
                        st.markdown(results["ats_analysis"])
                    
                    # Export options
                    st.markdown("### 📥 Export Options")
                    export_format = st.selectbox("Export Format:", ["Text File", "JSON", "Markdown"])
                    
                    if st.button("Export Documents"):
                        if export_format == "Text File":
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
                    st.info("If you're having issues, try using a different model like 'gemini-1.5-pro'.")
        st.markdown('</div>', unsafe_allow_html=True)

elif nav_option == "Profile Manager":
    st.title("👤 Profile Manager")
    
    if not st.session_state.saved_profiles:
        st.info("You don't have any saved profiles yet. Create a profile in the Resume & Cover Letter tab.")
    else:
        st.markdown("### 📋 Your Saved Profiles")
        profile_to_view = st.selectbox("Select a profile to view or edit:", list(st.session_state.saved_profiles.keys()))
        
        if profile_to_view:
            profile_data = st.session_state.saved_profiles[profile_to_view]
            
            st.markdown('<div class="custom-card">', unsafe_allow_html=True)
            st.markdown(f"## Profile: {profile_to_view}")
            
            # Display and allow editing of profile data
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
                    st.success(f"Profile '{profile_to_view}' updated successfully!")
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
            st.markdown('</div>', unsafe_allow_html=True)

elif nav_option == "History":
    st.title("📜 Generation History")
    
    if not st.session_state.history:
        st.info("No generation history available. Generate a resume or cover letter first.")
    else:
        history_items = st.session_state.history
        history_items.reverse()  # Show most recent first
        
        for idx, item in enumerate(history_items):
            with st.expander(f"{item['timestamp']} - {item['job_title']} at {item['company']}"):
                results = item["results"]
                
                # Display documents in tabs
                if results:
                    doc_tabs = st.tabs(["Resume", "Cover Letter", "ATS Analysis"])
                    
                    with doc_tabs[0]:
                        if "resume" in results:
                            st.markdown(results["resume"])
                        else:
                            st.info("No resume was generated for this entry.")
                            
                    with doc_tabs[1]:
                        if "cover_letter" in results:
                            st.markdown(results["cover_letter"])
                        else:
                            st.info("No cover letter was generated for this entry.")
                            
                    with doc_tabs[2]:
                        if "ats_analysis" in results:
                            st.markdown(results["ats_analysis"])
                        else:
                            st.info("No ATS analysis was generated for this entry.")
                
                # Delete option
                if st.button(f"Delete Entry", key=f"del_{idx}"):
                    st.session_state.history.remove(item)
                    st.success("History entry deleted!")
                    st.rerun()

elif nav_option == "ATS Optimizer":
    st.title("🎯 ATS Optimizer")
    st.write("Analyze your resume against a job description to improve ATS compatibility")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📄 Your Resume")
        resume_text = st.text_area("Paste your current resume text:", height=300)
        
    with col2:
        st.markdown("### 📋 Job Description")
        job_desc = st.text_area("Paste the job description:", height=300)
    
    if st.button("🔍 Analyze ATS Compatibility") and api_key:
        if not resume_text or not job_desc:
            st.warning("Please provide both your resume and the job description.")
        else:
            try:
                # Configure API
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")
                
                ats_prompt = (f"Perform a detailed ATS (Applicant Tracking System) compatibility analysis:\n\n"
                            f"RESUME:\n{resume_text}\n\n"
                            f"JOB DESCRIPTION:\n{job_desc}\n\n"
                            f"Provide the following analysis:\n"
                            f"1. Overall match score (percentage)\n"
                            f"2. Keyword analysis (which important keywords are present/missing)\n"
                            f"3. Specific recommendations to improve ATS compatibility\n"
                            f"4. Strengths of the current resume\n"
                            f"5. Suggested resume modifications with examples\n")
                
                with st.spinner("Analyzing your resume..."):
                    ats_response = model.generate_content(ats_prompt)
                    analysis = ats_response.text
                
                # Extract match percentage using regex
                match_percentage = re.search(r'(\d+)%', analysis)
                if match_percentage:
                    match_value = int(match_percentage.group(1))
                    # Create a progress bar for the match score
                    st.markdown("### Match Score")
                    st.progress(match_value/100)
                    
                    # Add color-coded feedback
                    if match_value >= 80:
                        st.markdown(f'<div class="feedback-box high-match">Score: {match_value}% - Strong Match</div>', unsafe_allow_html=True)
                    elif match_value >= 60:
                        st.markdown(f'<div class="feedback-box medium-match">Score: {match_value}% - Good Match</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="feedback-box low-match">Score: {match_value}% - Needs Improvement</div>', unsafe_allow_html=True)
                
                # Display full analysis
                st.markdown("### 📊 Detailed Analysis")
                st.markdown(analysis)
                
                # Option to generate an optimized version
                if st.button("✨ Generate Optimized Resume"):
                    optimize_prompt = (f"Based on this resume:\n{resume_text}\n\n"
                                    f"And this job description:\n{job_desc}\n\n"
                                    f"Generate a fully optimized version of the resume for ATS compatibility. "
                                    f"Keep the same basic information but reorganize, rephrase, and enhance "
                                    f"to maximize keyword matching and relevance. Format in Markdown.")
                    
                    with st.spinner("Generating optimized resume..."):
                        optimized_response = model.generate_content(optimize_prompt)
                        optimized_resume = optimized_response.text
                    
                    st.markdown("### ✅ Optimized Resume")
                    st.markdown(optimized_resume)
                    
                    # Download option
                    st.download_button(
                        label="Download Optimized Resume",
                        data=optimized_resume,
                        file_name="optimized_resume.md",
                        mime="text/markdown"
                    )
            
            except Exception as e:
                st.error(f"❌ Error: {e}")
