import streamlit as st
import os
import tempfile
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_community.document_loaders import PyPDFLoader

# 1. Environment variables load karo
load_dotenv()

# 2. Page ka setup
st.set_page_config(page_title="AI Resume Screener", page_icon="📄", layout="wide")
st.title("📄 AI Resume Screener & Job Matcher")
st.markdown("Upload a Resume and paste the Job Description to see how well the candidate fits.")

# 3. UI Layout (2 Columns)
col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Job Description (JD)")
    job_description = st.text_area("Paste the Job Description here:", height=300, placeholder="We are looking for a Python Developer...")

with col2:
    st.subheader("2. Upload Resume")
    uploaded_file = st.file_uploader("Upload a PDF Resume", type=["pdf"])

# 4. Analyze Button
if st.button("Analyze Resume 🚀", use_container_width=True):
    if uploaded_file is None or not job_description.strip():
        st.warning("Please upload a PDF and provide a Job Description first.")
    else:
        with st.spinner("AI is reading the resume and matching it with JD..."):
            try:
                # PDF ko temporarily save karo taake LangChain padh sake
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
                    tmp_file.write(uploaded_file.getvalue())
                    tmp_file_path = tmp_file.name

                # Load PDF
                loader = PyPDFLoader(tmp_file_path)
                resume_docs = loader.load()
                resume_text = "\n".join([doc.page_content for doc in resume_docs])

                # LLM Setup (Groq)
                llm = ChatGroq(model="openai/gpt-oss-20b", temperature=0, groq_api_key=os.getenv("GROQ_API_KEY"))

                # Prompt Template
                prompt = ChatPromptTemplate.from_template("""
                You are an expert HR Manager. Compare the following Resume with the Job Description.
                Provide the output strictly in JSON format with the following keys:
                - "match_score": (integer 0 to 100)
                - "matched_skills": (list of strings)
                - "missing_skills": (list of strings)
                - "summary": (short string explaining why the candidate is a good or bad fit)

                Job Description:
                {job_description}

                Resume:
                {resume_text}
                """)

                # Output Parser
                parser = JsonOutputParser()

                # LangChain Pipeline (LCEL)
                chain = prompt | llm | parser

                # Run Chain
                result = chain.invoke({
                    "job_description": job_description,
                    "resume_text": resume_text
                })

                # Clean up temp file
                os.remove(tmp_file_path)

                # --- Result Display UI ---
                st.success("Analysis Complete!")
                st.divider()

                # Score Display (Bada aur clear)
                score = result.get("match_score", 0)
                st.markdown(f"### Match Score: **{score}/100**")
                st.progress(score / 100)

                # Skills Display (2 Columns)
                res_col1, res_col2 = st.columns(2)
                
                with res_col1:
                    st.markdown("#### ✅ Matched Skills")
                    for skill in result.get("matched_skills", []):
                        st.write(f"- {skill}")
                        
                with res_col2:
                    st.markdown("#### ❌ Missing Skills")
                    for skill in result.get("missing_skills", []):
                        st.write(f"- {skill}")

                # Summary Display
                st.markdown("#### 📝 AI Summary")
                st.info(result.get("summary", "No summary generated."))

            except Exception as e:
                st.error(f"An error occurred: {e}")