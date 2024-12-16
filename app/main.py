from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .models import OnionRequest, TorResponse
import base64

app = FastAPI()

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Entry Proxy"}

@app.post("/relay", response_model=TorResponse)
async def relay_package(request: OnionRequest):
    """
    Accept an onion package and forward it to the Tor network.
    For testing purposes, we'll simulate a successful response.
    In a real implementation, this would:
    1. Verify the package structure
    2. Forward to the entry node
    3. Return the response from the exit node
    """
    try:
        # Verify package structure
        if not request.packages or len(request.packages) != 3:
            raise HTTPException(
                status_code=400,
                detail="Invalid package structure. Must contain exactly 3 layers."
            )

        # For testing, return a mock HTML response
        mock_html = """
        <html>
            <head><title>Test Onion Site</title></head>
            <body>
                <h1>Welcome to the Test Onion Site</h1>
                <p>This is a mock response from the Tor network.</p>
            </body>
        </html>
        """

        return TorResponse(
            content=mock_html,
            status=200
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
