from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.proxy import router

app = FastAPI()

# Enable CORS for browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://onion-browser-proxy-inzpir1h.devinapps.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# Include the proxy router
app.include_router(router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Entry Proxy"}

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}
