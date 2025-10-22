from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

class InfographicsAgent:
    """Generates infographic design blueprint using Gemini."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro-vision", temperature=0.3)
        self.prompt = PromptTemplate.from_template(
            """
            Given the structured data below, design an infographic layout specification.
            Include:
            - Type of visuals (charts, timelines, etc.)
            - Color scheme suggestion
            - Font and composition hierarchy
            - Export format direction (Canva, Adobe, JSON)
            
            Data: {content_data}
            Provide JSON response.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def generate_design_spec(self, content_data: dict):
        response = self.chain.invoke({"content_data": json.dumps(content_data)})
        try:
            return json.loads(response["text"])
        except Exception:
            return {"error": "Design spec parsing failed"}
