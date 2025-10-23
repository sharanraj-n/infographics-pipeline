"""
Agent for evaluating infographic design based on layout/content.
Prompts Gemini to return a simple structured dict with review feedback.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from infographic_pipeline.agents.robust_json import robust_json_extract
import json

class EvaluatorAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash-lite", temperature=0)
        self.prompt = PromptTemplate.from_template(
            """
            Evaluate the infographic design for:
            - Visual clarity
            - Data accuracy
            - Balance and hierarchy
            - Readability score

            Input JSON: {final_design}
            Return your answer as a single JSON object and nothing else.
            Keys must be: readability_score, data_accuracy, design_feedback.
            """
        )

    def evaluate(self, final_design):
        """
        Runs Gemini to evaluate a merged infographic design.
        Returns: dict (parsed model output)
        """
        chain = self.prompt | self.llm
        response = chain.invoke({"final_design": json.dumps(final_design)})
        text = getattr(response, "content", str(response))
        print("RAW LLM OUTPUT (evaluator agent):", text)
        return robust_json_extract(text)
