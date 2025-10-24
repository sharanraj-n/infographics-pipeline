import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .robust_json import robust_json_extract

class InfographicsAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0.3
        )
        
        self.prompt = PromptTemplate.from_template(
            """
            Given the structured infographic data below, suggest:
            - visual layout
            - infographic type(s)
            - color/font recommendations
            
            Output as pure JSON only.
            Data: {content_data}
            """
        )
    
    def generate_design_spec(self, content_data: dict):
        chain = self.prompt | self.llm
        response = chain.invoke({"content_data": json.dumps(content_data)})
        text = getattr(response, "content", str(response))
        print("RAW LLM OUTPUT (infographics agent):", text)
        return robust_json_extract(text)
