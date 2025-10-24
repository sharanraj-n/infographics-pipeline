from .agents.fine_tuned_article_agent import FineTunedArticleAgent
from .agents.infographics_agent import InfographicsAgent
from .agents.merger_agent import MergerAgent
from .agents.evaluator_agent import EvaluatorAgent

class InfographicPipeline:
    def __init__(self):
        self.article_agent = FineTunedArticleAgent()
        self.infographics_agent = InfographicsAgent()
        self.merger_agent = MergerAgent()
        self.evaluator_agent = EvaluatorAgent()

    def run(self, article_text: str):
        key_points = self.article_agent.extract_key_points(article_text)
        design_spec = self.infographics_agent.generate_design_spec(key_points)
        merged = self.merger_agent.merge(key_points, design_spec)
        evaluation = self.evaluator_agent.evaluate(merged)
        return {
            "structured_data": key_points,
            "visual_spec": design_spec,
            "final_design": merged,
            "evaluation": evaluation
        }
