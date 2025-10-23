"""
InfographicExporter: Handles generation of charts, HTML, and PDF outputs
from pipeline result dictionary, naming files with a given article name.
Uses pdfkit for PDF export (requires 'wkhtmltopdf' installed system-wide).
"""

import os
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def safe_filename(name):
    """Convert article name to a safe filename (no spaces or special chars)."""
    return re.sub(r'\W+', '_', name.lower()).strip('_')

class InfographicExporter:
    def __init__(self, output_dir="generated", article_name="infographic"):
        self.output_dir = output_dir
        self.article_name = safe_filename(article_name)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def chart_path(self):
        return os.path.join(self.output_dir, f"{self.article_name}_chart.png")

    def html_path(self):
        return os.path.join(self.output_dir, f"{self.article_name}_infographic.html")

    def pdf_path(self):
        return os.path.join(self.output_dir, f"{self.article_name}_infographic.pdf")

    def create_chart(self, supporting_data):
        """
        Generates a bar chart from supporting_data if possible.
        Output: {output_dir}/{article_name}_chart.png
        If no usable data, uses hardcoded demo data for user validation.
        """
        chart_path = self.chart_path()
        metrics = []
        values = []

        # Use given data, or fallback demo-data for debugging/demo
        if not supporting_data or not isinstance(supporting_data, list) or not any(supporting_data):
            print("No supporting data for charting; will use demo values.")
            demo_data = [
                {'metric': 'Demo Metric 1', 'value': 40},
                {'metric': 'Demo Metric 2', 'value': 65}
            ]
            data_source = demo_data
        else:
            data_source = supporting_data

        for item in data_source:
            if isinstance(item, dict):
                metric = str(item.get('metric', ''))
                val = item.get('value', '')
            else:
                metric = str(item)
                val = item

            if isinstance(val, (int, float)):
                number = val
            else:
                match = re.search(r"([-+]?\d*\.?\d+)", str(val))
                if match:
                    number = float(match.group(0))
                else:
                    number = None

            if metric and (number is not None):
                metrics.append(metric)
                values.append(number)

        if metrics and values and any(x != 0 for x in values):
            plt.figure(figsize=(6,4))
            plt.bar(metrics, values, color='#4285F4')
            plt.title('Key Statistics')
            plt.ylabel('Value')
            plt.xticks(rotation=20, ha='right')
            plt.tight_layout()
            plt.savefig(chart_path)
            plt.close()
            if os.path.exists(chart_path):
                print(f"Chart image generated at: {chart_path}")
            else:
                print("Chart file NOT generated (unknown error).")
        else:
            print("Chart file NOT generated (no suitable numeric data).")

    def save_infographic_html(self, result):
        """
        Creates {article}_infographic.html, including a chart image and pipeline output info.
        Output: {output_dir}/{article_name}_infographic.html
        """
        sd = result.get("structured_data", {})
        supporting_data_html = ""
        for stat in sd.get('supporting_data', []):
            if isinstance(stat, dict):
                supporting_data_html += f"<li>{stat.get('metric', '')}: {stat.get('value', '')}</li>"
            else:
                supporting_data_html += f"<li>{stat}</li>"

        visuals_html = ""
        for v in sd.get('visual_suggestions', []):
            if isinstance(v, dict):
                visuals_html += f"<li>{v.get('type', str(v))}</li>"
            else:
                visuals_html += f"<li>{v}</li>"

        html_content = f"""
        <html>
          <head>
            <title>Infographic Output: {self.article_name}</title>
            <style>
              body {{ font-family: Arial; padding: 40px; background: #f8f9fa; }}
              h1 {{ color: #2c3e50; }}
              .section {{ background: #fff; padding: 20px; margin-bottom: 15px; border-radius: 8px; }}
            </style>
          </head>
          <body>
            <h1>Infographic: {self.article_name.replace('_', ' ').title()}</h1>
            <div class="section">
              <h2>Main Points</h2>
              <ul>
                {''.join([f"<li>{pt}</li>" for pt in sd.get('main_points', [])]) or "<li>None</li>"}
              </ul>
            </div>
            <div class="section">
              <h2>Key Statistics</h2>
              <ul>
                {supporting_data_html or "<li>None</li>"}
              </ul>
            </div>
            <div class="section chart">
              <img src="{os.path.basename(self.chart_path())}" alt="Key Statistics Chart" width="400"/>
            </div>
            <div class="section">
              <h2>Suggested Visuals</h2>
              <ul>
                {visuals_html or "<li>None</li>"}
              </ul>
            </div>
            <div class="section">
              <h2>Summary</h2>
              <p>{sd.get('summary', '') or "No summary available."}</p>
            </div>
          </body>
        </html>
        """
        html_path = self.html_path()
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        if os.path.exists(html_path):
            print(f"Infographic HTML generated at: {html_path}")
        else:
            print("HTML file NOT generated!")

    def save_pdf(self):
        """
        Converts HTML to PDF. Output: {output_dir}/{article_name}_infographic.pdf
        Uses pdfkit (requires 'wkhtmltopdf' installed system-wide).
        """
        try:
            import pdfkit
        except ImportError:
            print("pdfkit is not installed. Run 'pip install pdfkit'")
            return
        html_path = self.html_path()
        pdf_path = self.pdf_path()
        options = {"enable-local-file-access": None}
        if not os.path.exists(html_path):
            print("HTML file not found, cannot generate PDF.")
            return
        try:
            pdfkit.from_file(html_path, pdf_path, options=options)
            if os.path.exists(pdf_path):
                print(f"Infographic PDF generated at: {pdf_path}")
            else:
                print("PDF file NOT generated (unknown error).")
        except Exception as e:
            print(f"PDF generation error: {e}")

    def export_all(self, pipeline_result):
        """
        Calls all exporters: chart, HTML, PDF—naming each with the article.
        Gives debug output for each stage.
        """
        self.create_chart(pipeline_result.get('structured_data', {}).get('supporting_data', []))
        self.save_infographic_html(pipeline_result)
        self.save_pdf()
