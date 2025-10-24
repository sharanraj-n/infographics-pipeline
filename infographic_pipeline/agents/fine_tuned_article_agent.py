import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from .robust_json import robust_json_extract

class FineTunedArticleAgent:
    def __init__(self):
        # Use API key from environment variable
        api_key = os.getenv("GOOGLE_GENAI_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_GENAI_API_KEY not found in environment variables")
        
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=api_key,
            temperature=0.4
        )
        
        self.prompt = PromptTemplate.from_template(
            """
            Extract infographic structure from this article:
            Article: {article_text}

            Output as pure JSON:
            - main_points: list of strings
            - supporting_data: list of objects with keys "metric" (string) and "value" (number)
            - summary: string
            - visual_suggestions: simple list of strings ("bar chart", "timeline", etc.)
            
            Never include text outside JSON!
            """
        )
    
    def extract_key_points(self, article_text: str):
        chain = self.prompt | self.llm
        response = chain.invoke({"article_text": article_text})
        text = getattr(response, "content", str(response))
        print("RAW LLM OUTPUT (article agent):", text)
        return robust_json_extract(text)
