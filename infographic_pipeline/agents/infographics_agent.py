"""
Agent for turning structured content into infographic layout/design specs.
Uses Gemini and robust JSON extraction.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from infographic_pipeline.agents.robust_json import robust_json_extract
import json

class InfographicsAgent:
    def __init__(self):
        # Lower temperature for more deterministic layout instructions
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.3)
        self.prompt = PromptTemplate.from_template(
            """
            Given the structured data below, design an infographic layout specification.
            Include:
            - Type of visuals (charts, timelines, etc.)
            - Color scheme suggestion
            - Font and composition hierarchy
            - Export format direction (Canva, Adobe, JSON)
            
            Data: {content_data}
            Return your answer as a single JSON object and nothing else.
            """
        )

    def generate_design_spec(self, content_data: dict):
        """
        Runs Gemini on structured content to generate infographic design spec.
        Returns: dict (parsed model output)
        """
        chain = self.prompt | self.llm
        response = chain.invoke({"content_data": json.dumps(content_data)})
        text = getattr(response, "content", str(response))
        print("RAW LLM OUTPUT (infographics agent):", text)
        return robust_json_extract(text)
