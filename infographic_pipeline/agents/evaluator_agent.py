import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .robust_json import robust_json_extract

class EvaluatorAgent:
    def __init__(self):
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0
        )
        
        self.prompt = PromptTemplate.from_template(
            """
            Evaluate this infographic design JSON for:
            - readability_score: 0-10
            - data_accuracy: 0-10
            - design_feedback: string
            
            Output as pure JSON only.
            Layout: {final_design}
            """
        )
    
    def evaluate(self, final_design):
        chain = self.prompt | self.llm
        response = chain.invoke({"final_design": json.dumps(final_design)})
        text = getattr(response, "content", str(response))
        print("RAW LLM OUTPUT (evaluator agent):", text)
        return robust_json_extract(text)
