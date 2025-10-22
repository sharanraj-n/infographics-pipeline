from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import json

class EvaluatorAgent:
    """Evaluates infographic clarity and correctness."""

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(model="gemini-pro", temperature=0)
        self.prompt = PromptTemplate.from_template(
            """
            Evaluate the infographic design for:
            - Visual clarity
            - Data accuracy
            - Balance and hierarchy
            - Readability score
            
            Input JSON: {final_design}
            Return evaluation as JSON.
            """
        )
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt)

    def evaluate(self, final_design):
        response = self.chain.invoke({"final_design": json.dumps(final_design)})
        try:
            return json.loads(response["text"])
        except Exception:
            return {"error": "Evaluation parsing failed"}
