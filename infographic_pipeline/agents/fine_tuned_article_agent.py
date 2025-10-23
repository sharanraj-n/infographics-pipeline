"""
Agent for extracting structured infographic info from the input article.
- Uses Google Gemini through LangChain.
- Forces a strictly-typed JSON output via prompt engineering.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from infographic_pipeline.agents.robust_json import robust_json_extract

class FineTunedArticleAgent:
    def __init__(self):
        # Set up Gemini LLM with reasonable temperature for info extraction
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0.4)
        # Prompt: Forces Gemini to always deliver keys in the right structure.
        self.prompt = PromptTemplate.from_template(
            """
            Analyze the article below and extract:
            1. Core themes (list of strings)
            2. Important statistics or data points (list of objects with keys: 'metric' (string), 'value' (number or string))
            3. Main insights and supporting ideas (string)
            4. Suggestions for visual representation (simple list of strings like "bar chart", "timeline", etc.)

            Article: {article_text}

            Return your answer as a single JSON object ONLY, with these keys:
            - main_points (list of strings)
            - supporting_data (list as above, always at least two items, never empty, never strings)
            - summary (string)
            - visual_suggestions (list of strings, never objects)

            Never include markdown, comments or extra explanations.
            """
        )

    def extract_key_points(self, article_text: str):
        """
        Runs the Gemini LLM chain on the article and extracts structured infographic content.
        Returns: dict (parsed model output)
        """
        chain = self.prompt | self.llm
        response = chain.invoke({"article_text": article_text})
        text = getattr(response, "content", str(response))
        print("RAW LLM OUTPUT (article agent):", text)
        return robust_json_extract(text)
