# 🧠 Infographic Generation Pipeline (LangChain + Gemini)

A modular **multi-agent AI pipeline** that generates structured infographic concepts from textual articles.  
It leverages **LangChain** for agent orchestration and **Google Gemini models** for reasoning, design mapping, and evaluation, all containerized through Docker for easy deployment.

---

## ✨ Features

- **Fine-Tuned Article Agent:** Extracts key themes, facts, and data points from any article using Gemini-Pro.
- **Infographics Agent:** Designs structured infographic layouts (charts, flows, or icons) using Gemini-Pro-Vision.
- **Merger Agent:** Combines textual analysis and design structure into a unified output.
- **Evaluator Agent:** Reviews infographic clarity, readability, and visual hierarchy.
- **Dockerized Setup:** Fully portable environment for local or cloud execution.

---

## 🧩 Project Structure

nfographic_pipeline/
│
├── agents/
│ ├── fine_tuned_article_agent.py
│ ├── infographics_agent.py
│ ├── merger_agent.py
│ └── evaluator_agent.py
│
├── pipeline.py
├── run_pipeline.py
├── requirements.txt
└── Dockerfile

---

## ⚙️ Setup & Installation

### 1. Clone Repository

git clone https://github.com/sharanraj-n/infographic-pipeline.git
cd infographic-pipeline

### 2. Create Environment

python -m venv venv
source venv/bin/activate # use venv\Scripts\activate on Windows

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Set Google Gemini API Key
Create a `.env` file and add:

GOOGLE_API_KEY=your_google_ai_studio_key_here

---

## 🐳 Running with Docker

### Build Docker Image

docker build -t langchain-gemini-pipeline .

### Execute Container

docker run --rm -e GOOGLE_API_KEY=<your_google_key_here> langchain-gemini-pipeline

---

## 🧪 Example Usage (inside container)

from infographic_pipeline.pipeline import InfographicPipeline

pipeline = InfographicPipeline()
article = "AI-driven infographic generation streamlines data storytelling through automation and analytics."
result = pipeline.run(article)

print(result["evaluation"])


---

## 🪄 Expected Output
A JSON structure summarizing:
- Extracted key points and statistics  
- Recommended visual design specification  
- Combined layout metadata  
- Evaluation report with readability and design feedback  

Example snippet:

{
"readability_score": 8.7,
"data_accuracy": true,
"design_feedback": "Excellent hierarchy and balanced composition."
}


---

## 🧰 Tech Stack

| Component        | Technology Used                     |
|------------------|-------------------------------------|
| Language Models  | Google Gemini-Pro / Gemini-Pro-Vision |
| Framework        | LangChain (LLMChain architecture)   |
| Environment      | Python 3.11                         |
| Containerization | Docker                              |
| Config Management| python-dotenv                       |

---

## 🚀 Future Enhancements
- Integrate Canva/Adobe API for live infographic generation  
- Add memory persistence using LangGraph or ChromaDB  
- Enable streaming evaluation for large document sets  

---

## 🧑‍💻 Author
Developed by **Team Stark**, 2025  
Designed for intelligent, multi-agent workflow automation using LangChain and Gemini.
