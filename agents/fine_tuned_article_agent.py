from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

class FineTunedArticleAgent:
    """Processes and analyzes the article using Gemini."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0.4)
        self.prompt = PromptTemplate.from_template(
            """
            Analyze the article below and extract:
            1. Core themes
            2. Important statistics or data points
            3. Main insights and supporting ideas
            4. Suggestions for visual representation (charts, icons, flow diagrams)
            
            Article: {article_text}
            Return structured JSON output.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def extract_key_points(self, article_text: str):
        response = self.chain.invoke({"article_text": article_text})
        try:
            return json.loads(response["text"])
        except Exception:
            return {"error": "Invalid JSON from model"}

