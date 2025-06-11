import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "polinka_project")))

from web.web_main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("web.web_main:app", host="0.0.0.0", port=8000, reload=True)

