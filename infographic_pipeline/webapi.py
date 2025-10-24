import os
from dotenv import load_dotenv
from fastapi import FastAPI, Form
from fastapi.responses import FileResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from .pipeline import InfographicPipeline
from .utils.exporter import InfographicExporter

# Load environment variables from .env
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Mount generated files so they can be accessed directly by HTML
if os.path.exists("generated"):
    app.mount("/generated", StaticFiles(directory="generated"), name="generated")

def safe_filename(name):
    import re
    return re.sub(r'\W+', '_', name.lower()).strip('_')

@app.get("/")
def root():
    """Redirect to the UI"""
    return RedirectResponse(url="/static/ui.html")

@app.post("/run")
async def run_pipeline(article_name: str = Form(...), article_text: str = Form(...)):
    """
    API endpoint to trigger the infographic pipeline.
    Accepts article name and text, returns generated file paths.
    """
    try:
        # Ensure generated directory exists
        if not os.path.exists("generated"):
            os.makedirs("generated")
        
        pipeline = InfographicPipeline()
        result = pipeline.run(article_text)
        exporter = InfographicExporter(article_name=article_name)
        exporter.export_all(result)
        
        files = {
            "html": f"generated/{exporter.article_name}_infographic.html",
            "png": f"generated/{exporter.article_name}_chart.png",
            "pdf": f"generated/{exporter.article_name}_infographic.pdf"
        }
        
        # Only return files that actually exist
        response = {k: v for k, v in files.items() if os.path.exists(v)}
        
        # Debug: Print what files actually exist
        print("Files generated:")
        for k, v in files.items():
            exists = os.path.exists(v)
            print(f"  {k}: {v} - {'EXISTS' if exists else 'MISSING'}")
        
        return JSONResponse({"files": response, "article_name": article_name})
    
    except Exception as e:
        print(f"Pipeline error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

@app.get("/download/{article_name}/{filetype}")
def download_file(article_name: str, filetype: str):
    """
    Download endpoint for generated files (html, png, pdf).
    """
    name = safe_filename(article_name)
    
    if filetype == "html":
        path = f"generated/{name}_infographic.html"
    elif filetype == "png":
        path = f"generated/{name}_chart.png"
    elif filetype == "pdf":
        path = f"generated/{name}_infographic.pdf"
    else:
        return JSONResponse({"error": "Invalid filetype"}, status_code=400)
    
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return JSONResponse({"error": f"File {path} not found."}, status_code=404)
    
    return FileResponse(path)
