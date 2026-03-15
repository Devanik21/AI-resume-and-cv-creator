# AI Resume And CV Creator

![Language](https://img.shields.io/badge/Language-Python-3776AB?style=flat-square) ![Stars](https://img.shields.io/github/stars/Devanik21/AI-resume-and-cv-creator?style=flat-square&color=yellow) ![Forks](https://img.shields.io/github/forks/Devanik21/AI-resume-and-cv-creator?style=flat-square&color=blue) ![Author](https://img.shields.io/badge/Author-Devanik21-black?style=flat-square&logo=github) ![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=flat-square)

> AI-powered resume and CV creation — ATS-optimised, professionally structured, and tailored to specific job descriptions in minutes.

---

**Topics:** `ats-optimization` · `career-ai` · `content-generation` · `deep-learning` · `generative-ai` · `large-language-models` · `natural-language-processing` · `nlp` · `resume-builder` · `text-generation`

## Overview

This application is a comprehensive AI resume builder that transforms raw career information into polished, ATS (Applicant Tracking System) optimised resume documents. It addresses one of the most practically valuable applications of LLMs: turning structured career data into the compelling, keyword-rich professional language that modern recruitment pipelines and human reviewers both expect.

The workflow begins with structured section-by-section input: professional summary, work experience (role, company, dates, key achievements), education, skills, certifications, and projects. Each section is individually processed by the LLM with a specialised prompt that emphasises quantified achievements (revenue impact, performance improvements, team size), strong action verbs, and industry-specific terminology appropriate to the user's field.

The job description tailoring feature is particularly powerful: paste the target job description and the application analyses it for required skills, preferred qualifications, and company-specific keywords, then rewrites the resume to maximise keyword overlap with the JD — increasing ATS pass rates without misrepresenting the candidate's actual experience. A keyword match score (0–100%) is computed and displayed for transparency.

---

## Motivation

Resume writing is a skill that blocks qualified candidates from opportunities they deserve. The difference between a 40% and 80% ATS keyword match can be the difference between an interview and a rejection — not because the candidate is underqualified, but because their resume wasn't written in the specific language the JD uses. This tool levels that playing field.

---

## Architecture

```
User Input (sections: summary, experience, skills, education)
        │
  Optional: Job Description paste
        │
  LLM Processing (GPT-4o / Gemini):
  ├── Section enhancement (quantify, action verbs)
  ├── JD keyword extraction (NLP)
  └── Resume rewrite with keyword injection
        │
  ATS keyword match score computation
        │
  Template rendering (Modern/Classic/Technical)
        │
  PDF export (ReportLab) + DOCX export (python-docx)
```

---

## Features

### Section-by-Section AI Generation
Each resume section (Summary, Experience, Skills, Education, Projects) is enhanced by a specialised LLM prompt focused on that section's specific conventions and goals.

### JD-Targeted Optimisation
Paste any job description; the app extracts required skills and preferred qualifications, then rewrites the resume to maximise keyword alignment with an ATS keyword match score (0–100%).

### Quantified Achievement Enhancement
The LLM identifies vague impact statements ('improved performance', 'helped customers') and rewrites them with specific, plausible quantification prompts for the user to fill in.

### Multiple Resume Templates
Four professionally designed templates: Modern (clean sans-serif), Classic (traditional serif), Technical (developer-focused, GitHub/links prominent), and Creative (bold headers, accent colour).

### Cover Letter Generator
Generate a tailored cover letter for the same target job, matching the tone and keywords of the JD while highlighting the candidate's most relevant experience.

### LinkedIn Summary Generator
Convert the resume summary section into an optimised LinkedIn 'About' section in the first-person tone that LinkedIn's algorithm and recruiters prefer.

### PDF and DOCX Export
Professional PDF output via ReportLab with correct typography and margins; DOCX output via python-docx for easy editing in Microsoft Word after download.

### Version History
Save multiple resume versions (one per target role) with JD metadata, allowing quick recall and comparison across job applications.

---

## Tech Stack

| Library / Tool | Role | Why This Choice |
|---|---|---|
| **Streamlit** | Application UI | Multi-section form, preview panel, sidebar |
| **OpenAI GPT-4o / Gemini** | Content generation | Section enhancement, JD analysis, keyword injection |
| **ReportLab** | PDF generation | Precise layout, fonts, margins, multi-column templates |
| **python-docx** | DOCX export | Word document generation with styles |
| **spaCy (optional)** | NLP keyword extraction | JD skill and qualification extraction |
| **pandas** | Version history | CSV-based resume version storage |

> **Key packages detected in this repo:** `streamlit` · `requests` · `google-generativeai` · `PyPDF2` · `python-docx` · `pandas` · `odfpy`

---

## Getting Started

### Prerequisites

- Python 3.9+ (or Node.js 18+ for TypeScript/JS projects)
- `pip` or `npm` package manager
- Relevant API keys (see Configuration section)

### Installation

```bash
git clone https://github.com/Devanik21/AI-resume-and-cv-creator.git
cd AI-resume-and-cv-creator
python -m venv venv && source venv/bin/activate
pip install streamlit openai google-generativeai reportlab python-docx pandas
echo 'OPENAI_API_KEY=sk-...' > .env
streamlit run app.py
```

---

## Usage

```bash
# Launch app
streamlit run app.py

# CLI resume generation
python generate_resume.py \
  --input career_data.json \
  --jd job_description.txt \
  --template modern \
  --output resume.pdf
```

---

## Configuration

| Variable | Default | Description |
|---|---|---|
| `OPENAI_API_KEY` | `(required)` | OpenAI API key for GPT-4o generation |
| `GOOGLE_API_KEY` | `(optional)` | Google API key for Gemini backend |
| `DEFAULT_TEMPLATE` | `modern` | Resume template: modern, classic, technical, creative |
| `MAX_PAGES` | `2` | Maximum resume pages (1 or 2) |
| `COVER_LETTER` | `True` | Enable cover letter generation tab |

> Copy `.env.example` to `.env` and populate all required values before running.

---

## Project Structure

```
AI-resume-and-cv-creator/
├── README.md
├── requirements.txt
├── app.py
└── ...
```

---

## Roadmap

- [ ] LinkedIn profile import via API for zero-friction onboarding
- [ ] Interview question prediction based on the resume + JD pair
- [ ] Salary range estimation using job title, location, and experience data
- [ ] Multi-language resume generation (English, French, German, Hindi)
- [ ] Recruiter feedback simulation: A/B test resume versions against a simulated recruiter LLM

---

## Contributing

Contributions, issues, and feature requests are welcome. Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'feat: add your feature'`)
4. Push to your branch (`git push origin feature/your-feature`)
5. Open a Pull Request

Please follow conventional commit messages and ensure any new code is documented.

---

## Notes

LLM-generated content should be reviewed and edited by the user before submission. The tool enhances and structures career information provided; it does not fabricate experience. Always verify that quantified achievements accurately reflect your actual performance.

---

## Author

**Devanik Debnath**  
B.Tech, Electronics & Communication Engineering  
National Institute of Technology Agartala

[![GitHub](https://img.shields.io/badge/GitHub-Devanik21-black?style=flat-square&logo=github)](https://github.com/Devanik21)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-devanik-blue?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/devanik/)

---

## License

This project is open source and available under the [MIT License](LICENSE).

---

*Crafted with curiosity, precision, and a belief that good software is worth building well.*
