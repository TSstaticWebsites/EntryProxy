from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.proxy import router as proxy_router

app = FastAPI(title="Entry Proxy")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://onion-browser-proxy-inzpir1h.devinapps.com"],
    allow_credentials=True,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

app.include_router(proxy_router, prefix="/api/v1")
