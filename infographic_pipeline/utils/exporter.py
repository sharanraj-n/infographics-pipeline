import os
import re
from datetime import datetime

import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for servers/containers
import matplotlib.pyplot as plt


def safe_filename(name: str) -> str:
    """Convert article name to a filesystem-safe filename."""
    return re.sub(r'\W+', '_', name.lower()).strip('_')


class InfographicExporter:
    def __init__(self, output_dir: str = "generated", article_name: str = "infographic"):
        self.output_dir = output_dir
        self.article_name = safe_filename(article_name)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def chart_path(self) -> str:
        return os.path.join(self.output_dir, f"{self.article_name}_chart.png")

    def html_path(self) -> str:
        return os.path.join(self.output_dir, f"{self.article_name}_infographic.html")

    def pdf_path(self) -> str:
        return os.path.join(self.output_dir, f"{self.article_name}_infographic.pdf")

    def _timestamp(self) -> str:
        return datetime.now().strftime("%B %d, %Y at %I:%M %p")

    def create_chart(self, supporting_data):
        """
        Build a bar chart from supporting_data and save as PNG.
        supporting_data may be list[dict(metric, value)] or list[str] with numbers.
        Falls back to demo data when not available.
        """
        chart_path = self.chart_path()
        print(f"[Exporter] Creating chart at: {chart_path}")

        metrics, values = [], []

        # Select data source
        if not supporting_data or not isinstance(supporting_data, list) or not any(supporting_data):
            print("[Exporter] No supporting data for chart; using demo chart.")
            data_source = [
                {"metric": "Demo Metric 1", "value": 40},
                {"metric": "Demo Metric 2", "value": 65},
            ]
        else:
            data_source = supporting_data

        # Parse values
        for item in data_source:
            if isinstance(item, dict):
                metric = str(item.get("metric", "")).strip()
                val = item.get("value", "")
            else:
                metric = str(item).strip()
                val = item

            # Extract numeric value
            if isinstance(val, (int, float)):
                number = float(val)
            else:
                m = re.search(r"([-+]?\d*\.?\d+)", str(val))
                number = float(m.group(0)) if m else None

            if metric and (number is not None):
                metrics.append(metric)
                values.append(number)

        print(f"[Exporter] Chart data -> Metrics: {metrics}, Values: {values}")

        # Always produce a chart, even if minimal
        if not metrics or not values:
            metrics = ["No Data"]
            values = [1.0]

        try:
            plt.figure(figsize=(10, 6))
            bars = plt.bar(metrics, values, color="#667eea", alpha=0.9, edgecolor="#4c5fd7", linewidth=1.5)

            plt.title("Key Statistics", fontsize=16, fontweight="bold", color="#333", pad=16)
            plt.ylabel("Value", fontsize=12, color="#555")
            plt.xlabel("Metrics", fontsize=12, color="#555")
            plt.xticks(rotation=45, ha="right", fontsize=10)
            plt.yticks(fontsize=10)

            ymax = max(values) if values else 1.0
            offset = max(0.01 * ymax, 0.25)

            for bar, val in zip(bars, values):
                h = bar.get_height()
                plt.text(
                    bar.get_x() + bar.get_width() / 2,
                    h + offset,
                    f"{val:g}",
                    ha="center",
                    va="bottom",
                    fontsize=10,
                    fontweight="bold",
                    color="#333",
                )

            plt.grid(axis="y", alpha=0.25, linestyle="--")
            ax = plt.gca()
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_color("#ddd")
            ax.spines["bottom"].set_color("#ddd")

            plt.tight_layout()
            plt.savefig(chart_path, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
            plt.close()

            if os.path.exists(chart_path):
                print(f"[Exporter] Chart generated: {chart_path} ({os.path.getsize(chart_path)} bytes)")
            else:
                print(f"[Exporter] Chart missing after save: {chart_path}")
        except Exception as e:
            print(f"[Exporter] Chart generation error: {e}")

    def save_infographic_html(self, result: dict):
        """
        Render a styled infographic HTML file based on the pipeline result.
        References the chart via /generated/<filename>.
        """
        sd = result.get("structured_data", {}) or {}

        # Build statistics cards
        supporting_data_html = ""
        for stat in sd.get("supporting_data", []) or []:
            if isinstance(stat, dict):
                metric = str(stat.get("metric", ""))
                value = str(stat.get("value", ""))
                supporting_data_html += f"""
                    <div class="stat-card">
                        <div class="stat-value">{value}</div>
                        <div class="stat-label">{metric}</div>
                    </div>
                """
            else:
                supporting_data_html += f"""
                    <div class="stat-card">
                        <div class="stat-value">{stat}</div>
                        <div class="stat-label"></div>
                    </div>
                """

        # Visual suggestions
        visuals_html = ""
        for v in sd.get("visual_suggestions", []) or []:
            visual_text = v if not isinstance(v, dict) else v.get("type", str(v))
            visuals_html += f'<span class="badge">{visual_text}</span>'

        # Main points
        main_points_html = ""
        for idx, pt in enumerate(sd.get("main_points", []) or [], 1):
            main_points_html += f"""
                <div class="point-card">
                    <div class="point-number">{idx}</div>
                    <div class="point-text">{pt}</div>
                </div>
            """

        chart_filename = f"{self.article_name}_chart.png"
        article_title = self.article_name.replace("_", " ").title()
        summary_text = sd.get("summary", "") or "No summary available."
        timestamp = self._timestamp()

        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Infographic: {article_title}</title>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        padding: 40px 20px;
        color: #333;
    }}
    .container {{ max-width: 1200px; margin: 0 auto; }}
    .header {{
        text-align: center; color: white; margin-bottom: 40px; animation: fadeInDown 0.8s ease;
    }}
    .header h1 {{
        font-size: 3rem; font-weight: 700; margin-bottom: 10px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }}
    .header .subtitle {{ font-size: 1.1rem; opacity: 0.9; }}

    .card {{
        background: white; border-radius: 20px; padding: 40px; margin-bottom: 30px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3); animation: fadeInUp 0.6s ease;
    }}
    .section-title {{
        font-size: 2rem; font-weight: 700; margin-bottom: 25px; color: #667eea;
        display: flex; align-items: center; gap: 15px;
    }}
    .section-title::before {{
        content: ""; width: 5px; height: 40px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 3px;
    }}

    /* Points */
    .points-grid {{ display: grid; gap: 20px; }}
    .point-card {{
        display: flex; align-items: flex-start; gap: 20px; padding: 20px;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 15px; transition: all 0.3s ease;
    }}
    .point-card:hover {{ transform: translateX(10px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
    .point-number {{
        flex-shrink: 0; width: 50px; height: 50px; border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
        display: flex; align-items: center; justify-content: center; font-size: 1.4rem; font-weight: 700;
    }}
    .point-text {{ flex: 1; font-size: 1.05rem; line-height: 1.6; }}

    /* Statistics */
    .stats-grid {{
        display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
        gap: 25px;
    }}
    .stat-card {{
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;
        padding: 28px; border-radius: 15px; text-align: center; transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102,126,234,0.3);
    }}
    .stat-card:hover {{ transform: translateY(-5px); box-shadow: 0 10px 25px rgba(102,126,234,0.5); }}
    .stat-value {{ font-size: 2.2rem; font-weight: 800; margin-bottom: 8px; }}
    .stat-label {{ font-size: 0.98rem; opacity: 0.95; }}

    /* Chart */
    .chart-container {{
        text-align: center; padding: 20px; background: #f8f9fa; border-radius: 15px;
    }}
    .chart-container img {{
        max-width: 100%; height: auto; border-radius: 10px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }}

    /* Visual Suggestions */
    .badges-container {{ display: flex; flex-wrap: wrap; gap: 12px; }}
    .badge {{
        display: inline-block; padding: 10px 18px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white; border-radius: 25px; font-size: 0.95rem; font-weight: 600; transition: all 0.3s ease;
    }}
    .badge:hover {{ transform: translateY(-2px); box-shadow: 0 6px 16px rgba(102,126,234,0.5); }}

    /* Summary */
    .summary-box {{
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 28px; border-radius: 15px; border-left: 6px solid #667eea;
        font-size: 1.07rem; line-height: 1.8; color: #555;
    }}

    /* Footer */
    .footer {{ text-align: center; color: white; margin-top: 40px; padding: 10px; opacity: 0.95; }}
    .footer a {{ color: white; text-decoration: none; font-weight: 600; }}

    /* Empty state */
    .empty-state {{ text-align: center; color: #999; font-style: italic; padding: 16px; }}

    /* Animations */
    @keyframes fadeInDown {{ from {{ opacity: 0; transform: translateY(-30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}

    /* Print */
    @media print {{
        body {{ background: white; padding: 16px; }}
        .card {{ box-shadow: none; page-break-inside: avoid; }}
        .point-card:hover, .stat-card:hover, .badge:hover {{ transform: none; }}
        .footer {{ color: #333; }}
    }}

    /* Responsive */
    @media (max-width: 768px) {{
        body {{ padding: 20px 12px; }}
        .header h1 {{ font-size: 2.2rem; }}
        .card {{ padding: 24px; }}
        .section-title {{ font-size: 1.5rem; }}
        .stats-grid {{ grid-template-columns: 1fr; }}
        .point-card {{ flex-direction: column; text-align: left; }}
        .point-number {{ margin: 0 0 12px 0; }}
    }}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1>📊 {article_title}</h1>
        <p class="subtitle">AI-Generated Infographic Report • {timestamp}</p>
    </div>

    <!-- Main Points -->
    <div class="card">
        <h2 class="section-title">💡 Key Insights</h2>
        <div class="points-grid">
            {main_points_html or '<div class="empty-state">No main points available</div>'}
        </div>
    </div>

    <!-- Statistics -->
    <div class="card">
        <h2 class="section-title">📈 Key Statistics</h2>
        <div class="stats-grid">
            {supporting_data_html or '<div class="empty-state">No statistics available</div>'}
        </div>
    </div>

    <!-- Chart -->
    <div class="card">
        <h2 class="section-title">📊 Data Visualization</h2>
        <div class="chart-container">
            <img src="/generated/{chart_filename}" alt="Key Statistics Chart" onerror="this.style.display='none'"/>
        </div>
    </div>

    <!-- Visual Suggestions -->
    <div class="card">
        <h2 class="section-title">🎨 Suggested Visuals</h2>
        <div class="badges-container">
            {visuals_html or '<span class="badge">No suggestions available</span>'}
        </div>
    </div>

    <!-- Summary -->
    <div class="card">
        <h2 class="section-title">📝 Summary</h2>
        <div class="summary-box">
            {summary_text}
        </div>
    </div>

    <div class="footer">
        <p>Generated by <a href="/">AI Infographic Generator</a> • Powered by Google Gemini</p>
    </div>
</div>
</body>
</html>
"""
        html_path = self.html_path()
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        print(f"[Exporter] HTML generated: {html_path}")

    def save_pdf(self):
        """
        Convert the generated HTML into PDF using pdfkit + wkhtmltopdf.
        Requires wkhtmltopdf installed on the system. If not available, logs error and returns.
        """
        try:
            import pdfkit
        except ImportError:
            print("[Exporter] pdfkit not installed. Run: pip install pdfkit")
            return

        html_path = self.html_path()
        pdf_path = self.pdf_path()

        if not os.path.exists(html_path):
            print("[Exporter] HTML not found; cannot build PDF.")
            return

        options = {
            "enable-local-file-access": None,
            "load-error-handling": "ignore",
            "quiet": "",
        }

        try:
            # If wkhtmltopdf is not in PATH, you can set explicit config here:
            # config = pdfkit.configuration(wkhtmltopdf="/usr/local/bin/wkhtmltopdf")
            # pdfkit.from_file(html_path, pdf_path, options=options, configuration=config)
            pdfkit.from_file(html_path, pdf_path, options=options)
            if os.path.exists(pdf_path):
                print(f"[Exporter] PDF generated: {pdf_path}")
            else:
                print("[Exporter] PDF file did not appear after conversion.")
        except Exception as e:
            print(f"[Exporter] PDF generation error: {e}")

    def export_all(self, pipeline_result: dict):
        """
        Produce chart, HTML, and PDF for a given pipeline result.
        """
        print("[Exporter] Starting export sequence...")
        self.create_chart(pipeline_result.get("structured_data", {}).get("supporting_data", []))
        self.save_infographic_html(pipeline_result)
        self.save_pdf()
        print("[Exporter] Export sequence completed.")
