📄 AI Resume Screener
I built this small project to automate the most boring part of hiring: reading hundreds of resumes.

Instead of manually checking if a candidate matches the job, you just upload a PDF resume, paste the Job Description, and let the AI do the matching. It saves a lot of time.

What it does:
Takes a PDF resume and a Job Description as input.

Gives a Match Score out of 100.

Tells you exactly which skills are matched and which are missing.

Provides a quick AI summary of why the candidate is a good fit.

How I built it:
I used Streamlit to make the UI so I didn't have to write HTML/CSS.
For the backend, I used LangChain to chain the prompt, the LLM (Groq API), and the output.

One cool thing I learned here: I used LangChain's JsonOutputParser. So instead of getting a messy paragraph from the AI, I get clean JSON data. This made it super easy to show the skills as bullet points and the score as a progress bar on the UI.

How to run this locally:
Clone the repo and go into the folder.

Install the packages:

bash
pip install streamlit langchain langchain-groq pypdf python-dotenv
Create a .env file in the main folder and add your Groq API key:

env
GROQ_API_KEY=your_api_key_here
Start the app:

bash
streamlit run app.py
Built by Waseem Saleem
