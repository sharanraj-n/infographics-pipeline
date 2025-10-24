# 🎨 AI Infographic Generator

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered web application that transforms articles into beautiful, data-rich infographics automatically using Google's Gemini AI.

![Infographic Generator Demo](docs/demo-screenshot.png)

---

## ✨ Features

- 🤖 **AI-Powered Analysis** - Uses Google Gemini to extract key insights, statistics, and visual suggestions
- 📊 **Automatic Chart Generation** - Creates beautiful bar charts from extracted data
- 🎨 **Modern UI** - Responsive web interface with gradient design and smooth animations
- 📄 **Multi-Format Export** - Generate HTML, PNG charts, and PDF documents
- ⚡ **Fast Processing** - Optimized for quick turnaround (10-30 seconds)
- 🔒 **API-First Design** - RESTful API for easy integration
- 🐳 **Docker Ready** - Containerized for easy deployment

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Google Gemini API Key ([Get one here](https://aistudio.google.com/app/apikey))
- (Optional) wkhtmltopdf for PDF generation

### Installation

1. **Clone the repository**

git clone https://github.com/sharanraj-n/infographics-pipeline.git

cd infographics-pipeline

2. **Create virtual environment**

python -m venv venv

source venv/bin/activate # On Windows: venv\Scripts\activate

3. **Install dependencies**

pip install -r requirements.txt

4. **Set up environment variables**

cp .env.example .env

Edit .env and add your Google Gemini API key

GOOGLE_GENAI_API_KEY=your-api-key-here

5. **Run the application**

uvicorn infographic_pipeline.webapi:app --reload

6. **Open in browser**

http://localhost:8000

## 🎯 Usage

### Web Interface

1. Navigate to `http://localhost:8000`
2. Enter an **Article Name** (e.g., `solar_power_2025`)
3. Paste your **Article Text** in the textarea
4. Click **Generate Infographics**
5. Download the generated files:
   - 🌐 **HTML** - Interactive web version
   - 📊 **PNG** - Chart visualization
   - 📄 **PDF** - Printable document

### API Usage

#### Generate Infographic

curl -X POST "http://localhost:8000/run"

-F "article_name=solar_power"

-F "article_text=Your article content here..."

**Response:**

{
"files": {
"html": "generated/solar_power_infographic.html",
"png": "generated/solar_power_chart.png",
"pdf": "generated/solar_power_infographic.pdf"
},
"article_name": "solar_power"
}

#### Download Files

Download HTML

curl "http://localhost:8000/download/solar_power/html" -o infographic.html

Download PNG

curl "http://localhost:8000/download/solar_power/png" -o chart.png

Download PDF

curl "http://localhost:8000/download/solar_power/pdf" -o infographic.pdf

---

## 🐳 Docker Deployment

### Build and Run

Build the image

docker build -t infographic-pipeline .

Run the container

docker run -d
-p 8000:8000
-e GOOGLE_GENAI_API_KEY="your-api-key"
-v $(pwd)/generated:/app/generated
--name infographic-pipeline
infographic-pipeline

### Using Docker Compose

Start services
docker-compose up -d

View logs
docker-compose logs -f

Stop services
docker-compose down

---

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GOOGLE_GENAI_API_KEY` | Google Gemini API key | ✅ Yes | - |
| `OUTPUT_DIR` | Directory for generated files | ❌ No | `generated` |

### Model Configuration

Edit agent files to change the Gemini model:

infographic_pipeline/agents/fine_tuned_article_agent.py
self.llm = ChatGoogleGenerativeAI(
model="gemini-1.5-flash-8b", # Change model here
google_api_key=api_key,
temperature=0.4
)

**Available Models:**
- `gemini-1.5-flash-8b` - Fast, free tier (recommended)
- `gemini-1.5-flash` - Balanced
- `gemini-1.5-pro` - Best quality

---

## 🛠️ Development

### Run Tests

pytest tests/

### Format Code

black infographic_pipeline/
flake8 infographic_pipeline/

### API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## 📊 Architecture

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Google Gemini](https://ai.google.dev/) - AI model provider
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [LangChain](https://www.langchain.com/) - LLM orchestration
- [Matplotlib](https://matplotlib.org/) - Chart generation
- [pdfkit](https://github.com/JazzCore/python-pdfkit) - PDF export

---

## 🐛 Troubleshooting

### Issue: "GOOGLE_GENAI_API_KEY not found"

**Solution:** Make sure you've created a `.env` file with your API key:
echo "GOOGLE_GENAI_API_KEY=your-key-here" > .env

### Issue: "404 models/gemini-xxx is not found"

**Solution:** Check your model name. Use `gemini-1.5-flash-8b` for free tier:
model="gemini-1.5-flash-8b"

### Issue: PDF generation fails

**Solution:** Install wkhtmltopdf:
macOS
brew install wkhtmltopdf # or download from GitHub releases

Ubuntu/Debian
sudo apt-get install wkhtmltopdf

Windows
Download from https://wkhtmltopdf.org/downloads.html

### Issue: Chart image not loading in HTML

**Solution:** Ensure FastAPI is mounting the generated directory:
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

---

## 📧 Contact

**Project Maintainer:** Your Name

- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)

---

## 🗺️ Roadmap

- [ ] Add user authentication
- [ ] Support more chart types (pie, line, scatter)
- [ ] Multi-language support
- [ ] Export to PowerPoint (PPTX)
- [ ] Batch processing via CSV upload
- [ ] Custom color themes
- [ ] AI-powered image generation
- [ ] Database integration for history
- [ ] Cloud storage integration (S3, GCS)
- [ ] Webhook notifications

---

## ⭐ Star History

If you find this project useful, please consider giving it a star on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/infographics-pipeline&type=Date)](https://star-history.com/#yourusername/infographics-pipeline&Date)

---

**Made with ❤️ using Google Gemini AI**

Additional Files to Create:

.env.example

# Google Gemini API Key (required)
# Get yours at: https://aistudio.google.com/app/apikey
GOOGLE_GENAI_API_KEY=your-api-key-here

# Output directory (optional)
OUTPUT_DIR=generated
