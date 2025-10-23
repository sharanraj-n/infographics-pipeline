import os
from dotenv import load_dotenv
from infographic_pipeline.pipeline import InfographicPipeline
from infographic_pipeline.utils.exporter import InfographicExporter

if __name__ == "__main__":
    load_dotenv()
    article_name = "solar_capacity"  # <-- set this per article!
    article_text = """
    India’s solar power capacity has reached 70GW in 2025, up from 35GW in 2022, according to the MNRE. This rapid expansion, aided by declining costs and government incentives, is projected to continue with an estimated 100GW goal by 2027. Key factors include abundant sunlight, adoption in rural areas, and large-scale solar parks. Challenges remain, such as grid integration and storage, but experts see India poised as a solar leader.
    """

    # Run pipeline
    pipeline = InfographicPipeline()
    result = pipeline.run(article_text)
    print("RESULT DUMP:", result)

    # Export all: images, html, pdf (files named with article_name)
    exporter = InfographicExporter(article_name=article_name)
    exporter.export_all(result)
