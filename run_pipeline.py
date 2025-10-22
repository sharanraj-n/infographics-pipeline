import os
from dotenv import load_dotenv
from infographic_pipeline.pipeline import InfographicPipeline

load_dotenv()

if __name__ == "__main__":
    article_text = (
        "AI-driven infographic generation streamlines data storytelling using visual automation."
    )
    pipeline = InfographicPipeline()
    result = pipeline.run(article_text)
    print("Evaluation:")
    print(result["evaluation"])
